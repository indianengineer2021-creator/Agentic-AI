"""Embedding configuration for the ChromaDB travel knowledge base."""

from __future__ import annotations

from config.settings import GEMINI_API_KEY


def get_embedding_model_name() -> str:
    """Return the default embedding model identifier."""
    return "models/gemini-embedding-001"


def get_embedding_backend() -> str:
    """Return the backend name used for embeddings."""
    return "gemini" if GEMINI_API_KEY else "demo"


__all__ = ["get_embedding_model_name", "get_embedding_backend"]
