"""Base agent factory (skeleton)."""

from __future__ import annotations

import os


from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama

from modular_ai_agent.tools import (
    get_math_tool,
    get_memory_tool,
    get_search_tool,
)


class DummyLLM:
    """Fallback LLM that simply echoes the prompt."""

    def predict(self, prompt: str) -> str:  # noqa: D401
        """Return the prompt unchanged."""
        return prompt


def get_llm():
    from langchain_community.llms import Ollama
    return Ollama(model="llama3")


# Default tools available to the agent
tools = [get_search_tool(), get_math_tool(), get_memory_tool()]


def run_agent(prompt: str) -> str:
    """Run a prompt through the agent and return the result."""
    # temporary passthrough until we add tools
    llm = get_llm()
    return llm.predict(prompt)


if __name__ == "__main__":  # pragma: no cover - manual invocation helper
    print(run_agent("Hello!"))
