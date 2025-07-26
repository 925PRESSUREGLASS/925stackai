"""Reusable Streamlit components for the GUI."""

from __future__ import annotations

import json
from typing import Any, Dict, List

import pandas as pd
import streamlit as st


def parse_quote_output(output: str) -> Dict[str, Any]:
    """Parse JSON string returned by ``run_quote``."""
    return json.loads(output)


def chat_bubble(text: str, user: bool = True) -> None:
    """Render a chat bubble for either the user or the agent."""

    role = "You" if user else "Agent"
    align = "left" if user else "right"
    st.markdown(
        (
            "<div style='text-align:%s; border:1px solid #ccc; padding:6px; "
            "border-radius:4px; margin:4px 0'><b>%s:</b> %s</div>"
        )
        % (align, role, text),
        unsafe_allow_html=True,
    )


def quote_table(items: List[Dict[str, Any]]) -> None:
    """Render a table of quote line items."""

    if not items:
        st.info("No items returned")
        return

    df = pd.DataFrame(items)
    st.table(df)


def render_quote(data: Dict[str, Any]) -> None:
    """Render quote details as JSON and table."""
    st.subheader("JSON")
    st.json(data)
    st.subheader("Breakdown")
    items = data.get("items", [])
    if items:
        st.table(items)
    st.write(f"**Total:** {data.get('total', 0)}")
