import numpy as np

from core.retriever import top_k_retrieval


def test_top_k_retrieval_returns_highest_score():
    qv = np.array([1.0, 0.0])
    chunk_vectors = [np.array([1.0, 0.0]), np.array([0.0, 1.0]), np.array([0.2, 0.9])]
    chunks = [
        {"chunk_id": "a", "text": "first", "source": "doc1", "page": 1},
        {"chunk_id": "b", "text": "second", "source": "doc1", "page": 2},
        {"chunk_id": "c", "text": "third", "source": "doc1", "page": 3},
    ]
    results = top_k_retrieval(qv, chunk_vectors, chunks, top_k=2, threshold=0.0)
    assert results[0].chunk_id == "a"
    assert len(results) >= 1
