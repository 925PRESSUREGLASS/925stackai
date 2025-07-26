import json

from agents.quote_agent import build_quote_agent
from logic.pricing_rules import CONFIG_PATH


def test_followup_applies_urgent_surcharge() -> None:
    agent = build_quote_agent()

    first = json.loads(agent("Quote 20 windows"))
    second = json.loads(agent("make that urgent"))

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        surcharge = json.load(f)["surcharge"]["urgent"]

    assert second["total"] == first["total"] + surcharge
