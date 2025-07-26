def test_two_storey_surcharge():
    from logic.pricing_rules import calculate_price

    scope = {"service": "window", "qty": 10, "storey": 2}
    result = calculate_price(scope)
    assert result["total"] == 10 * 4 + 40  # base + surcharge
