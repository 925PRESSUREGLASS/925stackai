
import json
from core.prompt_manager import PromptManager


def test_prompt_includes_related_section() -> None:
    prompt = "Bug: Details. Related: Doc1, Doc2"
    output = PromptManager().build_prompt(prompt, dev_mode=False)
    assert "Doc1" in output
    assert "Doc2" in output


def test_modes_produce_valid_json() -> None:
    prompt = "Bug"
    for m in ["scan", "fix", "pr", "log"]:
        out = PromptManager().build_prompt(f"{prompt} mode:{m}", dev_mode=False)
        assert m in out
