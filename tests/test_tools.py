from langchain_core.tools import Tool

from modular_ai_agent.tools import get_math_tool, get_search_tool


def test_get_search_tool() -> None:
    tool = get_search_tool()
    assert isinstance(tool, Tool)


def test_get_math_tool() -> None:
    tool = get_math_tool()
    assert isinstance(tool, Tool)
