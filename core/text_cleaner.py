from __future__ import annotations

import re


def clean_text(text: str) -> str:
    if not text:
        return ""

    cleaned = text.replace("\r", "\n")
    cleaned = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", cleaned)
    cleaned = cleaned.replace("\u00a0", " ")
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\n +", "\n", cleaned)
    cleaned = re.sub(r" +\n", "\n", cleaned)
    cleaned = re.sub(r"\n{2,}", "\n\n", cleaned)

    paragraphs = [segment.strip() for segment in cleaned.split("\n\n") if segment.strip()]
    fixed: list[str] = []
    for paragraph in paragraphs:
        normalized = re.sub(r"\s+", " ", paragraph).strip()
        if normalized:
            fixed.append(normalized)

    return "\n\n".join(fixed)
