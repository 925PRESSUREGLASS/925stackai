"""Base agent factory (skeleton)."""

from __future__ import annotations

import os

from langchain_openai import ChatOpenAI


class DummyLLM:
    """Fallback LLM that simply echoes the prompt."""

    def predict(self, prompt: str) -> str:  # noqa: D401
        """Return the prompt unchanged."""
        return prompt


def get_llm(model: str = "gpt-4o-mini"):
    """Return an LLM instance.

    If an OpenAI API key is configured, ``ChatOpenAI`` will be used; otherwise a
    simple echo model is returned so tests can run without network access.
    """
    if os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(model_name=model, temperature=0)  # type: ignore[call-arg]
    return DummyLLM()


def run_agent(prompt: str) -> str:
    """Run a prompt through the agent and return the result."""
    # temporary passthrough until we add tools
    llm = get_llm()
    return llm.predict(prompt)


if __name__ == "__main__":  # pragma: no cover - manual invocation helper
    print(run_agent("Hello!"))
