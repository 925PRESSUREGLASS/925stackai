import json

from agents.quote_agent import run_quote
from logic.job_parser import parse_prompt
from logic.pricing_rules import calculate_price


def test_pipeline_known_service(monkeypatch):
    monkeypatch.setattr("logic.pricing_rules.memory_search", lambda q: "none")

    prompt = "Clean 10 windows on a two storey house"
    scope = parse_prompt(prompt)
    pricing = calculate_price(scope)
    assert pricing["total"] > 0

    output = run_quote(prompt)
    data = json.loads(output)
    assert data["total"] == pricing["total"]
    assert "memory_result" not in data


def test_pipeline_unknown_service(monkeypatch):
    monkeypatch.setattr("logic.pricing_rules.memory_search", lambda q: "mock result")

    prompt = "Polish 3 marble floors"
    data = json.loads(run_quote(prompt))
    assert data["items"] == []
    assert data["memory_result"] == "mock result"

