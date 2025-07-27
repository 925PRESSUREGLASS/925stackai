"""Simple in-memory directed graph with JSON persistence."""

from __future__ import annotations

import json
import os
from typing import Any, Dict


class Graph:
    """Directed graph stored as adjacency dict."""

    def __init__(self, path: str = "memory/graph.json") -> None:
        self.path = path
        self._nodes: set[str] = set()
        self._edges: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self._load()

    # Internal helpers -----------------------------------------------------
    def _load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._nodes = set(data.get("nodes", []))
                self._edges = data.get("edges", {})
            except Exception:
                self._nodes = set()
                self._edges = {}
        else:
            self._nodes = set()
            self._edges = {}

    def _save(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        data = {"nodes": sorted(self._nodes), "edges": self._edges}
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # Public API -----------------------------------------------------------
    def add_node(self, node_id: str) -> None:
        """Add a node to the graph."""
        if node_id not in self._nodes:
            self._nodes.add(node_id)
            self._edges.setdefault(node_id, {})
            self._save()

    def add_link(
        self, source: str, target: str, metadata: Dict[str, Any] | None = None
    ) -> None:
        """Create a directed edge from ``source`` to ``target`` with ``metadata``."""
        if metadata is None:
            metadata = {}
        self.add_node(source)
        self.add_node(target)
        self._edges[source][target] = metadata
        self._save()

    def query_links(self, node_id: str) -> Dict[str, Dict[str, Any]]:
        """Return all outgoing links from ``node_id``."""
        return self._edges.get(node_id, {})


__all__ = ["Graph"]
