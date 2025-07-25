import json
from logic.pricing_rules import calculate_price

def test_fallback_to_memory(monkeypatch):
    # Patch memory_search where it is used in logic.pricing_rules
    def fake_memory_search(query: str) -> str:
        assert "price per m2 solar" in query
        return "solar panel cleaning costs 12.5 USD per m²."
    monkeypatch.setattr("logic.pricing_rules.memory_search", fake_memory_search)
    scope = {"service": "solar", "qty": 3}
    result = calculate_price(scope)
    assert result["items"] == []
    assert result["total"] == 0.0
    assert "memory_result" in result
    assert "12.5" in result["memory_result"]
