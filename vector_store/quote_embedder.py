
import json
import os
from typing import Any, Dict, List, Optional

from langchain_community.embeddings import HuggingFaceEmbeddings
try:
    from langchain_community.embeddings import OpenAIEmbeddings
except ImportError:
    OpenAIEmbeddings = None

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions


class QuoteVectorStore:


    def count(self) -> int:
        """Return the number of vectors in the collection."""
        try:
            info = self.collection.count()
            return info if isinstance(info, int) else 0
        except Exception:
            return 0
    def __init__(
        self,
        data_path: str = "data/quotes.jsonl",
        persist_dir: str = "vector_store/chroma_index",
        embedding_type: Optional[str] = None,
    ):
        self.data_path = data_path
        self.persist_dir = persist_dir
        self.client = chromadb.PersistentClient(
            path=self.persist_dir, settings=Settings(allow_reset=True)
        )
        self.collection = self.client.get_or_create_collection("quotes")
        # Choose embedding model: 'huggingface' (default, local) or 'openai' (API)
        embedding_type = (
            embedding_type
            or os.environ.get("QUOTE_EMBEDDING_TYPE", "huggingface").lower()
        )
        if embedding_type == "openai" and OpenAIEmbeddings is not None:
            self.embedding_model = OpenAIEmbeddings()
        else:
            # Use langchain_huggingface for HuggingFaceEmbeddings (future-proof)
            import sentence_transformers
            model_name = "all-MiniLM-L6-v2"
            try:
                model = sentence_transformers.SentenceTransformer(model_name)
                model.to("cpu")
                self.embedding_model = HuggingFaceEmbeddings(model_name=model_name, model_kwargs={"device": "cpu"})
            except Exception as e:
                print(f"Error loading HuggingFaceEmbeddings: {e}")
                raise

    def build_index(self) -> None:
        if not os.path.exists(self.data_path):
            return
        with open(self.data_path, "r", encoding="utf-8") as f:
            quotes = [json.loads(line) for line in f if line.strip()]
        # Clear and re-add all (delete all docs by IDs)
        try:
            all_docs = self.collection.get()
            all_ids = all_docs.get("ids", [])
            if all_ids:
                self.collection.delete(ids=all_ids)
        except Exception:
            pass
        for i, quote in enumerate(quotes):
            content = quote.get("content") or quote.get("prompt") or str(quote)
            metadata = {"quote_id": quote.get("id", str(i))}
            for k, v in quote.items():
                if k == "content":
                    continue
                # Serialize non-primitive types
                if isinstance(v, (dict, list)):
                    metadata[k] = json.dumps(v, ensure_ascii=False)
                else:
                    metadata[k] = v
            self.collection.add(
                documents=[content],
                metadatas=[metadata],
                ids=[str(metadata["quote_id"])],
            )

    def query(self, prompt: str, top_k: int = 3) -> List[Dict[str, Any]]:
        # Compute embedding using HuggingFaceEmbeddings (offline)
        embedding = self.embedding_model.embed_query(prompt)
        results = self.collection.query(query_embeddings=[embedding], n_results=top_k)
        matches = []
        docs = results.get("documents")
        metas = results.get("metadatas")
        ids = results.get("ids")
        if docs and metas and ids:
            docs = docs[0]
            metas = metas[0]
            ids = ids[0]
            for doc, meta, id_ in zip(docs, metas, ids):
                matches.append({"content": doc, "metadata": meta})
        return matches
