"""ChromaDB-based vector store layer for travel knowledge retrieval."""

from __future__ import annotations

from pathlib import Path

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config.settings import BASE_DIR, GEMINI_API_KEY
from rag.documents import load_documents
from rag.embeddings import get_embedding_model_name


def build_vector_store(persist_directory: str | Path | None = None) -> Chroma:
    """Create or rebuild the travel knowledge vector database."""
    persist_dir = Path(persist_directory) if persist_directory else BASE_DIR / "data" / "vectorstore"
    persist_dir.mkdir(parents=True, exist_ok=True)

    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is required to build the vector store.")

    existing_store = Chroma(
        persist_directory=str(persist_dir),
        collection_name="travel_knowledge",
    )
    existing_store.delete_collection()

    embeddings = GoogleGenerativeAIEmbeddings(
        model=get_embedding_model_name(),
        google_api_key=GEMINI_API_KEY,
    )
    docs = load_documents()
    return Chroma.from_documents(
        docs,
        embeddings,
        persist_directory=str(persist_dir),
        collection_name="travel_knowledge",
    )


def get_retriever(k: int = 4):
    """Return a retriever configured for the local travel knowledge base."""
    persist_dir = BASE_DIR / "data" / "vectorstore"
    if not GEMINI_API_KEY:
        return None
    embeddings = GoogleGenerativeAIEmbeddings(
        model=get_embedding_model_name(),
        google_api_key=GEMINI_API_KEY,
    )
    vector_store = Chroma(persist_directory=str(persist_dir), embedding_function=embeddings, collection_name="travel_knowledge")
    return vector_store.as_retriever(search_kwargs={"k": k})


def get_relevant_context(destination: str, query: str, k: int = 4) -> list[str]:
    """Find relevant travel knowledge snippets for a destination and query."""
    retriever = get_retriever(k=k)
    if retriever is None:
        return [
            f"General travel guidance for {destination}: verify visa policies, safety, and local transport from official sources before booking.",
            "Demo-friendly advice: keep travel documents ready and compare local transport costs before departure.",
        ]
    docs = retriever.invoke(f"{destination} {query}")
    return [doc.page_content for doc in docs]


__all__ = ["build_vector_store", "get_retriever", "get_relevant_context"]
