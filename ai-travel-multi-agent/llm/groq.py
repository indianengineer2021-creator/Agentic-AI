"""Reusable Groq chat client for structured agent review."""

from __future__ import annotations

from langchain_groq import ChatGroq

from config.settings import GROQ_API_KEY, GROQ_MODEL
from models.schemas import TravelReview


class GroqClient:
    """Use Groq to analyze and return a structured review of agent outputs."""

    def __init__(self, api_key: str = GROQ_API_KEY, model_name: str = GROQ_MODEL) -> None:
        self.api_key = api_key
        self.model_name = model_name
        self.client = None
        if self.api_key:
            self.client = ChatGroq(
                model=self.model_name,
                groq_api_key=self.api_key,
                temperature=0.2,
            )

    def is_configured(self) -> bool:
        """Return True when a Groq API key exists."""
        return bool(self.api_key)

    def review(self, prompt: str) -> TravelReview:
        """Invoke Groq and validate its structured travel-plan review."""
        if not self.client:
            raise RuntimeError("Groq API key is not configured.")
        response = self.client.with_structured_output(TravelReview).invoke(prompt)
        review = TravelReview.model_validate(response)
        return review.model_copy(update={"provider": "groq", "model": self.model_name})


__all__ = ["GroqClient"]
