"""Stub grading utility — always passes for now."""

from typing import Any, Dict, Optional


def grade_response(
    prompt: str, response: str, rules: Optional[Dict[str, Any]] | None = None
) -> Dict[str, Any]:
    return {"score": 1.0, "passed": ["stub"], "failures": []}
