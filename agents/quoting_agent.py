"""Minimal quoting agent — replace with real LLM calls later."""


class QuotingAgent:
    def __init__(self):
        # In real usage you would set up an OpenAI / Ollama client here
        pass

    def run(self, prompt: str) -> str:
        # \u2728 Stubbed deterministic response
        return (
            "Quote calculated successfully. (Stub)\n"
            "Prompt received:\n" + prompt
        )
