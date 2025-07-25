"""Math evaluation tool utilities."""

from __future__ import annotations

from langchain_core.tools import Tool


def _safe_eval(expression: str) -> str:
    """Evaluate a math expression in a restricted namespace."""
    try:
        result = eval(expression, {"__builtins__": {}})
    except Exception as exc:  # pragma: no cover - error path
        return f"Error: {exc}"
    return str(result)


def get_math_tool() -> Tool:
    """Return a simple calculator tool."""
    return Tool.from_function(
        func=_safe_eval,
        name="calculator",
        description="Evaluate a math expression.",
    )
