"""Utility helpers for loading human‑authored specs and their test cases."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict

_ROOT = Path(__file__).resolve().parent.parent


def _spec_dir() -> Path:
    return _ROOT / "specs"


def load_spec(name: str) -> str:
    """Return raw markdown spec content for *name*."""
    path = _spec_dir() / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf‑8")


def load_tests(name: str) -> Dict:
    """Return the rules/tests dictionary for *name* from validation.json."""
    path = _spec_dir() / "validation.json"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf‑8") as fh:
        data = json.load(fh)
    return data.get(name, {})
