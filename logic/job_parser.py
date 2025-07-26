from __future__ import annotations

import re
from typing import Dict

pricing_rules = {
    "window": 50.0,
    "gutter_clean": 120.0,
    "urgent_surcharge": 40.0,
}

WINDOW_RE = re.compile(r"(\d+)\s*windows?")


def parse_prompt(prompt: str) -> Dict[str, any]:
    """Parse an initial job prompt into a quote scope."""
    scope: Dict[str, any] = {}
    text = prompt.lower()

    match = WINDOW_RE.search(text)
    if match:
        scope["windows"] = int(match.group(1))

    if "gutter" in text:
        scope["gutter_clean"] = True

    if "urgent" in text:
        scope["urgent"] = True

    return scope


def parse_followup(prompt: str, last_scope: Dict[str, any]) -> Dict[str, any]:
    """Merge follow-up instructions with the last scope."""
    updates = parse_prompt(prompt)
    merged = last_scope.copy()
    merged.update(updates)
    return merged
