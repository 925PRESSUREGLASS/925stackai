from typing import Optional


class Llama3QuoteModel:
    """Lightweight stand-in for the real Llama 3 model."""

    def __init__(self, *args, **kwargs) -> None:
        # Accept arbitrary args for API compatibility
        pass

    def generate_text(self, prompt: str, max_new_tokens: int = 64) -> str:
        """Return a dummy response used to trigger rule-based fallback."""
        return "{}"

    def chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        max_new_tokens: int = 64,
    ) -> str:
        """Return a basic echo-style response."""
        return self.generate_text(user_message, max_new_tokens=max_new_tokens)
