from agents.quote_agent import QuoteAgent
from agents.spec_guard import grade_response
from core.spec_loader import load_tests
import json
from pathlib import Path

_LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
_LOG_DIR.mkdir(exist_ok=True)

class Orchestrator:
    def __init__(self):
        self.agent = QuoteAgent()

    def run(self, prompt: str):
        response = self.agent(prompt)

        # Evaluate response
        test_block = load_tests("quote_generation")
        rules = test_block.get("rules", {})
        eval_summary = grade_response(prompt, response, rules)

        # Persist log
        log_path = _LOG_DIR / "eval_log.json"
        history = json.loads(log_path.read_text("utf-8")) if log_path.exists() else []
        history.append({"prompt": prompt, "response": response, **eval_summary})
        log_path.write_text(json.dumps(history, indent=2), encoding="utf-8")

        return response, eval_summary
