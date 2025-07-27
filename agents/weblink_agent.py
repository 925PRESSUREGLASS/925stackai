from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np

from modular_ai_agent.memory.memory_setup import _get_embeddings

CONFIG_PATH = Path(__file__).parent.parent / "configs" / "weblink.json"
GRAPH_PATH = Path(os.getenv("WEBLINK_GRAPH_PATH", "storage/weblink_graph.json"))


def _load_config() -> Dict[str, Any]:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"top_k": 3}


_config = _load_config()
DEFAULT_TOP_K = int(_config.get("top_k", 3))

_embedder = _get_embeddings()
_nodes: Dict[str, Dict[str, Any]] = {}


def _load_graph() -> None:
    global _nodes
    if GRAPH_PATH.exists():
        with open(GRAPH_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            _nodes = data.get("nodes", {})
    else:
        _nodes = {}


def _save_graph() -> None:
    GRAPH_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump({"nodes": _nodes}, f)


_load_graph()


def index_issue(issue: Dict[str, Any]) -> None:
    """Add ``issue`` to the graph with its embedding."""
    issue_id = str(issue.get("id", len(_nodes) + 1))
    desc = str(issue.get("description", ""))
    emb = _embedder.embed_query(desc)
    _nodes[issue_id] = {"snippet": desc, "embedding": emb}
    _save_graph()


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def query_related(text: str, top_k: int | None = None) -> List[Tuple[str, str]]:
    """Return related node IDs and snippets for ``text``."""
    if top_k is None:
        top_k = DEFAULT_TOP_K
    if not _nodes:
        return []
    query_emb = np.array(_embedder.embed_query(text))
    scores = []
    for node_id, data in _nodes.items():
        emb = np.array(data["embedding"])
        scores.append((node_id, _cosine(query_emb, emb)))
    scores.sort(key=lambda x: x[1], reverse=True)
    result: List[Tuple[str, str]] = []
    for node_id, _ in scores[:top_k]:
        result.append((node_id, _nodes[node_id]["snippet"]))
    return result


__all__ = ["index_issue", "query_related"]
