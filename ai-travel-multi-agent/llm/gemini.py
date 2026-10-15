"""Reusable Gemini client backed by LangChain."""

from __future__ import annotations

from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import GEMINI_API_KEY, GEMINI_MODEL


class GeminiClient:
    """Thin wrapper for Gemini with a clean, reusable interface."""

    def __init__(self, api_key: str = GEMINI_API_KEY, model_name: str = GEMINI_MODEL) -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.client = None
        if self.api_key:
            self.client = ChatGoogleGenerativeAI(
                model=self.model_name,
                google_api_key=self.api_key,
                temperature=0.3,
            )

    def is_configured(self) -> bool:
        """Return True when a Gemini key exists."""
        return bool(self.api_key)

    def invoke(self, prompt: str) -> str:
        """Invoke the Gemini chat model with a plain-text prompt."""
        if not self.client:
            raise RuntimeError("Gemini API key is not configured.")
        return self.client.invoke(prompt).content


__all__ = ["GeminiClient"]
