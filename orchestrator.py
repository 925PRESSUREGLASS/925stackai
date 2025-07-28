"""Orchestrates the flow Prompt → Agent → Response."""

from pathlib import Path

from prompt_manager import PromptManager
from agents.quoting_agent import QuotingAgent

_LOG_DIR = Path(__file__).parent / "logs"
_LOG_DIR.mkdir(exist_ok=True)


class Orchestrator:
    def __init__(self) -> None:
        self.prompt_mgr: PromptManager = PromptManager()
        self.agent: QuotingAgent = QuotingAgent()

    def run(self, user_prompt: str, *, dev_mode: bool = False) -> str:
        prompt = self.prompt_mgr.build_prompt(user_prompt, dev_mode=dev_mode)
        response = self.agent.run(prompt)

        # very simple log
        log_file = _LOG_DIR / "run_history.log"
        with log_file.open("a", encoding="utf-8", errors="ignore") as fh:
            fh.write(f"PROMPT: {user_prompt}\nRESPONSE: {response}\n\n")
        return response
