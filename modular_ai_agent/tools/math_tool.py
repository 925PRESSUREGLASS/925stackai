"""Math evaluation tool utilities."""

from __future__ import annotations

from langchain_core.tools import Tool


import ast

def _safe_eval(expression: str) -> str:
    """Safely evaluate a math expression using ast.literal_eval."""
    try:
        result = ast.literal_eval(expression)
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
