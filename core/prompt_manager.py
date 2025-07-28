

# Added spec-driven prompting
import os
import json
from core.spec_loader import load_spec, load_tests

class PromptManager:
    SPEC_NAME = "quote_generation"

    def build_prompt(self, user_prompt: str, dev_mode: bool = False) -> str:
        """Assemble the full prompt sent to the quoting agent with spec injection."""
        spec_md = load_spec(self.SPEC_NAME)
        base_prompt = f"""# Specification\n{spec_md}\n\n# User Prompt\n{user_prompt.strip()}"""

        if dev_mode:
            test_block = load_tests(self.SPEC_NAME)
            tests = test_block.get("tests", [])
            rules = test_block.get("rules", {})
            if tests:
                base_prompt += "\n\n# Dev Mode – Test Prompts\n"
                for i, t in enumerate(tests, 1):
                    base_prompt += f"\n## Test {i}: {t['prompt']}\nExpected contains: {t.get('expected_contains', '')}\n"
            if rules:
                base_prompt += f"\n\n# Dev Mode – Rules\n{json.dumps(rules, indent=2)}"
        return base_prompt
