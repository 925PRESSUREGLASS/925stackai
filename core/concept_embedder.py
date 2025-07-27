"""Utility for generating and caching text embeddings."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List

try:
    import openai
except Exception:  # pragma: no cover - optional dependency
    openai = None

from sentence_transformers import SentenceTransformer


class ConceptEmbedder:
    """Compute embeddings using OpenAI or a local model with caching."""

    def __init__(self, cache_path: str | Path = "memory/vector_store.json") -> None:
        self.cache_path = Path(cache_path)
        self.cache: Dict[str, List[float]] = {}
        self._model: SentenceTransformer | None = None
        self._load_cache()

    def _load_cache(self) -> None:
        if self.cache_path.exists():
            with open(self.cache_path, "r", encoding="utf-8") as f:
                self.cache = json.load(f)

    def _save_cache(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, ensure_ascii=False)

    def _hf_model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        return self._model

    def embed(self, text: str) -> List[float]:
        """Return embedding vector for ``text``."""
        if text in self.cache:
            return self.cache[text]
        api_key = os.getenv("OPENAI_API_KEY")
        vec: List[float]
        if api_key and openai is not None:
            try:
                resp = openai.Embedding.create(
                    model="text-embedding-ada-002", input=[text]
                )
                vec = resp["data"][0]["embedding"]
            except Exception:
                vec = self._hf_model().encode(text).tolist()
        else:
            vec = self._hf_model().encode(text).tolist()
        self.cache[text] = [float(x) for x in vec]
        self._save_cache()
        return self.cache[text]
