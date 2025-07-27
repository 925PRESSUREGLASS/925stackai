#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path
import readline  # noqa: F401 -- enable history keys

from agents import GUIAgent, MemoryAgent

try:  # Optional quoting agent
    from agents.quote_agent import QuoteAgent as QuotingAgent
except Exception:  # pragma: no cover - optional dependency
    QuotingAgent = None

LOG_PATH = Path("logs/chat_log.txt")


def gui_agent(message: str) -> str:
    """Return a simple GUI agent response."""
    return GUIAgent().process_user_input(message, {})


def chat_loop() -> None:
    """Run a minimal interactive chat."""

    gui = GUIAgent()
    memory = MemoryAgent()
    quote = QuotingAgent() if QuotingAgent else None

    help_text = (
        "Available commands:\n"
        "/help   Show this message\n"
        "/clear  Forget conversation history\n"
        "/recall Show conversation history\n"
        "/quote  Generate a quote using the quoting agent\n"
        "exit    Quit the chat"
    )

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    while True:
        try:
            user = input(" > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user:
            continue
        if user.lower() in {"exit", "quit"}:
            break
        if user == "/help":
            print(help_text)
            continue
        if user == "/clear":
            memory.clear()
            print("Memory cleared.")
            continue
        if user == "/recall":
            print(memory.recall() or "(no history)")
            continue
        if user.startswith("/quote"):
            prompt = user[len("/quote") :].strip() or "quote"
            reply = quote(prompt) if quote else "Quoting agent unavailable."
        elif user.startswith("/"):
            print("Unknown command.")
            continue
        else:
            reply = gui.process_user_input(user, {})

        memory.add("user", user)
        memory.add("assistant", reply)
        print(reply)
        with LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(f"User: {user}\nAssistant: {reply}\n")


if __name__ == "__main__":  # pragma: no cover - manual use
    chat_loop()
