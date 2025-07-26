"""Lightweight model stub for quote generation."""

from __future__ import annotations

from typing import Optional

from llama3_model.utils import condition_logic, quote_formatter


class Llama3QuoteModel:
    """Simplified model that generates quotes using rule logic."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: D401
        """Initialize the model (no-op)."""
        pass

    def generate_text(self, prompt: str, max_new_tokens: int = 64) -> str:
        """Generate a JSON quote based on the input prompt."""
        data = condition_logic.apply_conditions(prompt)
        data["customer"] = "Test Customer"
        return quote_formatter.format_quote(data)

    def chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        max_new_tokens: int = 64,
    ) -> str:
        """Simple chat interface returning generated quote."""
        return self.generate_text(user_message, max_new_tokens=max_new_tokens)

    # Compatibility with original API
    def ollama_chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        model: str = "llama3",
        host: str = "http://localhost:11434",
        max_new_tokens: int = 128,
    ) -> str:
        return self.chat(user_message, system_prompt, max_new_tokens=max_new_tokens)
