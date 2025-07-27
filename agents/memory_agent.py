from __future__ import annotations

class MemoryAgent:
    """Simple in-memory storage for chat history."""

    def __init__(self) -> None:
        self.history: list[str] = []

    def add(self, role: str, text: str) -> None:
        self.history.append(f"{role}: {text}")

    def recall(self) -> str:
        return "\n".join(self.history)

    def clear(self) -> None:
        self.history.clear()
