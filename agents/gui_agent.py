from __future__ import annotations

try:  # Optional segment detection module
    from logic.segment_detect import detect_customer_segment
except Exception:  # pragma: no cover - fallback when module missing
    def detect_customer_segment(_: str) -> str:
        return "unknown"

class GUIAgent:
    """Minimal GUI agent used for CLI chat."""

    def process_user_input(self, message: str, session_state: dict | None = None) -> str:
        if session_state is not None and "segment" not in session_state:
            session_state["segment"] = detect_customer_segment(message)
        return f"Echo: {message}"
