from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class RetrievalResult:
    chunk_id: str
    score: float
    text: str
    source: str
    page: int | None


def top_k_retrieval(query_vector: np.ndarray, chunk_vectors: list[np.ndarray], chunks: list[dict], top_k: int = 4, threshold: float = 0.2) -> list[RetrievalResult]:
    if not chunk_vectors or not chunks:
        return []

    similarities = []
    for idx, vector in enumerate(chunk_vectors):
        if vector is None:
            continue
        score = float(np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector)))
        similarities.append((idx, score))

    similarities = sorted(similarities, key=lambda item: item[1], reverse=True)
    results: list[RetrievalResult] = []
    for idx, score in similarities:
        if score < threshold:
            continue
        item = chunks[idx]
        results.append(
            RetrievalResult(
                chunk_id=item["chunk_id"],
                score=float(score),
                text=item["text"],
                source=item["source"],
                page=item.get("page"),
            )
        )
        if len(results) >= top_k:
            break
    return results
