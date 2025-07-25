from logic.pricing_rules import calculate_price


def test_calculate_price_window_large() -> None:
    scope = {"service": "window", "qty": 20, "size": "large"}
    result = calculate_price(scope)
    assert "items" in result
    assert result["items"][0]["subtotal"] == 100.0  # 4.0 * 20 * 1.25
    assert result["total"] == 100.0
