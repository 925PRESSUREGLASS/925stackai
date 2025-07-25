import json
from agents.quote_agent import run_quote

def test_quote_flow_window():
    prompt = "Quote for 12 large windows, urgent, two storey."
    output = run_quote(prompt)
    data = json.loads(output)
    assert data["customer"] == "Test Customer"
    assert data["total"] > 0
    assert any("window" in item["service"] for item in data["items"])
    assert data["items"][0]["qty"] == 12
    assert data["items"][0]["size"] == "large"
    assert data["total"] > 0
    assert data["items"][0]["subtotal"] > 0
    assert data["total"] > data["items"][0]["subtotal"]  # surcharge applied

def test_quote_flow_pressure():
    prompt = "Pressure wash 5 areas, rush."
    output = run_quote(prompt)
    data = json.loads(output)
    assert data["customer"] == "Test Customer"
    assert data["total"] > 0
    assert any("pressure" in item["service"] for item in data["items"])
    assert data["items"][0]["qty"] == 5
    assert data["total"] > 0

def test_quote_flow_unknown():
    prompt = "Quote for 3 solar panels."
    output = run_quote(prompt)
    data = json.loads(output)
    # Should fallback to memory tool, so items is empty and memory_result present
    assert data["items"] == []
    assert "memory_result" in data
