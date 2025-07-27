from __future__ import annotations

import json
from typing import Any, Dict

from .weblink_agent import index_issue, query_related


class EvaluationAgent:
    """Minimal agent that records issues and returns them as JSON."""

    def __init__(self) -> None:
        self._issues: list[Dict[str, Any]] = []

    def __call__(self, prompt: str) -> str:
        issue: Dict[str, Any] = {"id": len(self._issues) + 1, "description": prompt}
        index_issue(issue)
        issue["related"] = query_related(issue["description"])
        self._issues.append(issue)
        return json.dumps(issue)


def build_evaluation_agent() -> EvaluationAgent:
    return EvaluationAgent()


def run_evaluation(prompt: str) -> str:
    agent = build_evaluation_agent()
    return agent(prompt)


__all__ = ["build_evaluation_agent", "run_evaluation", "EvaluationAgent"]
