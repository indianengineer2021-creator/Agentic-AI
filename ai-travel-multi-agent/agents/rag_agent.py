"""Retrieval-augmented knowledge agent for travel planning."""

from __future__ import annotations

from rag.vectorstore import get_relevant_context


def retrieve_travel_context(destination: str, query: str) -> list[str]:
    """Return the top relevant travel knowledge snippets for a destination."""
    return get_relevant_context(destination=destination, query=query, k=4)


def retrieve_info() -> str:
    """Compatibility helper for early scaffold usage."""
    return "RAG agent initialized."


__all__ = ["retrieve_travel_context", "retrieve_info"]
