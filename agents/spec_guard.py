"""Stub grading utility — always passes for now."""


def grade_response(prompt: str, response: str, rules: dict | None = None):
    return {"score": 1.0, "passed": ["stub"], "failures": []}
