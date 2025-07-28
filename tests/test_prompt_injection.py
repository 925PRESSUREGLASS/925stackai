import json

from core.prompt_manager import build_prompt


def test_prompt_includes_related_section(monkeypatch) -> None:
    monkeypatch.setattr(
        "agents.weblink_agent.query_related_knowledge",
        lambda desc: ["Doc1", "Doc2"],
        raising=False,
    )
    issue = {"title": "Bug", "body": "Details", "description": "some bug"}
    output = build_prompt(issue, mode="scan")
    data = json.loads(output)
    assert "Related Knowledge" in data["prompt"]
    assert "Doc1" in data["prompt"]
    assert "Doc2" in data["prompt"]


def test_modes_produce_valid_json() -> None:
    issue = {"title": "Bug"}
    for m in ["scan", "fix", "pr", "log"]:
        out = build_prompt(issue, mode=m)
        data = json.loads(out)
        assert data["mode"] == m
        assert isinstance(data["prompt"], str)
