"""
Pricing engine for window cleaning & pressure washing.
Exposes `calculate_price(scope: dict) -> dict`.
Reads `configs/pricing.json` at runtime.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from modular_ai_agent.tools.memory_tool import memory_search
from modular_ai_agent.tools.math_tool import _safe_eval

CONFIG_PATH = Path(__file__).parent.parent / "configs" / "pricing.json"


@dataclass
class PricingRecord:
    service: str
    qty: int
    size: str = ""
    surcharges: Optional[Dict[str, Any]] = None
    items: Optional[List[Any]] = None
    total: float = 0.0


def calculate_price(scope: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate price based on scope and pricing config."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    service = scope.get("service")
    qty = int(scope.get("qty", 1))
    size = scope.get("size", "")
    surcharges = dict(scope.get("surcharges", {}))

    # Automatically apply two_storey surcharge if storey >= 2
    if service == "window" and int(scope.get("storey", 1)) >= 2:
        surcharges["two_storey"] = True

    items = []
    total = 0.0

    if service not in config:
        # Fallback: search memory for price per m2
        query = f"price per m2 {service}"
        # Assume memory_search implements an 'invoke' method as per protocol
        memory_result = memory_search.invoke(query)
        return {
            "items": [],
            "surcharges": surcharges,
            "total": 0.0,
            "memory_result": memory_result,
        }

    base_price = config[service]["base_price"]
    # Support math expressions in base_price
    if isinstance(base_price, str):
        try:
            base_price_eval = float(_safe_eval(base_price))
        except Exception:
            base_price_eval = 0.0
    else:
        base_price_eval = base_price
    price = base_price_eval * qty

    # Apply size multiplier if applicable
    if size and "large_multiplier" in config[service] and size == "large":
        large_multiplier = config[service]["large_multiplier"]
        if isinstance(large_multiplier, str):
            try:
                large_multiplier_eval = float(_safe_eval(large_multiplier))
            except Exception:
                large_multiplier_eval = 1.0
        else:
            large_multiplier_eval = large_multiplier
        price *= large_multiplier_eval

    items.append(
        {
            "service": service,
            "qty": qty,
            "unit_price": base_price,
            "size": size,
            "subtotal": round(price, 2),
        }
    )

    # Apply surcharges
    surcharge_total = 0.0
    for key, value in (surcharges or {}).items():
        surcharge_cfg = config.get("surcharge", {}).get(key)
        if surcharge_cfg:
            if isinstance(surcharge_cfg, str):
                try:
                    surcharge = float(_safe_eval(surcharge_cfg)) if value else 0
                except Exception:
                    surcharge = 0
            elif isinstance(surcharge_cfg, (int, float)):
                surcharge = surcharge_cfg if value else 0
            else:
                surcharge = 0
            surcharge_total += surcharge

    total = price + surcharge_total

    return {"items": items, "surcharges": surcharges, "total": round(total, 2)}
