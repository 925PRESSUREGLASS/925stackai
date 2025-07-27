from __future__ import annotations

import json
from typing import Any, Dict


VALID_MODES = {"scan", "fix", "pr", "log"}


def build_prompt(issue: Dict[str, Any], mode: str = "scan", **kwargs: Any) -> str:
    """Return a JSON encoded prompt for the given issue.

    Parameters
    ----------
    issue: Dict[str, Any]
        Issue data with optional ``title``, ``body``, ``patch`` and ``related`` keys.
    mode: str, optional
        Operation mode. One of ``scan``, ``fix``, ``pr`` or ``log``.

    Returns
    -------
    str
        JSON string containing ``mode`` and ``prompt`` keys.
    """
    if mode not in VALID_MODES:
        raise ValueError(f"Invalid mode: {mode}")

    parts: list[str] = []
    title = issue.get("title", "")
    if title:
        parts.append(f"# {title}")
    body = issue.get("body", "")
    if body:
        parts.append(body)

    patch = issue.get("patch")
    if patch:
        parts.append("### Patch")
        parts.append(patch)

    related = issue.get("related")
    if related:
        parts.append("### Related Knowledge")
        for entry in related:
            if isinstance(entry, dict):
                entry_title = entry.get("title", "")
            else:
                entry_title = str(entry)
            parts.append(f"\u2022 {entry_title}")

    prompt_str = "\n".join(parts)
    return json.dumps({"mode": mode, "prompt": prompt_str})
