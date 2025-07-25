"""FAISS vector store helpers."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List

from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

EMBED_DIM = 1536

def _get_embeddings():
    """Return embeddings implementation based on environment."""
    if os.getenv("OPENAI_API_KEY"):
        return OpenAIEmbeddings()
    return FakeEmbeddings(size=EMBED_DIM)

def get_vectorstore(path: str | Path) -> FAISS:
    """Load or initialize a FAISS vector store at ``path``."""
    path = Path(path)
    embeddings = _get_embeddings()
    if (path / "index.faiss").exists():
        return FAISS.load_local(str(path), embeddings, allow_dangerous_deserialization=True)

    path.mkdir(parents=True, exist_ok=True)
    store = FAISS.from_documents([Document(page_content="dummy")], embeddings)
    store.delete(list(store.index_to_docstore_id.values()))
    store.save_local(str(path))
    return store

def add_documents(store: FAISS, docs: Iterable[str | Document]) -> None:
    """Add text or ``Document`` objects to ``store``."""
    prepared: List[Document] = []
    for d in docs:
        if isinstance(d, Document):
            prepared.append(d)
        else:
            prepared.append(Document(page_content=str(d)))
    if prepared:
        store.add_documents(prepared)

def as_retriever(store: FAISS, *, k: int = 4):
    """Return a retriever for ``store``."""
    return store.as_retriever(search_kwargs={"k": k})


def get_retriever(path: str | Path | None = None):
    """Return a default FAISS retriever."""
    if path is None:
        path = Path(os.getenv("VECTOR_STORE_PATH", "/tmp/faiss_store"))
    store = get_vectorstore(path)
    if not list(store.index_to_docstore_id.values()):
        add_documents(store, ["placeholder memory"])
    return as_retriever(store)
