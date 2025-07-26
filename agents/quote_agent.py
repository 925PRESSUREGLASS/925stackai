"""
Quote agent that uses LangChain, pricing_rules.calculate_price,
and returns STRICT JSON {"customer", "items", "total"}.
"""

import json
from typing import Any, Dict, Callable

from modular_ai_agent.agents.base_agent import get_llm, tools

from logic.pricing_rules import calculate_price
from logic.job_parser import parse_prompt


def build_quote_agent() -> Callable[[str], str]:
    # For now, just a passthrough using pricing_rules and tools
    llm = get_llm()

    def agent(prompt: str) -> str:
        # Parse the prompt into a scope dict
        scope = parse_prompt(prompt)
        customer = "Test Customer"
        pricing = calculate_price(scope)
        result = {
            "customer": customer,
            "items": pricing["items"],
            "total": pricing["total"],
        }
        # If pricing has memory_result (fallback), include it in output
        if "memory_result" in pricing:
            result["memory_result"] = pricing["memory_result"]
        return json.dumps(result)

    return agent


def run_quote(prompt: str) -> str:
    agent = build_quote_agent()
    output = agent(prompt)
    # Ensure output is valid JSON with required keys
    data = json.loads(output)
    assert all(k in data for k in ("customer", "items", "total"))
    return output
