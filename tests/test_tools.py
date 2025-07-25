from modular_ai_agent.tools import get_search_tool, get_math_tool
from langchain_core.tools import Tool


def test_get_search_tool() -> None:
    tool = get_search_tool()
    assert isinstance(tool, Tool)


def test_get_math_tool() -> None:
    tool = get_math_tool()
    assert isinstance(tool, Tool)
