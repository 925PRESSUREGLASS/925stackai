from __future__ import annotations

import re
from typing import Any, Dict, List


# Natural language prompt parser
def parse_prompt(prompt: str) -> Dict[str, Any]:
    """
    Parse a natural language job prompt into a structured job dict.
    Covers: service (window/pressure), qty, size (large), storey, rush/urgent.
    """
    prompt = prompt.lower()
    result: Dict[str, Any] = {}

    # Service detection
    if "window" in prompt:
        result["service"] = "window"
    elif "pressure" in prompt or "power wash" in prompt:
        result["service"] = "pressure"
    else:
        result["service"] = ""

    # Quantity (e.g., "10 windows", "5 jobs")
    qty_match = re.search(r"(\d+)\s*(windows?|jobs?|areas?)", prompt)
    if not qty_match:
        qty_match = re.search(r"(\d+)\b", prompt)
    result["qty"] = int(qty_match.group(1)) if qty_match else 1

    # Size
    result["size"] = "large" if "large" in prompt else ""

    # Storey
    storey_match = re.search(r"(\d+)\s*(storey|story|floor)s?", prompt)
    if storey_match:
        result["storey"] = int(storey_match.group(1))
    elif "two storey" in prompt or "2-storey" in prompt or "second floor" in prompt:
        result["storey"] = 2
    else:
        result["storey"] = 1

    # Rush/Urgent
    if "rush" in prompt or "urgent" in prompt or "asap" in prompt:
        result.setdefault("surcharges", {})["urgent"] = True

    return result


def parse_followup(prompt: str, last_scope: Dict[str, Any]) -> Dict[str, Any]:
    """Merge follow-up instructions into ``last_scope``."""
    updates = parse_prompt(prompt)
    merged = dict(last_scope)

    if updates.get("service"):
        merged["service"] = updates["service"]

    if re.search(r"\d", prompt):
        merged["qty"] = updates.get("qty", merged.get("qty", 1))

    if "large" in prompt:
        merged["size"] = updates.get("size", merged.get("size", ""))

    if re.search(r"(storey|story|floor)", prompt):
        merged["storey"] = updates.get("storey", merged.get("storey", 1))

    if updates.get("surcharges"):
        sur = merged.get("surcharges", {}).copy()
        sur.update(updates["surcharges"])
        merged["surcharges"] = sur

    return merged


def parse_job(data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse a job dictionary and return a normalized job dict."""
    # Example: normalize keys, validate fields, etc.
    job: Dict[str, Any] = {}
    job["service"] = str(data.get("service", ""))
    job["qty"] = int(data.get("qty", 1))
    job["storey"] = int(data.get("storey", 1))
    job["size"] = str(data.get("size", ""))
    job["surcharges"] = data.get("surcharges", {})
    return job


# Example usage for mypy strict compliance
def parse_jobs(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [parse_job(d) for d in data_list]
