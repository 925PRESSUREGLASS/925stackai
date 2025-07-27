"""
Quote agent that uses LangChain, pricing_rules.calculate_price,
and returns STRICT JSON {"customer", "items", "total"}.
"""

import json
from typing import Any, Callable, Dict

from langchain.memory import ConversationBufferMemory

from logic.job_parser import parse_followup, parse_prompt
from logic.pricing_rules import calculate_price
from modular_ai_agent.agents.base_agent import get_llm


class QuoteAgent:
    """Stateful quote agent keeping short conversation history."""

    def __init__(self) -> None:
        self.llm = get_llm()
        # Updated for LangChain 0.3.1+ memory API
        # Updated for LangChain 0.3.1+ memory API (see migration guide)
        self.memory = ConversationBufferMemory()  # TODO: See LangChain memory migration guide for future updates
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


# --- CLI chat interface ---
if __name__ == "__main__":
    print("Quote Agent CLI Chat. Type 'exit' to quit.\n")
    agent = build_quote_agent()
    while True:
        try:
            prompt = input("You: ")
            if prompt.strip().lower() in {"exit", "quit"}:
                print("Exiting.")
                break
            response = agent(prompt)
            print(f"Agent: {response}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break
