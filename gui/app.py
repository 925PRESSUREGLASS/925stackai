from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import streamlit as st
from agents.quote_agent import run_quote

try:
    from logic import job_parser
except Exception:  # pragma: no cover - optional dependency
    job_parser = None

from .components import chat_bubble, quote_table


def main() -> None:
    """Run the Streamlit quote app."""
    st.set_page_config(page_title="Quote Generator")

    history: List[Dict[str, Any]] = st.session_state.setdefault("history", [])

    col_chat, col_output = st.columns(2)

    with col_chat:
        st.header("Conversation")
        for entry in history:
            chat_bubble("user", entry["prompt"])
            chat_bubble("assistant", json.dumps(entry["quote"], indent=2))

        prompt: str = st.text_input("Describe the job", key="prompt")
        if st.button("Generate Quote") and prompt:
            quote_json = run_quote(prompt)
            quote_data: Dict[str, Any] = json.loads(quote_json)
            parsed: Optional[Dict[str, Any]] = None
            if job_parser is not None and hasattr(job_parser, "parse_prompt"):
                parsed = job_parser.parse_prompt(prompt)
            history.append({"prompt": prompt, "quote": quote_data, "parsed": parsed})
            st.session_state.prompt = ""

    with col_output:
        st.header("Quote Result")
        if history:
            latest = history[-1]
            st.subheader("JSON")
            st.json(latest["quote"])
            st.subheader("Items")
            quote_table(latest["quote"].get("items", []))
            if latest.get("parsed") is not None:
                st.subheader("Parsed Job")
                st.json(latest["parsed"])


if __name__ == "__main__":
    main()
