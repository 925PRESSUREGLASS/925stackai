import json
from llama3_model.model import Llama3QuoteModel
from llama3_model.inference import generate_quote
from llama3_model.utils.condition_logic import apply_conditions


def test_generate_quote_with_heavy_soil():
    input_description = (
        "Create a quote for cleaning 10 small windows with heavy soiling."
    )
    model = Llama3QuoteModel()
    output_json = generate_quote(
        input_description, model=model, confidence_threshold=0.0
    )
    data = json.loads(output_json)
    assert isinstance(data, dict), "Output is not a JSON object"
    required_keys = {"customer", "items", "total"}
    assert required_keys.issubset(
        set(data.keys())
    ), f"Missing required keys: {required_keys - set(data.keys())}"
    expected = apply_conditions(input_description)
    assert (
        abs(data["total"] - expected["total"]) < 1e-6
    ), "Total does not match expected rule-based total"
