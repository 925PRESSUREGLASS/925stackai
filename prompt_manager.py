class PromptManager:
    def build_prompt(self, user_prompt: str, dev_mode: bool = False) -> str:
        """Return the full prompt that will be sent to the quoting agent."""
        header = "# Quoting Prompt\n"
        body = user_prompt.strip()
        if dev_mode:
            body += "\n\n[DEV MODE ENABLED]"
        return f"{header}{body}"
