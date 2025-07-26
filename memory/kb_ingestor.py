from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any, Iterable, List

from langchain_community.document_loaders import (
    CSVLoader,
    JSONLoader,
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings


def _get_embeddings() -> OpenAIEmbeddings:
    """Return OpenAI embeddings instance, ensuring API key is configured."""
    if not os.getenv("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY environment variable not set")
    return OpenAIEmbeddings()


def _loader_for(path: Path) -> Any:
    ext = path.suffix.lower()
    if ext in {".md", ".markdown"}:
        return UnstructuredMarkdownLoader(str(path))
    if ext == ".csv":
        return CSVLoader(str(path))
    if ext == ".json":
        return JSONLoader(str(path))
    if ext == ".pdf":
        return PyPDFLoader(str(path))
    if ext == ".docx":
        return UnstructuredWordDocumentLoader(str(path))
    return TextLoader(str(path))


def _iter_files(target: Path) -> Iterable[Path]:
    if target.is_dir():
        for p in target.rglob("*"):
            if p.is_file():
                yield p
    else:
        yield target


def _load_docs(path: Path) -> List[Document]:
    docs: List[Document] = _loader_for(path).load()
    for d in docs:
        d.metadata.update(
            {
                "filename": path.name,
                "type": path.suffix.lstrip("."),
                "path": str(path),
            }
        )
    return docs


def _get_store(path: Path) -> FAISS:
    embeddings = _get_embeddings()
    if (path / "index.faiss").exists():
        return FAISS.load_local(
            str(path), embeddings, allow_dangerous_deserialization=True
        )
    path.mkdir(parents=True, exist_ok=True)
    store = FAISS.from_documents([Document(page_content="placeholder")], embeddings)
    store.save_local(str(path))
    return store


def _persist(store: FAISS, path: Path) -> None:
    # Remove placeholder docs if still present
    for idx, doc_id in list(store.index_to_docstore_id.items()):
        doc = store.docstore.search(doc_id)
        if isinstance(doc, Document) and doc.page_content == "placeholder":
            store.delete([doc_id])
    store.save_local(str(path))


def ingest(target: Path, store: str = "memory/vector_store") -> int:
    files = list(_iter_files(target))
    docs: List[Document] = []
    for fp in files:
        docs.extend(_load_docs(fp))

    if not docs:
        return 0

    store_path = Path(store)
    vs = _get_store(store_path)
    vs.add_documents(docs)
    _persist(vs, store_path)
    return len(docs)


def ingest_cli() -> None:
    parser = argparse.ArgumentParser(description="Ingest files into FAISS store")
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
