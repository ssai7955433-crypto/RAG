import numpy as np

from core.embeddings import EmbeddingEngine


def test_embedding_engine_returns_vector():
    engine = EmbeddingEngine(model_name='sentence-transformers/all-MiniLM-L6-v2')
    vector = engine.encode('This is a test sentence.')
    assert isinstance(vector, np.ndarray)
    assert vector.shape[0] > 0
