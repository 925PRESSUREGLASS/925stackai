
"""Lightweight spec‑compliance checker used during dev/test runs."""

from __future__ import annotations

import re
from typing import Dict, List, Any


def _check_regex(pattern: str, target: str) -> bool:
    return bool(re.search(pattern, target, flags=re.MULTILINE))


def _check_char_limit(limit: int, quote: str) -> bool:
    # only measure first line (quote text)
    first_line = quote.split("\n", 1)[0].strip("\n")
    return len(first_line) <= limit


def grade_response(prompt: str, response: str, rules: Dict[str, Any]) -> Dict[str, Any]:
    """Grade *response* against *rules* extracted from validation.json."""

    checks = {
        "quote_wrapped": lambda r: _check_regex(rules["quote_wrapped"], response),
        "has_source": lambda r: _check_regex(rules["has_source"], response),
        "char_limit": lambda r: _check_char_limit(rules["char_limit"], response),
    }

    passed: List[str] = []
    failures: List[str] = []

    for name, fn in checks.items():
        (passed if fn(response) else failures).append(name)

    score = round(len(passed) / max(len(passed) + len(failures), 1), 2)
    return {"score": score, "passed": passed, "failures": failures}
