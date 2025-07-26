from __future__ import annotations

"""CLI helper to ingest knowledge base documents into a FAISS vector store."""

import argparse
from pathlib import Path
from typing import Iterable, List

from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.json_loader import JSONLoader
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.word_document import UnstructuredWordDocumentLoader
from langchain_core.documents import Document

from modular_ai_agent.memory.memory_setup import get_vectorstore, add_documents


_SUPPORTED_SUFFIXES = {
    ".md": UnstructuredMarkdownLoader,
    ".markdown": UnstructuredMarkdownLoader,
    ".txt": TextLoader,
    ".pdf": PyPDFLoader,
    ".csv": CSVLoader,
    ".json": JSONLoader,
    ".docx": UnstructuredWordDocumentLoader,
}

_LOADER_CONFIGS = {
    JSONLoader: {"jq_schema": "."},
}


def _load_file(path: Path) -> List[Document]:
    """Load ``path`` into LangChain ``Document`` objects with metadata."""
    loader_cls = _SUPPORTED_SUFFIXES.get(path.suffix.lower())
    if loader_cls is None:
        return []

    loader_params = _LOADER_CONFIGS.get(loader_cls, {})
    loader = loader_cls(str(path), **loader_params)

    docs = loader.load()
    for doc in docs:
        doc.metadata.setdefault("filename", path.name)
        doc.metadata.setdefault("type", path.suffix.lstrip("."))
        doc.metadata.setdefault("path", str(path))
    return docs


def _collect_files(target: Path) -> Iterable[Path]:
    """Yield all file paths contained in ``target``."""
    if target.is_dir():
        for f in target.rglob("*"):
            if f.is_file() and f.suffix.lower() in _SUPPORTED_SUFFIXES:
                yield f
    elif target.is_file() and target.suffix.lower() in _SUPPORTED_SUFFIXES:
        yield target


def ingest(target: Path, store: str = "memory/vector_store") -> int:
    """Ingest ``target`` into the FAISS store at ``store``."""
    files = list(_collect_files(target))
    docs: List[Document] = []
    for file in files:
        docs.extend(_load_file(file))

    if not docs:
        return 0

    vs = get_vectorstore(store)
    add_documents(vs, docs, store)
    return len(docs)


def ingest_cli() -> None:
    """Entry point for ``python memory/kb_ingestor.py``."""
    parser = argparse.ArgumentParser(description="Ingest files into a FAISS store")
    parser.add_argument("target", type=Path, help="File or directory to ingest")
    parser.add_argument(
        "--store",
        type=str,
        default="memory/vector_store",
        help="Directory for the FAISS vector store",
    )

    args = parser.parse_args()
    count = ingest(args.target, args.store)
    print(f"\u2705 Ingested {count} document chunks into {args.store}")


if __name__ == "__main__":
    ingest_cli()
