from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Document:
    page_content: str
    metadata: Dict[str, Any] | None = None
