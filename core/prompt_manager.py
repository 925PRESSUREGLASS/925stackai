from __future__ import annotations

try:
    from agents.weblink_agent import query_related_knowledge
except Exception:  # pragma: no cover - fallback when module missing
    def query_related_knowledge(_: str) -> list[str]:
        return []

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
    related = query_related_knowledge(issue.get("description", ""))
    if related:
        parts.append("\n".join(["### Related Knowledge", *related]))
    prompt = "\n".join(p for p in parts if p)
    return json.dumps({"mode": mode, "prompt": prompt})
