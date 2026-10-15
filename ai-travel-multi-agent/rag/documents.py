"""Travel knowledge document loader utilities."""

from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document


def get_knowledge_files() -> list[Path]:
    """Return all travel knowledge files in the knowledge base folder."""
    base = Path(__file__).resolve().parents[1] / "data" / "travel_knowledge"
    return sorted(base.glob("*.md"))


def load_documents() -> list[Document]:
    """Load travel knowledge files as LangChain documents."""
    docs: list[Document] = []
    for file in get_knowledge_files():
        content = file.read_text(encoding="utf-8")
        docs.append(Document(page_content=content, metadata={"source": str(file.name)}))
    return docs


__all__ = ["get_knowledge_files", "load_documents"]
