from __future__ import annotations

"""Streamlit front end for generating quotes."""

import json
from typing import Any, Dict

import streamlit as st

from agents.quote_agent import run_quote

try:  # pragma: no cover - optional dependency
    from logic.job_parser import parse_prompt
except Exception:  # pragma: no cover
    parse_prompt = None

from .components import chat_bubble, quote_table


def _generate(prompt: str) -> Dict[str, Any]:
    """Call the quote agent and parse JSON response."""
    raw = run_quote(prompt)
    data: Dict[str, Any] = json.loads(raw)
    return data


def main() -> None:
    """Entry point for the Streamlit app."""

    st.set_page_config(page_title="Window Cleaning Quotes")

    if "history" not in st.session_state:
        st.session_state.history = []

    col_chat, col_result = st.columns([1, 2])

    with col_chat:
        st.header("Chat History")
        for entry in st.session_state.history:
            chat_bubble(entry["prompt"], user=True)
            chat_bubble(json.dumps(entry["response"], indent=2), user=False)

    with col_result:
        st.header("Quote Generator")
        prompt = st.text_input("Describe the job", key="prompt")
        if st.button("Generate Quote") and prompt:
            response = _generate(prompt)
            parsed = parse_prompt(prompt) if parse_prompt else None
            st.session_state.history.append(
                {"prompt": prompt, "response": response, "parsed": parsed}
            )

        if st.session_state.history:
            latest = st.session_state.history[-1]
            st.subheader("Quote JSON")
            st.json(latest["response"])
            st.subheader("Items")
            quote_table(latest["response"].get("items", []))
            if latest.get("parsed") is not None:
                st.subheader("Parsed Job")
                st.json(latest["parsed"])


if __name__ == "__main__":  # pragma: no cover
    main()

