import json

from agents.quote_agent import run_quote


def test_run_quote_returns_valid_json():
    prompt = "Please quote 20 large windows for cleaning"
    output = run_quote(prompt)
    data = json.loads(output)
    assert isinstance(data, dict)
    assert set(data.keys()) == {"customer", "items", "total"}
    # Allow for LLM variability: just check total is a positive float
    assert isinstance(data["total"], (int, float))
    assert data["total"] > 0
