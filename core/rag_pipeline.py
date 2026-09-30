from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from core.chunker import Chunk, chunk_text
from core.document_loader import load_document
from core.embeddings import EmbeddingEngine
from core.model_selector import select_model
from core.ollama_client import OllamaClient
from core.retriever import top_k_retrieval
from core.text_cleaner import clean_text


@dataclass
class IndexState:
    documents: list[dict[str, Any]] = field(default_factory=list)
    chunks: list[dict[str, Any]] = field(default_factory=list)
    vectors: list[np.ndarray] = field(default_factory=list)


@dataclass
class RAGConfig:
    chunk_size: int = 500
    chunk_overlap: int = 80
    top_k: int = 4
    threshold: float = 0.2
    temperature: float = 0.2


class RAGPipeline:
    def __init__(self) -> None:
        self.config = RAGConfig()
        self.index = IndexState()
        self.embedding_engine = EmbeddingEngine()
        self.client = OllamaClient()
        self.chat_history: list[dict[str, str]] = []

    def process_uploaded_file(self, uploaded_file) -> dict[str, Any]:
        file_bytes = uploaded_file.getvalue()
        filename = uploaded_file.name
        loaded = load_document(file_bytes, filename)
        cleaned = clean_text(loaded.text)
        if not cleaned.strip():
            return {"status": "error", "message": "Document is empty."}

        source_chunks = chunk_text(cleaned, chunk_size=self.config.chunk_size, chunk_overlap=self.config.chunk_overlap, source_name=filename)
        vectors = []
        chunk_records: list[dict[str, Any]] = []
        for chunk in source_chunks:
            vector = self.embedding_engine.encode(chunk.text)
            vectors.append(vector)
            chunk_records.append({
                "chunk_id": chunk.chunk_id,
                "source": chunk.source,
                "page": chunk.page,
                "text": chunk.text,
                "vector": vector,
            })

        self.index.documents.append({
            "filename": filename,
            "type": loaded.source_type,
            "page_count": loaded.page_count,
            "char_count": len(cleaned),
        })
        self.index.chunks.extend(chunk_records)
        self.index.vectors.extend(vectors)

        return {"status": "ok", "chunks": len(source_chunks), "chars": len(cleaned)}

    def answer_question(self, question: str) -> dict[str, Any]:
        if not self.index.chunks:
            return {"answer": "Please upload a document first.", "sources": [], "retrieved_context": ""}

        cleaned_question = clean_text(question)
        query_vector = self.embedding_engine.encode(cleaned_question)
        results = top_k_retrieval(query_vector, self.index.vectors, self.index.chunks, top_k=self.config.top_k, threshold=self.config.threshold)

        if not results:
            return {
                "answer": "I could not find relevant information in the uploaded document for that question. Please ask a question related to the document content.",
                "sources": [],
                "retrieved_context": "",
            }

        context_block = "\n\n".join(f"[Source: {item.source} | Page: {item.page}]\n{item.text}" for item in results)
        model_name, family, message = select_model()
        if not model_name:
            return {
                "answer": message or "No local Ollama model is available.",
                "sources": [{"source": item.source, "page": item.page, "score": item.score} for item in results],
                "retrieved_context": context_block,
            }

        prompt = (
            "You are a grounded document assistant. Answer only using the retrieved context below. "
            "Do not invent facts. If the answer is not in the context, say that the information was not found in the uploaded documents. "
            "Be concise and mention the source document or page when possible.\n\n"
            f"Context:\n{context_block}\n\nQuestion:\n{cleaned_question}"
        )

        generated = self.client.generate(model_name, prompt, temperature=self.config.temperature)
        answer = generated.strip() if generated.strip() else "No answer produced from the local model."
        self.chat_history.append({"question": cleaned_question, "answer": answer})

        return {
            "answer": answer,
            "sources": [{"source": item.source, "page": item.page, "score": item.score} for item in results],
            "retrieved_context": context_block,
            "model": model_name,
        }
