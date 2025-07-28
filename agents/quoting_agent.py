"""Minimal quoting agent — replace with real LLM calls later."""


class QuotingAgent:
    def __init__(self) -> None:
        """Initialize the quoting agent."""
        # In real usage you would set up an OpenAI / Ollama client here
        pass

    def run(self, prompt: str) -> str:
        """Return a deterministic placeholder response for the given ``prompt``."""
        return "Quote calculated successfully. (Stub)\n" "Prompt received:\n" + prompt
