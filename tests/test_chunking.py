from core.chunker import chunk_text


def test_chunk_creation_basic():
    text = "This is a sample document. " * 30
    chunks = chunk_text(text, chunk_size=120, chunk_overlap=20)
    assert len(chunks) > 0
    assert all(chunk.text for chunk in chunks)


def test_chunk_overlap_not_negative():
    text = "Alpha beta gamma delta epsilon zeta eta theta"
    chunks = chunk_text(text, chunk_size=30, chunk_overlap=50)
    assert len(chunks) > 0
