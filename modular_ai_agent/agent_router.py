"""Simple intent-based agent router."""

from __future__ import annotations

from typing import Any, Callable, Dict

from agents.quote_agent import run_quote
from modular_ai_agent.tools.memory_tool import memory_search


class Router:
    """Dispatch calls to handlers based on an intent tag."""

    def __init__(self) -> None:
        self._routes: Dict[str, Callable[..., Any]] = {
            "quote": run_quote,
            "memory": memory_search,
        }

    def register(self, tag: str, handler: Callable[..., Any]) -> None:
        """Register ``handler`` for ``tag``."""
        self._routes[tag] = handler

    def route(self, tag: str, *args: Any, **kwargs: Any) -> Any:
        """Dispatch to the handler associated with ``tag``."""
        handler = self._routes.get(tag)
        if handler is None:
            return self.fallback(tag, *args, **kwargs)
        return handler(*args, **kwargs)

    def fallback(self, tag: str, *args: Any, **kwargs: Any) -> str:
        """Default fallback when no tag matches."""
        return f"No handler for intent '{tag}'"
