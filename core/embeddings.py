from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


@dataclass
class EmbeddingConfig:
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingEngine:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def encode(self, text: str) -> np.ndarray:
        vector = self.model.encode(text, normalize_embeddings=True)
        return np.asarray(vector, dtype=np.float32)

    @staticmethod
    def cosine_similarity(query_vector: np.ndarray, doc_vectors: list[np.ndarray]) -> np.ndarray:
        if doc_vectors:
            matrix = np.vstack(doc_vectors)
            return cosine_similarity(query_vector.reshape(1, -1), matrix).reshape(-1)
        return np.array([], dtype=np.float32)
