import json
from typing import Any, Dict


def format_quote(quote_data: Dict[str, Any]) -> str:
    for key in ["customer", "items", "total"]:
        if key not in quote_data:
            quote_data[key] = None
    if isinstance(quote_data.get("total"), float):
        quote_data["total"] = round(quote_data["total"], 2)
    if isinstance(quote_data.get("items"), list):
        for item in quote_data["items"]:
            if "subtotal" in item and isinstance(item["subtotal"], float):
                item["subtotal"] = round(item["subtotal"], 2)
    try:
        json_str = json.dumps(quote_data)
    except Exception as e:
        json_str = json.dumps(
            {
                "customer": quote_data.get("customer", ""),
                "items": quote_data.get("items", []),
                "total": quote_data.get("total", 0.0),
            }
        )
    return json_str
