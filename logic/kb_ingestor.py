from __future__ import annotations
from pathlib import Path
from typing import Any, List
import argparse

from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    UnstructuredMarkdownLoader,
    TextLoader,
)
from modular_ai_agent.memory.memory_setup import get_vectorstore

def _loader_for(path: Path) -> Any:
    suf = path.suffix.lower()
    if suf == ".pdf":
        return PyPDFLoader(str(path))
    if suf == ".csv":
        return CSVLoader(str(path))
    if suf in {".md", ".markdown"}:
        return UnstructuredMarkdownLoader(str(path))
    return TextLoader(str(path))

def ingest(target: Path, store: str = "memory/vector_store") -> int:
    files: List[Path] = [p for p in target.rglob("*") if p.is_file()] if target.is_dir() else [target]
    docs = []
    for f in files:
        docs.extend(_loader_for(f).load())
    vs = get_vectorstore(store)
    vs.add_documents(docs)
    vs.save_local(store)
    return len(docs)

def ingest_cli() -> None:
    parser = argparse.ArgumentParser(description="Ingest files into FAISS store")
    parser.add_argument("target", type=Path, help="File or directory to ingest")
    parser.add_argument(
        "--store",
        type=str,
        default="memory/vector_store",
        help="Path where the FAISS index is (will be created if absent)",
    )
    args = parser.parse_args()
    count = ingest(args.target, args.store)
    print(f"✅ Ingested {count} document chunks into {args.store}")
