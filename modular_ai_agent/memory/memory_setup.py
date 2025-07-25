from __future__ import annotations

"""Simple FAISS setup for tool tests."""

from langchain_community.vectorstores import FAISS
from langchain.embeddings.fake import FakeEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever


def _build_store() -> VectorStoreRetriever:
    """Create an in-memory FAISS retriever with sample docs."""
    docs = [
        "Hello world document.",
        "Another document about cats.",
        "The sky is blue and the sun is bright.",
    ]
    embeddings = FakeEmbeddings(size=5)
    store = FAISS.from_texts(docs, embeddings)
    return store.as_retriever()


_retriever = _build_store()


def get_retriever() -> VectorStoreRetriever:
    """Return a retriever backed by a FAISS index."""
    return _retriever
