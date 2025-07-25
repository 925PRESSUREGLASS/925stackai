from __future__ import annotations

"""LangChain tool for querying the FAISS retriever."""

from langchain.tools import tool
from langchain_core.documents import Document
from ..memory.memory_setup import get_retriever

_retriever = get_retriever()


@tool
def memory_search(query: str) -> str:
    """Search the FAISS memory and return matching document text."""
    docs = _retriever.invoke(query)
    if not docs:
        return "No documents found."
    if isinstance(docs[0], Document):
        return "\n".join(doc.page_content for doc in docs)
    # fallback for typed list
    return str(docs)


# alias used by tests
tool = memory_search
