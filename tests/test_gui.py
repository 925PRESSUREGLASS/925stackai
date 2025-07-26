from __future__ import annotations

from gui.components import parse_quote_output


def test_parse_quote_output() -> None:
    json_str = (
        '{"customer": "Bob", "items": [{"service": "window", "qty": 1, '
        '"unit_price": 2, "size": "", "subtotal": 2}], "total": 2}'
    )
    data = parse_quote_output(json_str)
    assert data["customer"] == "Bob"
    assert data["total"] == 2
    assert data["items"][0]["service"] == "window"


"""Simple import test for the GUI."""

import importlib
import sys
import types


class FakeSessionState(dict):
    """Minimal stand-in for ``st.session_state`` used in tests."""

    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value


def test_gui_main_runs() -> None:
    """Ensure the Streamlit app's main function can be executed."""

    # Fake quote agent
    fake_agent = types.ModuleType("agents.quote_agent")
    fake_agent.run_quote = lambda prompt: "{}"
    sys.modules["agents.quote_agent"] = fake_agent

    # Fake streamlit module
    fake_streamlit = types.ModuleType("streamlit")

    def noop(*args, **kwargs):
        return ""

    def columns(spec):
        class Col:
            def __getattr__(self, name):
                return noop

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

        return [Col(), Col()]

    fake_streamlit.set_page_config = noop
    fake_streamlit.columns = columns
    fake_streamlit.header = noop
    fake_streamlit.text_input = lambda *a, **k: ""
    fake_streamlit.button = lambda *a, **k: False
    fake_streamlit.subheader = noop
    fake_streamlit.json = noop
    fake_streamlit.markdown = noop
    fake_streamlit.table = noop
    fake_streamlit.info = noop
    fake_streamlit.session_state = FakeSessionState({"history": []})

    sys.modules["streamlit"] = fake_streamlit

    gui_app = importlib.import_module("gui.app")
    importlib.reload(gui_app)
    gui_app.main()
