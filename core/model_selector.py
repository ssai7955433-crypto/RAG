from __future__ import annotations

import json
import subprocess
from typing import Any


def detect_ollama_models() -> tuple[str, str, list[str]]:
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return "", "not_connected", []
        lines = result.stdout.strip().splitlines()
        if len(lines) < 2:
            return "", "not_connected", []
        models: list[str] = []
        for line in lines[1:]:
            if not line.strip():
                continue
            parts = line.split()
            if parts:
                models.append(parts[0])
        return "connected", "ok", models
    except FileNotFoundError:
        return "", "not_connected", []


def get_model_recommendation() -> tuple[str, str]:
    status, _, models = detect_ollama_models()
    if status != "connected":
        return ("No model detected", "N/A")

    normalized = [m.lower() for m in models]
    qwen_candidates = [m for m in normalized if "qwen" in m]
    if qwen_candidates:
        return (qwen_candidates[0], "Qwen")

    llama_candidates = [m for m in normalized if "llama" in m]
    if llama_candidates:
        return (llama_candidates[0], "Llama")

    return ("No Qwen/Llama model detected", "None")


def select_model() -> tuple[str | None, str | None, str | None]:
    status, _, models = detect_ollama_models()
    if status != "connected":
        return None, "Ollama is not installed or not running.", "Install Ollama and pull a local model."

    normalized = [m.lower() for m in models]

    for candidate in normalized:
        if "qwen" in candidate:
            return candidate, "Qwen", None

    for candidate in normalized:
        if "llama" in candidate:
            return candidate, "Llama", None

    return None, "No Qwen or Llama model is installed locally.", "Run: ollama pull qwen3 or ollama pull llama3.2"
