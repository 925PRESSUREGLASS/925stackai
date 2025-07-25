from modular_ai_agent.agents.base_agent import run_agent


def test_echo() -> None:
    assert "Hello" in run_agent("Hello")
