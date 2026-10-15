"""Tests for retrieval behavior and knowledge-base access."""

from __future__ import annotations

from rag.documents import get_knowledge_files, load_documents
from rag.embeddings import get_embedding_model_name


def test_knowledge_files_exist() -> None:
    """Confirm the travel knowledge base includes destination documents."""
    files = get_knowledge_files()
    assert any("singapore" in file.name for file in files)
    assert any("travel_tips" in file.name for file in files)


def test_load_documents() -> None:
    """Check that markdown knowledge sources load into LangChain documents."""
    docs = load_documents()
    assert len(docs) >= 1
    assert docs[0].page_content


def test_embedding_model_name() -> None:
    """Use a currently supported Gemini text embedding model."""
    assert get_embedding_model_name() == "models/gemini-embedding-001"
