"""Simple in-memory search tool."""

from __future__ import annotations

from langchain_core.documents import Document
from langchain_core.tools import Tool

from ..memory.memory_setup import get_retriever

_retriever = get_retriever()


def memory_search(query: str) -> str:
    """Search the memory store and return matching document text."""
    docs = _retriever.invoke(query)
    if not docs:
        return "No documents found."
    if isinstance(docs[0], Document):
        return "\n".join(d.page_content for d in docs)
    return str(docs)


# alias used by tests
tool = memory_search  # type: ignore[assignment]

__all__ = ["tool"]


def get_memory_tool() -> Tool:
    """Return the memory search tool."""
    return Tool.from_function(
        func=memory_search, name="memory_search", description="Search stored documents."
    )
