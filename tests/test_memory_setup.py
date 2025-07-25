from pathlib import Path

from langchain_core.documents import Document
from modular_ai_agent.memory.memory_setup import get_vectorstore, add_documents, as_retriever


def test_memory_roundtrip(tmp_path: Path) -> None:
    store_path = tmp_path / "vs"
    vs = get_vectorstore(store_path)
    add_documents(vs, [Document(page_content="tiny doc")])
    # Re-instantiate retriever after adding documents to ensure index is updated
    retriever = as_retriever(vs, k=1)
    docs = retriever.invoke("tiny")
    assert any("tiny doc" in d.page_content for d in docs)
