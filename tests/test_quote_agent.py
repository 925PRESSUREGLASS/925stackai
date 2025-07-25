import json

from modular_ai_agent.agents.quote_agent import run_agent, tools as quote_tools
from modular_ai_agent.agents.base_agent import tools as base_tools


def test_quote_json() -> None:
    output = run_agent("Alice", ["widget", "gadget"])
    data = json.loads(output)
    assert data["customer"] == "Alice"
    assert data["items"] == ["widget", "gadget"]
    assert data["total"] == 2


def test_tools_reference() -> None:
    assert quote_tools is base_tools
