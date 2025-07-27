"""Text embedding helper with simple JSON cache."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List

_CACHE_PATH = Path("memory/vector_store.json")
_cache: Dict[str, List[float]] | None = None
_model = None


def _load_cache() -> Dict[str, List[float]]:
    global _cache
    if _cache is None:
        if _CACHE_PATH.exists():
            with open(_CACHE_PATH, "r", encoding="utf-8") as f:
                _cache = json.load(f)
        else:
            _cache = {}
    return _cache


def _save_cache() -> None:
    if _cache is None:
        return
    _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(_cache, f, indent=2)


def _embed_openai(text: str) -> List[float]:
    import openai

    response = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
    return response["data"][0]["embedding"]


def _embed_local(text: str) -> List[float]:
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    vector = _model.encode(text)
    return vector.tolist()


def embed(text: str) -> List[float]:
    """Return embedding for ``text`` using OpenAI if available."""

    cache = _load_cache()
    if text in cache:
        return cache[text]

    if os.getenv("OPENAI_API_KEY"):
        vec = _embed_openai(text)
    else:
        vec = _embed_local(text)

    cache[text] = vec
    _save_cache()
    return vec


__all__ = ["embed"]
