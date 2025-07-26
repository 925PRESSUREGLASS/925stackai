from gui.components import parse_quote_output


def test_parse_quote_output() -> None:
    json_str = (
        '{"customer": "Bob", "items": [{"service": "window", "qty": 1, '
        '"unit_price": 2, "size": "", "subtotal": 2}], "total": 2}'
    )
    data = parse_quote_output(json_str)
    assert data["customer"] == "Bob"
    assert data["total"] == 2
    assert data["items"][0]["service"] == "window"
