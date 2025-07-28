from logic.pricing_rules import calculate_price


def test_calculate_price_window_large() -> None:
    scope = {"service": "window", "qty": 20, "size": "large"}
    result = calculate_price(scope)
    assert "items" in result
    assert result["items"][0]["subtotal"] == 100.0  # 4.0 * 20 * 1.25
    assert result["total"] == 100.0


def test_calculate_price_window_math_expr() -> None:
    # Simulate config with math expression for base_price
    from logic import pricing_rules
    import json
    import os
    config_path = pricing_rules.CONFIG_PATH
    # Backup original config
    with open(config_path, "r", encoding="utf-8") as f:
        original_config = json.load(f)

    # Update window base_price to a math expression
    config = original_config.copy()
    config["window"]["base_price"] = "2 + 2"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f)

    try:
        scope = {"service": "window", "qty": 10}
        result = calculate_price(scope)
        assert result["items"][0]["unit_price"] == "2 + 2"
        assert result["items"][0]["subtotal"] == 40.0  # 4 * 10
        assert result["total"] == 40.0
    finally:
        # Restore original config
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(original_config, f)
