"""Simple directed graph stored in-memory and persisted to JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class Graph:
    """Dictionary-of-dictionaries directed graph."""

    def __init__(self, path: str | Path = "memory/graph.json") -> None:
        self.path = Path(path)
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self._load()

    def _load(self) -> None:
        if self.path.exists():
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.nodes = data.get("nodes", {})
            self.edges = data.get("edges", {})

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump({"nodes": self.nodes, "edges": self.edges}, f, ensure_ascii=False)

    def add_node(self, node_id: str, **attrs: Any) -> None:
        """Add ``node_id`` with optional ``attrs``."""
        if node_id not in self.nodes:
            self.nodes[node_id] = {}
        self.nodes[node_id].update(attrs)
        self._save()

    def add_link(self, src: str, dst: str, **attrs: Any) -> None:
        """Add directed edge from ``src`` to ``dst`` with ``attrs``."""
        self.edges.setdefault(src, {})[dst] = attrs
        self._save()

    def query_links(self, node_id: str) -> Dict[str, Dict[str, Any]]:
        """Return outgoing links from ``node_id``."""
        return self.edges.get(node_id, {})
