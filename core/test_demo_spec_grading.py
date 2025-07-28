from core.demo_spec_grading import grade_quote_response


def test_perfect_quote():
    prompt = "Give me a quote about perseverance"
    response = '"Perseverance is not a long race; it is many short races one after the other."\n— Walter Elliot, Unknown (1930)'
    result = grade_quote_response(prompt, response)
    assert result["score"] == 1.0
    assert set(result["passed"]) == {"quote_wrapped", "has_source", "char_limit"}
    assert result["failures"] == []


def test_missing_source():
    prompt = "Give me a quote about perseverance"
    response = '"Perseverance is not a long race; it is many short races one after the other."'
    result = grade_quote_response(prompt, response)
    assert "has_source" in result["failures"]
    assert result["score"] < 1.0


def test_too_long():
    prompt = "Give me a quote about perseverance"
    response = '"' + "a" * 300 + '"\n— Walter Elliot, Unknown (1930)'
    result = grade_quote_response(prompt, response)
    assert "char_limit" in result["failures"]
    assert result["score"] < 1.0
