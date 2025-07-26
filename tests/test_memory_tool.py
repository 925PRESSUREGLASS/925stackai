from modular_ai_agent.tools.memory_tool import tool


def test_tool_returns_text() -> None:
    result = tool.invoke("hello")
    assert isinstance(result, str)
    assert bool(result)
