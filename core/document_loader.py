from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any

import fitz
from docx import Document


@dataclass
class LoadedDocument:
    filename: str
    source_type: str
    text: str
    page_count: int


def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages: list[str] = []
    for page in doc:
        text = page.get_text("text")
        if text and text.strip():
            pages.append(text.strip())
    doc.close()
    return "\n\n".join(pages)


def extract_text_from_docx(file_bytes: bytes) -> str:
    stream = BytesIO(file_bytes)
    document = Document(stream)
    paragraphs: list[str] = []
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        if text:
            paragraphs.append(text)
    for table in document.tables:
        for row in table.rows:
            row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
            if row_text:
                paragraphs.append(row_text)
    return "\n\n".join(paragraphs)


def load_document(file_bytes: bytes, filename: str) -> LoadedDocument:
    suffix = Path(filename).suffix.lower()
    if suffix == ".pdf":
        text = extract_text_from_pdf(file_bytes)
        page_count = len(fitz.open(stream=file_bytes, filetype="pdf"))
        return LoadedDocument(filename=filename, source_type="pdf", text=text, page_count=page_count)
    if suffix == ".docx":
        text = extract_text_from_docx(file_bytes)
        stream = BytesIO(file_bytes)
        doc = Document(stream)
        return LoadedDocument(filename=filename, source_type="docx", text=text, page_count=max(1, len(doc.paragraphs)))
    raise ValueError(f"Unsupported file type: {filename}")
