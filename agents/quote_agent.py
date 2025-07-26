from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict
import re

from langchain.memory import ConversationBufferMemory

from logic.job_parser import parse_followup, pricing_rules


@dataclass
class QuoteAgent:
    """Simple quoting agent with short term memory."""

    memory: ConversationBufferMemory = field(default_factory=lambda: ConversationBufferMemory(k=3, return_messages=True))
    scope: Dict[str, any] = field(default_factory=dict)

    def build_quote_agent(self) -> "QuoteAgent":
        """Initialize or reset agent state while preserving memory."""
        if not isinstance(self.memory, ConversationBufferMemory):
            self.memory = ConversationBufferMemory(k=3, return_messages=True)
        return self

    def _calculate_total(self) -> float:
        windows = self.scope.get("windows", 0)
        total = windows * pricing_rules.get("window", 0)
        if self.scope.get("gutter_clean"):
            total += pricing_rules.get("gutter_clean", 0)
        if self.scope.get("urgent"):
            total += pricing_rules.get("urgent_surcharge", 0)
        self.scope["total"] = total
        return total

    def handle_prompt(self, prompt: str) -> str:
        """Process a user prompt and update quote."""
        self.scope = parse_followup(prompt, self.scope)
        total = self._calculate_total()
        response = (
            f"Quote for {self.scope.get('windows', 0)} windows"
        )
        if self.scope.get("gutter_clean"):
            response += " with gutter cleaning"
        if self.scope.get("urgent"):
            response += " (urgent)"
        response += f". Total: ${total:.2f}"

        # track conversation
        self.memory.chat_memory.add_user_message(prompt)
        self.memory.chat_memory.add_ai_message(response)
        return response
