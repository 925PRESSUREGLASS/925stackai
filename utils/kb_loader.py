from pathlib import Path
from typing import Dict, List, Tuple

def load_kb(folder: str = "925stackai-KB") -> Dict[str, str]:
    """Load all Markdown files from the KB folder into a dict."""
    kb = {}
    for md_file in Path(folder).rglob("*.md"):
        kb[md_file.stem] = md_file.read_text(encoding="utf-8")
    return kb

def search_kb(kb: Dict[str, str], query: str) -> List[Tuple[str, str]]:
    """Simple keyword search over the KB content."""
    results = []
    for title, content in kb.items():
        if query.lower() in content.lower():
            results.append((title, content))
    return results
