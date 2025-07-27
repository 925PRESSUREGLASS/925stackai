import json

from core.prompt_manager import build_prompt


def test_prompt_includes_related_section() -> None:
    issue = {"title": "Bug", "body": "Details", "related": [{"title": "Doc1"}, {"title": "Doc2"}]}
    output = build_prompt(issue, mode="scan")
    data = json.loads(output)
    assert "Related Knowledge" in data["prompt"]
    assert "\u2022 Doc1" in data["prompt"]
    assert "\u2022 Doc2" in data["prompt"]


def test_modes_produce_valid_json() -> None:
    issue = {"title": "Bug"}
    for m in ["scan", "fix", "pr", "log"]:
        out = build_prompt(issue, mode=m)
        data = json.loads(out)
        assert data["mode"] == m
        assert isinstance(data["prompt"], str)
