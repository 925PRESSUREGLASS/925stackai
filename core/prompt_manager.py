from __future__ import annotations

import json
from typing import Any, Dict, Iterable


VALID_MODES = {"scan", "fix", "pr", "log"}

def _format_related(related: Iterable[Any]) -> str:
    """Return a formatted related knowledge section."""
    lines = ["### Related Knowledge"]
    for item in related:
        title = item.get("title") if isinstance(item, dict) else str(item)
        lines.append(f"\u2022 {title}")
    return "\n".join(lines)


def build_prompt(issue: Dict[str, Any], *, mode: str = "scan", **_: Any) -> str:
    """Build a prompt string for the given ``issue`` and ``mode``."""
    if mode not in VALID_MODES:
        raise ValueError(f"Unsupported mode: {mode}")

    parts = [issue.get("title", ""), issue.get("body", "")]
    related = issue.get("related")
    if related:
        parts.append(_format_related(related))
    prompt = "\n".join(p for p in parts if p)
    return json.dumps({"mode": mode, "prompt": prompt})
