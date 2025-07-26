import json
from typing import Any, Dict
import streamlit as st


def parse_quote_output(output: str) -> Dict[str, Any]:
    """Parse JSON string returned by ``run_quote``."""
    return json.loads(output)


def render_quote(data: Dict[str, Any]) -> None:
    """Render quote details as JSON and table."""
    st.subheader("JSON")
    st.json(data)
    st.subheader("Breakdown")
    items = data.get("items", [])
    if items:
        st.table(items)
    st.write(f"**Total:** {data.get('total', 0)}")
