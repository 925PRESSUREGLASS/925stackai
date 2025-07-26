from __future__ import annotations

from typing import Any, Dict, List

import streamlit as st


def chat_bubble(role: str, content: str) -> None:
    """Render a chat message bubble."""
    with st.chat_message(role):
        st.markdown(content)


def quote_table(items: List[Dict[str, Any]]) -> None:
    """Render a table showing quote line items."""
    if not items:
        st.write("No items")
        return
    st.table(items)
