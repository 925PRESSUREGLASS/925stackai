from modular_ai_agent.agents.base_agent import run_agent


def test_echo() -> None:
    result = run_agent("Hello")
    assert "Hello" in result or result == "Hello"
