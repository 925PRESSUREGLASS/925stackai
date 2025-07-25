"""
Domain-specific quoting agent.

Uses the same LangChain tools list as the base agent.

Replies strictly in JSON:
{ "customer": "<name>", "items": [...], "total": <number> }
"""

from __future__ import annotations

import json
import re
from typing import List, Dict, Any

from modular_ai_agent.tools.memory_tool import memory_search

from .base_agent import get_llm, tools as base_tools

# Export the same tool list so it can be extended elsewhere
tools = base_tools


def run_agent(customer: str, items: List[str]) -> str:
    """Return a simple JSON quote for ``items``."""
    # The LLM is unused for now but kept for API parity
    llm = get_llm()
    _ = llm.predict("quote")
    quote = {
        "customer": customer,
        "items": items,
        "total": len(items),
    }
    return json.dumps(quote)


def run_quote(prompt: str) -> str:
    """Compute a material quote from ``prompt``.

    ``prompt`` should mention an area in square meters and optionally a
    material. If either value cannot be parsed or the price lookup fails,
    ``total`` will be ``null`` and ``items`` will be empty in the returned
    JSON string.
    """
    text = prompt.replace("m\u00b2", "m2")
    match = re.search(r"(?P<area>\d+(?:\.\d+)?)\s*m2(?:\s+(?P<material>\w+))?", text, re.I)
    if not match:
        return json.dumps({"items": [], "total": None})

    area = float(match.group("area"))
    material = match.group("material")
    if not material:
        return json.dumps({"items": [], "total": None})

    price_str = memory_search(f"price per m2 for {material}")
    m_price = re.search(r"(\d+(?:\.\d+)?)", price_str)
    if not m_price:
        return json.dumps({"items": [], "total": None})
    price = float(m_price.group(1))

    total = area * price
    item: Dict[str, Any] = {
        "material": material,
        "area_m2": area,
        "unit_price": price,
    }
    return json.dumps({"items": [item], "total": total})
