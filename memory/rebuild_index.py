#!/usr/bin/env python3
"""Utility to rebuild the local vector store from a directory of documents."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    CSVLoader,
    DirectoryLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def _loader_for(path: Path):
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return PyPDFLoader(str(path))
    if suffix == ".csv":
        return CSVLoader(str(path))
    if suffix in {".md", ".markdown"}:
        return UnstructuredMarkdownLoader(str(path))
    return TextLoader(str(path))


def _ingest(path: Path) -> List:
    files = [p for p in path.rglob("*") if p.is_file()]
    docs = []
    for f in files:
        docs.extend(_loader_for(f).load())
    return docs


def rebuild(input_dir: Path, store_dir: Path) -> None:
    docs = _ingest(input_dir)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vs = FAISS.from_documents(splits, embeddings)
    store_dir.mkdir(parents=True, exist_ok=True)
    vs.save_local(str(store_dir))


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild vector store")
    parser.add_argument("--input", type=Path, required=True, help="Docs directory")
    parser.add_argument(
        "--store", type=Path, required=True, help="Destination vector store path"
    )
    args = parser.parse_args()
    rebuild(args.input, args.store)
    print(f"\u2705 Vector store rebuilt at {args.store}")


if __name__ == "__main__":
    main()
