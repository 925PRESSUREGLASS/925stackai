
from core.spec_loader import load_tests
from agents.spec_guard import grade_response

def grade_quote_response(prompt: str, response: str) -> dict:
    """
    Grade a quote response against the current spec rules.
    Returns a dict with score, passed, and failures.
    """
    rules = load_tests("quote_generation")["rules"]
    return grade_response(prompt, response, rules)

# Example usage (can be removed in production):
if __name__ == "__main__":
    prompt = "Give me a quote about perseverance"
    response = '"Perseverance is not a long race; it is many short races one after the other."\n— Walter Elliot, Unknown (1930)'
    result = grade_quote_response(prompt, response)
    print("Prompt:", prompt)
    print("Response:", response)
    print("Grading Result:", result)
