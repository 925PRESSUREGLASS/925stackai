import sys
import types

# stub quote_agent to avoid heavy deps
fake_agent = types.ModuleType("agents.quote_agent")


def run_quote(prompt: str) -> str:  # type: ignore[return-type]
    return '{"customer": "Test", "items": [], "total": 0.0}'


fake_agent.run_quote = run_quote
sys.modules["agents.quote_agent"] = fake_agent

from gui.app import main


def test_main_runs() -> None:
    main()
