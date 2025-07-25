from modular_ai_agent.tools.memory_tool import tool


def test_tool_returns_text():
    result = tool("hello")
    assert isinstance(result, str) and result
