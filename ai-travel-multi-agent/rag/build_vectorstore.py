"""Build the ChromaDB travel knowledge vectorstore for the app."""

from __future__ import annotations

from rag.vectorstore import build_vector_store


def main() -> None:
    """Create the vector database from the local markdown travel knowledge."""
    build_vector_store()
    print("Vector store built successfully.")


if __name__ == "__main__":
    main()
