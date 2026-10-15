"""Reusable xAI Grok client backed by LangChain."""

from __future__ import annotations

from langchain_xai import ChatXAI

from config.settings import GROK_MODEL, XAI_API_KEY


class GrokClient:
    """Thin wrapper for Grok as an independent reviewer model."""

    def __init__(self, api_key: str = XAI_API_KEY, model_name: str = GROK_MODEL) -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.client = None
        if self.api_key:
            self.client = ChatXAI(
                model=self.model_name,
                xai_api_key=self.api_key,
                temperature=0.2,
            )

    def is_configured(self) -> bool:
        """Return True when a Grok API key exists."""
        return bool(self.api_key)

    def invoke(self, prompt: str) -> str:
        """Invoke the Grok model with a plain-text prompt."""
        if not self.client:
            raise RuntimeError("Grok API key is not configured.")
        return self.client.invoke(prompt).content


__all__ = ["GrokClient"]
