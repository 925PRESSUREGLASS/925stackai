import json

from modular_ai_agent.agents.quote_agent import (
    run_agent,
    run_quote,
    tools as quote_tools,
)
from modular_ai_agent.agents.base_agent import tools as base_tools


def test_quote_json() -> None:
    output = run_agent("Alice", ["widget", "gadget"])
    data = json.loads(output)
    assert data["customer"] == "Alice"
    assert data["items"] == ["widget", "gadget"]
    assert data["total"] == 2


def test_tools_reference() -> None:
    assert quote_tools is base_tools


def test_run_quote_success(monkeypatch) -> None:
    monkeypatch.setattr(
        "modular_ai_agent.agents.quote_agent.memory_search",
        lambda q: "50",
    )
    result = json.loads(run_quote("SmallCo wants 10 m\u00b2 epoxy"))
    assert result["total"] == 10 * 50
    assert result["items"] == [
        {"material": "epoxy", "area_m2": 10.0, "unit_price": 50.0}
    ]


def test_run_quote_price_missing(monkeypatch) -> None:
    monkeypatch.setattr(
        "modular_ai_agent.agents.quote_agent.memory_search",
        lambda q: "No documents found.",
    )
    result = json.loads(run_quote("10 m\u00b2 mystery"))
    assert result["total"] is None
    assert result["items"] == []
