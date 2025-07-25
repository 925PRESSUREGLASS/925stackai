"""Web search tool utilities."""

from __future__ import annotations

from langchain_core.tools import Tool

try:
    from langchain_community.tools import DuckDuckGoSearchRun
except Exception:  # pragma: no cover - optional dependency
    DuckDuckGoSearchRun = None  # type: ignore[misc]


def _dummy_search(query: str) -> str:
    """Fallback search implementation."""
    return f"Search results for '{query}' are unavailable."


def get_search_tool() -> Tool:
    """Return a search tool, falling back to a dummy tool if needed."""
    if DuckDuckGoSearchRun is not None:
        return Tool.from_function(
            func=DuckDuckGoSearchRun().run,
            name="search",
            description="Search the web for information using DuckDuckGo.",
        )
    return Tool.from_function(
        func=_dummy_search,
        name="search",
        description="Search the web for information.",
    )
