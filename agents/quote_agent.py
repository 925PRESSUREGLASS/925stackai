"""
Quote agent that uses LangChain, pricing_rules.calculate_price,
and returns STRICT JSON {"customer", "items", "total"}.
"""

import json
from typing import Any, Dict, Callable
from langchain.memory import ConversationBufferMemory

from modular_ai_agent.agents.base_agent import get_llm

from logic.pricing_rules import calculate_price
from logic.job_parser import parse_prompt, parse_followup


class QuoteAgent:
    """Stateful quote agent keeping short conversation history."""

    def __init__(self) -> None:
        self.llm = get_llm()
        self.memory = ConversationBufferMemory()
        self._last_scope: Dict[str, Any] | None = None

    def __call__(self, prompt: str) -> str:
        if self._last_scope is None:
            scope = parse_prompt(prompt)
        else:
            scope = parse_followup(prompt, self._last_scope)
        self._last_scope = scope

        self.memory.chat_memory.add_user_message(prompt)
        customer = "Test Customer"
        pricing = calculate_price(scope)
        result = {
            "customer": customer,
            "items": pricing["items"],
            "total": pricing["total"],
        }
        if "memory_result" in pricing:
            result["memory_result"] = pricing["memory_result"]

        response = json.dumps(result)
        self.memory.chat_memory.add_ai_message(response)
        return response


def build_quote_agent() -> Callable[[str], str]:
    """Return a stateful quote agent instance."""

    return QuoteAgent()


def run_quote(prompt: str) -> str:
    agent = build_quote_agent()
    output = agent(prompt)
    # Ensure output is valid JSON with required keys
    data = json.loads(output)
    assert all(k in data for k in ("customer", "items", "total"))
    return output
