from __future__ import annotations

import json
from typing import Any, Dict, List

from logic.job_parser import parse_prompt
from logic.pricing_rules import calculate_price

try:
    from vector_store.quote_embedder import find_similar_quotes
except Exception:  # pragma: no cover - optional dependency fallback
    def find_similar_quotes(_: Dict[str, Any]) -> List[Dict[str, Any]]:
        return []

try:
    from logic.pricing_engine import calculate_intelligent_price
except Exception:  # pragma: no cover - optional dependency fallback
    def calculate_intelligent_price(_: Dict[str, Any], __: Any | None = None) -> Any:
        raise RuntimeError("pricing engine unavailable")


class QuotingAgent:
    """Quote generation agent with optional similarity and pricing engine."""

    def generate_quote(self, prompt: str, session_state: Dict[str, Any] | None = None) -> Dict[str, Any]:
        job_data = parse_prompt(prompt)
        segment = session_state.get("segment") if session_state else None

        try:
            similar_quotes = find_similar_quotes(job_data)
        except Exception:
            similar_quotes = []

        try:
            price_info = calculate_intelligent_price(job_data, segment)
            intelligent_price = price_info
            items = job_data.get("items", []) if isinstance(price_info, dict) else []
            total = price_info.get("total") if isinstance(price_info, dict) else price_info
        except Exception:
            result = calculate_price(job_data)
            items = result.get("items", [])
            total = result.get("total", 0.0)
            intelligent_price = None
            if "memory_result" in result:
                job_data["memory_result"] = result["memory_result"]

        response = {
            "customer": "Test Customer",
            "items": items,
            "total": total,
            "similar_quotes": similar_quotes,
            "intelligent_price": intelligent_price,
        }
        if "memory_result" in job_data:
            response["memory_result"] = job_data["memory_result"]
        return response


def run_quote(prompt: str, session_state: Dict[str, Any] | None = None) -> str:
    agent = QuotingAgent()
    result = agent.generate_quote(prompt, session_state)
    return json.dumps(result)
