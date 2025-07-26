"""Simple vector store utilities using JSON persistence."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Any


@dataclass
class Document:
    page_content: str
    metadata: dict | None = None


class SimpleVectorStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.docs: List[str] = []
        self._load()

    def _load(self) -> None:
        if (self.path / "store.json").exists():
            with open(self.path / "store.json", "r", encoding="utf-8") as f:
                self.docs = json.load(f)
        else:
            self.docs = []

    def save(self) -> None:
        self.path.mkdir(parents=True, exist_ok=True)
        with open(self.path / "store.json", "w", encoding="utf-8") as f:
            json.dump(self.docs, f)

    @classmethod
    def from_documents(
        cls, docs: Iterable[Document], path: Path
    ) -> "SimpleVectorStore":
        store = cls(path)
        store.add_documents(docs)
        return store

    def add_documents(self, docs: Iterable[Document]) -> None:
        for d in docs:
            self.docs.append(d.page_content)
        self.save()

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Return documents containing all words from the query."""
        words = query.lower().split()
        results = [Document(d) for d in self.docs if all(w in d.lower() for w in words)]
        return results[:k]

    def as_retriever(self, *, k: int = 4) -> Any:
        class Retriever:
            def __init__(self, store: SimpleVectorStore, limit: int) -> None:
                self.store = store
                self.limit = limit

            def invoke(self, query: str) -> List[Document]:
                return self.store.similarity_search(query, k=self.limit)

        return Retriever(self, k)


def get_vectorstore(path: str | Path) -> SimpleVectorStore:
    path = Path(path)
    store = SimpleVectorStore(path)
    if not store.docs:
        store.add_documents([Document(page_content="hello world")])
    return store


def add_documents(
    store: SimpleVectorStore, docs: Iterable[str | Document], path: str | Path
) -> None:
    prepared = [
        d if isinstance(d, Document) else Document(page_content=str(d)) for d in docs
    ]
    store.add_documents(prepared)


def as_retriever(store: SimpleVectorStore, *, k: int = 4) -> Any:
    return store.as_retriever(k=k)


def get_retriever(path: str | Path | None = None, *, k: int = 4) -> Any:
    if path is None:
        path = Path(os.getenv("VECTOR_STORE_PATH", "memory/vector_store"))
    store = get_vectorstore(path)
    return as_retriever(store, k=k)
