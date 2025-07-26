"""Web search tool utilities."""

from __future__ import annotations

from typing import Any

from langchain_core.tools import Tool

search_run_cls: Any = None
try:
    from langchain_community.tools import DuckDuckGoSearchRun

    search_run_cls = DuckDuckGoSearchRun
except Exception:  # pragma: no cover - optional dependency
    pass


def _dummy_search(query: str) -> str:
    """Fallback search implementation."""
    return f"Search results for '{query}' are unavailable."


def get_search_tool() -> Tool:
    """Return a search tool, falling back to a dummy tool if needed."""
    if search_run_cls is not None:
        return Tool.from_function(
            func=search_run_cls().run,
            name="search",
            description="Search the web for information using DuckDuckGo.",
        )
    return Tool.from_function(
        func=_dummy_search,
        name="search",
        description="Search the web for information.",
    )
