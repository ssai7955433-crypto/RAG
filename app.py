from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from core.model_selector import detect_ollama_models, get_model_recommendation
from core.rag_pipeline import RAGPipeline

st.set_page_config(page_title="Local RAG Workshop", page_icon="📚", layout="wide")


@st.cache_resource
def get_pipeline() -> RAGPipeline:
    return RAGPipeline()


def render_header() -> None:
    st.markdown(
        """
        <div style='padding: 0.5rem 0 1rem 0;'>
            <h1 style='margin-bottom: 0;'>Hands-On RAG Workshop</h1>
            <p style='margin-top: 0.2rem; color: #64748b;'>Local LLM • Qwen → Llama fallback • Q&A over uploaded documents</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    model_name, model_family = get_model_recommendation()
    ollama_status = "Connected" if detect_ollama_models()[0] else "Not Connected"
    st.markdown(
        f"""
        <div style='display:flex; gap: 12px; flex-wrap: wrap; margin-bottom: 1rem;'>
            <span style='background:#e0f2fe; color:#075985; padding: 6px 10px; border-radius: 999px;'>Model: <strong>{model_name}</strong> ({model_family})</span>
            <span style='background:#dcfce7; color:#166534; padding: 6px 10px; border-radius: 999px;'>Ollama: {ollama_status}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    render_header()
    pipeline = get_pipeline()

    st.sidebar.header("Workshop Settings")
    top_k = st.sidebar.slider("Top-K retrieval", 1, 10, 4)
    threshold = st.sidebar.slider("Similarity threshold", 0.0, 1.0, 0.25, step=0.01)
    chunk_size = st.sidebar.slider("Chunk size", 150, 1200, 500, step=50)
    chunk_overlap = st.sidebar.slider("Chunk overlap", 0, 300, 80, step=10)
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2, step=0.05)

    pipeline.config.top_k = top_k
    pipeline.config.threshold = threshold
    pipeline.config.chunk_size = chunk_size
    pipeline.config.chunk_overlap = chunk_overlap
    pipeline.config.temperature = temperature

    uploaded_files = st.file_uploader(
        "Upload PDF or DOCX",
        type=["pdf", "docx"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            pipeline.process_uploaded_file(uploaded_file)

    st.subheader("Knowledge Base")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Documents", len(pipeline.index.documents))
    with col2:
        st.metric("Chunks", len(pipeline.index.chunks))
    with col3:
        st.metric("Embedding model", "SentenceTransformer")
    with col4:
        st.metric("Retrieval", "Enabled")

    if not pipeline.index.documents:
        st.info("Upload a PDF or DOCX to start the RAG workshop demo.")
        return

    question = st.text_input("Ask a question about the uploaded document")
    if st.button("Generate answer") and question:
        answer = pipeline.answer_question(question)
        st.subheader("Answer")
        st.write(answer["answer"])

        if answer.get("sources"):
            st.subheader("Sources")
            for source in answer["sources"]:
                st.markdown(
                    f"- **{source['source']}** • page {source.get('page', 'n/a')} • score {source.get('score', 0.0):.3f}"
                )

        if answer.get("retrieved_context"):
            st.subheader("Retrieved context")
            st.text_area("Context used by the model", answer["retrieved_context"], height=220)

    st.subheader("Chat history")
    for message in pipeline.chat_history:
        st.write(f"**You:** {message['question']}")
        st.write(f"**Assistant:** {message['answer']}")


if __name__ == "__main__":
    main()
