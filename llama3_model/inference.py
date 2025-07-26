import json
from typing import Any, Dict, Union

from llama3_model.model import Llama3QuoteModel
from llama3_model.utils import condition_logic, quote_formatter


def generate_quote(
    input_data: Union[str, Dict[str, Any]],
    model: Llama3QuoteModel,
    confidence_threshold: float = 0.1,
) -> str:
    """
    Generate a quote for the given job input using the model, with rule-based fallback.
    :param input_data: Job description (dict of fields or raw text prompt).
    :param model: Trained Llama3QuoteModel used for generation.
    :param confidence_threshold: Threshold for confidence/rule deviation to trigger fallback.
    :return: JSON string of the quote (with "customer", "items", "total").
    """
    structured_input = input_data
    if isinstance(input_data, str):
        structured_input = condition_logic.parse_input(input_data)
    prompt = (
        json.dumps(structured_input)
        if isinstance(structured_input, dict)
        else str(structured_input)
    )
    generated_text = model.generate_text(prompt)
    model_output = {}
    try:
        model_output = json.loads(generated_text)
    except json.JSONDecodeError:
        model_output = {}
    rule_result = condition_logic.apply_conditions(structured_input)
    model_total = model_output.get("total")
    rule_total = rule_result.get("total")
    low_confidence = False
    if model_total is None:
        low_confidence = True
    elif rule_total is not None and model_total is not None:
        diff = abs(model_total - rule_total)
        if rule_total > 0 and diff / rule_total > confidence_threshold:
            low_confidence = True
    else:
        low_confidence = True
    final_data = None
    if low_confidence:
        final_data = rule_result
    else:
        final_data = model_output
        if "surcharges" in rule_result and "surcharges" not in final_data:
            final_data["surcharges"] = rule_result["surcharges"]
    customer_name = ""
    if isinstance(input_data, dict):
        customer_name = (
            input_data.get("customer") or input_data.get("customer_name") or ""
        )
    if not customer_name:
        customer_name = "Unknown Customer"
    final_data["customer"] = customer_name
    output_json = quote_formatter.format_quote(final_data)
    return output_json
