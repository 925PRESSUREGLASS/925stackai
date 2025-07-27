import json
from core.prompt_manager import build_prompt


def test_related_section_added():
    issue = {
        "title": "Test issue",
        "body": "Fix the bug",
        "related": [
            {"title": "KB Article 1"},
            {"title": "KB Article 2"},
        ],
    }
    result = build_prompt(issue)
    data = json.loads(result)
    assert "Related Knowledge" in data["prompt"]
    assert "KB Article 1" in data["prompt"]
    assert "KB Article 2" in data["prompt"]

