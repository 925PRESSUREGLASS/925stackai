"""FAISS vector store helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List, Any

from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

EMBED_DIM = 1536


def _get_embeddings() -> OpenAIEmbeddings | FakeEmbeddings:
    """Return embeddings implementation based on environment."""
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIEmbeddings()
    return FakeEmbeddings(size=EMBED_DIM)


def get_vectorstore(path: str | Path) -> FAISS:
    """Load or initialize a FAISS vector store at ``path``."""
    path = Path(path)
    embeddings = _get_embeddings()
    if (path / "index.faiss").exists():
        return FAISS.load_local(
            str(path), embeddings, allow_dangerous_deserialization=True
        )

    path.mkdir(parents=True, exist_ok=True)
    store = FAISS.from_documents([Document(page_content="dummy")], embeddings)
    store.save_local(str(path))
    return store


def add_documents(store: FAISS, docs: Iterable[str | Document], path: str | Path) -> None:
    """Add text or ``Document`` objects to ``store`` and persist the index."""
    prepared: List[Document] = []
    for d in docs:
        if isinstance(d, Document):
            prepared.append(d)
        else:
            prepared.append(Document(page_content=str(d)))
    if prepared:
        store.add_documents(prepared)
        # Remove placeholder document if present using public API
        for idx, doc_id in list(store.index_to_docstore_id.items()):
          
for idx, doc_id in list(store.index_to_docstore_id.items()):
    doc = store.docstore.search(doc_id)
    # Handle both Document and str types
    if doc:
        if hasattr(doc, "page_content"):
            if doc.page_content == "dummy":
                store.delete([doc_id])
        elif isinstance(doc, str):
            if doc == "dummy":
                store.delete([doc_id])
store.save_local(str(path))


def as_retriever(store: FAISS, *, k: int = 4) -> Any:
    """Return a retriever for ``store``."""
    return store.as_retriever(search_kwargs={"k": k})


def get_retriever(path: str | Path | None = None, *, k: int = 4) -> Any:
    """Convenience wrapper to load a vector store and return its retriever."""
    if path is None:
        path = Path(os.getenv("VECTOR_STORE_PATH", "memory/vector_store"))
    store = get_vectorstore(path)
    if not store.index_to_docstore_id:
        store.add_documents([Document(page_content="hello world")])
        store.save_local(str(Path(path)))
    return as_retriever(store, k=k)
