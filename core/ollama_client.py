from __future__ import annotations

import json
import time
from typing import Any

import requests


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434") -> None:
        self.base_url = base_url.rstrip("/")

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def list_models(self) -> list[str]:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code != 200:
                return []
            payload = response.json()
            return [item.get("name", "") for item in payload.get("models", []) if item.get("name")]
        except requests.RequestException:
            return []

    def generate(self, model: str, prompt: str, temperature: float = 0.2) -> str:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature},
        }
        response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result.get("response", "")
