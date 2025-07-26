import json
import re
from pathlib import Path
from typing import Any, Dict, Union

CONFIG_PATH = Path(__file__).parent.parent / "config" / "pricing_rules.json"
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    PRICING_CONFIG = json.load(f)

def apply_conditions(input_data: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    if isinstance(input_data, str):
        input_data = parse_input(input_data)
    result: Dict[str, Any] = {"items": [], "surcharges": {}, "total": 0.0}
    if not input_data:
        return result
    service = input_data.get("service")
    qty = int(input_data.get("qty", 1))
    size = input_data.get("size", "")
    surcharges = dict(input_data.get("surcharges", {}))
    if service not in PRICING_CONFIG:
        return result
    service_config = PRICING_CONFIG[service]
    base_price = service_config.get("base_price", 0.0)
    price = base_price * qty
    if size and service_config.get("large_multiplier") and str(size).lower() == "large":
        price *= service_config["large_multiplier"]
    item_entry = {
        "service": service,
        "qty": qty,
        "unit_price": base_price,
        "size": size,
        "subtotal": round(price, 2)
    }
    result["items"].append(item_entry)
    if service == "window" and int(input_data.get("storey", 1)) >= 2:
        surcharges["two_storey"] = True
    total_surcharge = 0.0
    for key, value in surcharges.items():
        surcharge_cfg = PRICING_CONFIG.get("surcharge", {}).get(key)
        if not surcharge_cfg:
            continue
        if isinstance(surcharge_cfg, (int, float)):
            if isinstance(value, bool) and value:
                total_surcharge += surcharge_cfg
            elif isinstance(value, (int, float)) and value != 0:
                total_surcharge += surcharge_cfg * value
        result["surcharges"][key] = value
    total = price + total_surcharge
    result["total"] = round(total, 2)
    return result

def parse_input(text: str) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    text_lower = text.lower()
    if "window" in text_lower:
        data["service"] = "window"
    elif "pressure" in text_lower or "power wash" in text_lower:
        data["service"] = "pressure"
    match = re.search(r'(\d+)', text_lower)
    if match:
        qty = int(match.group(1))
        data["qty"] = qty
    if "large" in text_lower:
        data["size"] = "large"
    elif "small" in text_lower:
        data["size"] = "small"
    conditions = {}
    if "heavy" in text_lower or "heavy soil" in text_lower or "heavily soiled" in text_lower:
        conditions["heavy_soil"] = True
    if "urgent" in text_lower or "rush" in text_lower:
        conditions["urgent"] = True
    if "two-storey" in text_lower or "two story" in text_lower or "2 storey" in text_lower or "2 story" in text_lower:
        data["storey"] = 2
    if conditions:
        data["surcharges"] = conditions
    return data
