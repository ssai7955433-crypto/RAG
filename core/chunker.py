from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Chunk:
    chunk_id: str
    text: str
    source: str
    page: int | None = None
    start_char: int = 0
    end_char: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


def split_paragraphs(text: str) -> list[str]:
    paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
    return paragraphs


def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 80, source_name: str = "document", page_number: int | None = None) -> list[Chunk]:
    if not text or chunk_size <= 0:
        return []

    if chunk_overlap >= chunk_size:
        chunk_overlap = max(0, chunk_size // 4)

    paragraphs = split_paragraphs(text)
    chunks: list[Chunk] = []
    buffer: list[str] = []
    current_length = 0

    for paragraph in paragraphs:
        buffer.append(paragraph)
        current_length += len(paragraph)

        if current_length >= chunk_size:
            combined = " ".join(buffer)
            chunks.append(
                Chunk(
                    chunk_id=f"{source_name}-chunk-{len(chunks) + 1}",
                    text=combined,
                    source=source_name,
                    page=page_number,
                    start_char=0,
                    end_char=len(combined),
                    metadata={"source": source_name, "page": page_number},
                )
            )
            buffer = [combined[-max(1, chunk_overlap):]] if chunk_overlap else []
            current_length = len(" ".join(buffer)) if buffer else 0

    if buffer:
        combined = " ".join(buffer)
        if combined.strip():
            chunks.append(
                Chunk(
                    chunk_id=f"{source_name}-chunk-{len(chunks) + 1}",
                    text=combined,
                    source=source_name,
                    page=page_number,
                    start_char=0,
                    end_char=len(combined),
                    metadata={"source": source_name, "page": page_number},
                )
            )

    if not chunks:
        normalized = " ".join(part for part in paragraphs)
        if normalized.strip():
            chunks.append(
                Chunk(
                    chunk_id=f"{source_name}-chunk-1",
                    text=normalized[:chunk_size],
                    source=source_name,
                    page=page_number,
                    start_char=0,
                    end_char=len(normalized[:chunk_size]),
                    metadata={"source": source_name, "page": page_number},
                )
            )

    return chunks
