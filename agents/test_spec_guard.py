import pytest
from agents.spec_guard import grade_response

@pytest.mark.parametrize("response,expected_score", [
    ("> \"Learning never exhausts the mind.\"  \n> — *Leonardo da Vinci* (1500)\n\n**Analysis:** This quote highlights the endless potential of curiosity.", 1.0),
    ("> \"Learning never exhausts the mind.\"  \n> — *Leonardo da Vinci* (1500)", 0.67),
    ("> \"Learning never exhausts the mind.\"", 0.33),
    ("No quote format here.", 0.0),
])
def test_grade_response(response, expected_score):
    rules = {
        "checks": [
            {"name": "quote_format", "pattern": "^>", "weight": 1},
            {"name": "attribution", "pattern": "—", "weight": 1},
            {"name": "analysis_section", "pattern": "\\*\\*Analysis:", "weight": 1},
        ]
    }
    result = grade_response("dummy prompt", response, rules)
    assert result["score"] == expected_score
