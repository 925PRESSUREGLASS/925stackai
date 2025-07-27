from __future__ import annotations

class GUIAgent:
    """Minimal GUI agent used for CLI chat."""

    def process_user_input(self, message: str, session_state: dict | None = None) -> str:
        return f"Echo: {message}"
