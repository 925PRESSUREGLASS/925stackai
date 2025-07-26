import json
from pathlib import Path
from typing import Dict, Any, List

STORE_PATH = Path(__file__).parent.parent / "data" / "quotes.jsonl"
STORE_PATH.parent.mkdir(parents=True, exist_ok=True)


class JobStore:
    def __init__(self, path: Path = STORE_PATH):
        self.path = path

    def save(self, record: Dict[str, Any]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

    def list_all(self) -> List[Dict[str, Any]]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as f:
            return [json.loads(line) for line in f]
