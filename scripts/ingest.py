#!/usr/bin/env python3
"""
CLI helper that ingests files or folders into the FAISS vector store.

Usage:
    python scripts/ingest.py <path> [--store memory/vector_store]

If <path> is a directory, it is walked recursively.
Supported file types:
    .pdf  →  PyPDFLoader
    .csv  →  CSVLoader
    .md   →  UnstructuredMarkdownLoader
    .txt  →  TextLoader (fallback)
"""

import argparse
from pathlib import Path

from langchain.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    UnstructuredMarkdownLoader,
    TextLoader,
)
from modular_ai_agent.memory.memory_setup import get_vectorstore


def _loader_for(path: Path):
    suf = path.suffix.lower()
    if suf == ".pdf":
        return PyPDFLoader(str(path))
    if suf == ".csv":
        return CSVLoader(str(path))
    if suf in {".md", ".markdown"}:
        return UnstructuredMarkdownLoader(str(path))
    return TextLoader(str(path))


def main():
    parser = argparse.ArgumentParser(description="Ingest files into FAISS store")
    parser.add_argument("target", type=Path, help="File or directory to ingest")
    parser.add_argument(
        "--store",
        type=str,
        default="memory/vector_store",
        help="Path where the FAISS index is (will be created if absent)",
    )
    args = parser.parse_args()

    target: Path = args.target
    files = (
        [p for p in target.rglob("*") if p.is_file()] if target.is_dir() else [target]
    )

    docs = []
    for f in files:
        docs.extend(_loader_for(f).load())

    vs = get_vectorstore(args.store)
    vs.add_documents(docs)
    print(f"✅ Ingested {len(docs)} document chunks into {args.store}")


if __name__ == "__main__":
    main()
