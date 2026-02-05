from __future__ import annotations

import os
from typing import Any

import requests

DISCLAIMER = "هذا النظام لا يقدم استشارات قانونية أو فتاوى."


class LexeraAIClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("LEXERA_API_BASE_URL", "https://api.groq.com/openai/v1")
        self.api_key = os.getenv("LEXERA_API_KEY", "")
        self.model = os.getenv("LEXERA_MODEL", "llama-3.3-70b-versatile")
        self.timeout = int(os.getenv("LEXERA_API_TIMEOUT", "60"))

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        if not self.configured:
            raise RuntimeError("LEXERA_API_KEY is not configured")

        url = f"{self.base_url.rstrip('/')}/chat/completions"
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Lexera legal research assistant for Egypt. "
                        "Never provide legal advice, fatwas, or final legal decisions. "
                        "Provide research-only analysis with clear limitations."
                    ),
                },
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        message = data["choices"][0]["message"]["content"]
        return f"{message}\n\n⚠️ {DISCLAIMER}"
