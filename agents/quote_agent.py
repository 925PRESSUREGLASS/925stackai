"""Simple quote agent using rule-based pricing."""

from __future__ import annotations

import json
from typing import Any, Dict, Callable

from logic.pricing_rules import calculate_price
from logic.job_parser import parse_prompt, parse_followup


class ConversationBufferMemory:
    """Minimal conversation memory stub."""

    class ChatMemory(list):
        def add_user_message(self, msg: str) -> None:
            self.append(("user", msg))

        def add_ai_message(self, msg: str) -> None:
            self.append(("ai", msg))

    def __init__(self) -> None:
        self.chat_memory = self.ChatMemory()


class QuoteAgent:
    """Stateful quote agent keeping short conversation history."""

    def __init__(self) -> None:
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
