from __future__ import annotations
import argparse
from pathlib import Path
from typing import List

from modular_ai_agent.memory.memory_setup import Document, get_vectorstore


def _loader_for(path: Path) -> List[Document]:
    """Return a list of Documents loaded from ``path``."""
    text = path.read_text(encoding="utf-8")
    return [Document(page_content=text)]


def ingest(target: Path, store: str = "memory/vector_store") -> int:
    files: List[Path] = (
        [p for p in target.rglob("*") if p.is_file()] if target.is_dir() else [target]
    )
    docs = []
    for f in files:
        docs.extend(_loader_for(f))
    vs = get_vectorstore(store)
    from modular_ai_agent.memory.memory_setup import add_documents as _add_docs

    _add_docs(vs, docs, store)
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
