from __future__ import annotations

import argparse
from typing import Any, Dict, List

from agents.gui_agent import GUIAgent
from agents.quoting_agent import QuotingAgent
from core.prompt_manager import build_prompt


class Orchestrator:
    """Coordinate agents for processing issues."""

    def __init__(self) -> None:
        self.gui = GUIAgent()
        self.quoter = QuotingAgent()
        self.session_state: Dict[str, Any] = {}

    def process_issues(self, issues: List[Dict[str, Any]], *, dry_run: bool = False) -> None:
        for issue in issues:
            self.gui.process_user_input(issue.get("description", ""), self.session_state)
            quote = self.quoter.generate_quote(issue.get("description", ""), self.session_state)
            prompt = build_prompt(issue, mode="scan")
            if not dry_run:
                # Placeholder for PR push logic
                pass
            issue["quote"] = quote
            issue["prompt"] = prompt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("issues", nargs="*", help="Issue descriptions")
    parser.add_argument("--dry-run", action="store_true", help="Skip PR push")
    args = parser.parse_args()

    orch = Orchestrator()
    issues = [{"description": desc, "title": desc} for desc in args.issues]
    orch.process_issues(issues, dry_run=args.dry_run)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
