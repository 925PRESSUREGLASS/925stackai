"""
Domain-specific quoting agent.

Uses the same LangChain tools list as the base agent.

Replies strictly in JSON:
{ "customer": "<name>", "items": [...], "total": <number> }
"""

from __future__ import annotations

import json
from typing import List

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
