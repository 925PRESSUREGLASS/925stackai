import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from agents.quote_agent import QuoteAgent
from logic.job_parser import pricing_rules


def test_urgent_followup_increases_total():
    agent = QuoteAgent().build_quote_agent()
    agent.handle_prompt("Quote 20 windows")
    base_total = agent.scope["total"]

    agent.handle_prompt("make that urgent")
    new_total = agent.scope["total"]

    assert new_total - base_total == pricing_rules["urgent_surcharge"]
