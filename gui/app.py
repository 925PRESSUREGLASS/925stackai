from __future__ import annotations

import json
from typing import Any, Dict

import streamlit as st

from agents.quote_agent import run_quote
from .components import (
    chat_bubble,
    parse_quote_output,
    quote_table,
    render_quote,
)

try:  # pragma: no cover - optional dependency
    from logic.job_parser import parse_prompt
except Exception:  # pragma: no cover
    parse_prompt = None


def _generate(prompt: str) -> Dict[str, Any]:
    """Call the quote agent and parse JSON response."""
    raw = run_quote(prompt)
    data: Dict[str, Any] = json.loads(raw)
    return data


def main() -> None:
    st.set_page_config(page_title="Quote Assistant", layout="wide")
    st.header("Quoting Assistant")

    if "history" not in st.session_state:
        st.session_state.history = []

    col_chat, col_result = st.columns([1, 2])

    with col_chat:
        st.header("Chat History")
        for entry in st.session_state.history:
            chat_bubble(entry["prompt"], user=True)
            chat_bubble(json.dumps(entry["response"], indent=2), user=False)
        prompt = st.text_input("Describe the job", key="prompt_input")
        if st.button("Generate Quote") and prompt.strip():
            response = _generate(prompt.strip())
            parsed = parse_prompt(prompt.strip()) if parse_prompt else None
            st.session_state.history.append(
                {"prompt": prompt.strip(), "response": response, "parsed": parsed}
            )
            st.session_state.prompt_input = ""

    with col_result:
        st.header("Quote")
        if st.session_state.history:
            latest = st.session_state.history[-1]
            render_quote(latest["response"])
            st.subheader("Quote JSON")
            st.json(latest["response"])
            st.subheader("Items")
            quote_table(latest["response"].get("items", []))
            if latest.get("parsed") is not None:
                st.subheader("Parsed Job")
                st.json(latest["parsed"])
        else:
            st.markdown("Enter a job description to generate a quote.")


if __name__ == "__main__":
    main()
