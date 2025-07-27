from cli_chat import gui_agent


def test_gui_agent_response() -> None:
    resp = gui_agent("hello")
    assert isinstance(resp, str)
