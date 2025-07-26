from pathlib import Path

from langchain_core.documents import Document

from modular_ai_agent.memory.memory_setup import (add_documents, as_retriever,
                                                  get_vectorstore)


def test_memory_roundtrip(tmp_path: Path) -> None:
    store_path = tmp_path / "vs"
    vs = get_vectorstore(store_path)
    add_documents(vs, [Document(page_content="tiny doc")], store_path)
    # Reload the store from disk to ensure FAISS index is up to date
    vs_reloaded = get_vectorstore(store_path)
    retriever = as_retriever(vs_reloaded, k=1)
    docs = retriever.invoke("tiny")
    assert any("tiny doc" in d.page_content for d in docs)
