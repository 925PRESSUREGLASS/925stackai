"""Base agent factory (skeleton)."""

from __future__ import annotations




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
    """Return OllamaLLM if available, otherwise a dummy LLM."""
    try:
        from langchain_ollama import OllamaLLM
        return OllamaLLM(model="llama3")
    except Exception:
        return DummyLLM()


# Default tools available to the agent
tools = [get_search_tool(), get_math_tool(), get_memory_tool()]


def run_agent(prompt: str) -> str:
    """Run a prompt through the agent and return the result."""
    llm = get_llm()
    try:
        return llm.invoke(prompt)
    except Exception:
        return DummyLLM().predict(prompt)


if __name__ == "__main__":  # pragma: no cover - manual invocation helper
    print(run_agent("Hello!"))
