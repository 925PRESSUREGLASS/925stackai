"""CLI for ingesting knowledge files into a FAISS vector store."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    CSVLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_community.document_loaders.base import BaseLoader

from modular_ai_agent.memory.memory_setup import get_vectorstore, add_documents


SUPPORTED_SUFFIXES = {
    ".md",
    ".markdown",
    ".csv",
    ".txt",
    ".pdf",
    ".docx",
}


def _loader_for(path: Path) -> BaseLoader:
    suf = path.suffix.lower()
    if suf in {".md", ".markdown"}:
        return UnstructuredMarkdownLoader(str(path))
    if suf == ".csv":
        return CSVLoader(str(path))
    if suf == ".pdf":
        return PyPDFLoader(str(path))
    if suf == ".docx":
        return UnstructuredWordDocumentLoader(str(path))
    return TextLoader(str(path))


def _load_with_metadata(path: Path) -> List[Document]:
    docs = _loader_for(path).load()
    for d in docs:
        d.metadata.update(
            {
                "filename": path.name,
                "type": path.suffix.lstrip("."),
                "path": str(path),
            }
        )
    return docs


def _iter_files(target: Path) -> Iterable[Path]:
    if target.is_dir():
        for f in target.rglob("*"):
            if f.is_file() and f.suffix.lower() in SUPPORTED_SUFFIXES:
                yield f
    else:
        if target.suffix.lower() in SUPPORTED_SUFFIXES:
            yield target


def ingest(target: Path | str, store: str = "memory/vector_store") -> int:
    target_path = Path(target)
    docs: List[Document] = []
    for file in _iter_files(target_path):
        docs.extend(_load_with_metadata(file))
    if not docs:
        return 0
    vs = get_vectorstore(store)
    add_documents(vs, docs, store)
    return len(docs)


def ingest_cli() -> None:
    parser = argparse.ArgumentParser(description="Ingest files into a FAISS store")
    parser.add_argument("target", type=Path, help="File or directory to ingest")
    parser.add_argument(
        "--store",
        type=str,
        default="memory/vector_store",
        help="Directory for the FAISS index",
    )
    args = parser.parse_args()
    count = ingest(args.target, args.store)
    print(f"✅ Ingested {count} document chunks into {args.store}")


if __name__ == "__main__":
    ingest_cli()
