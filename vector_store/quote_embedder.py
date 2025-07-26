
from typing import List, Dict, Any
import os
import json
from langchain.embeddings import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

class QuoteVectorStore:
    def __init__(self, data_path: str = "data/quotes.jsonl", persist_dir: str = "vector_store/chroma_index"):
        self.data_path = data_path
        self.persist_dir = persist_dir
        self.client = chromadb.PersistentClient(path=self.persist_dir, settings=Settings(allow_reset=True))
        self.collection = self.client.get_or_create_collection("quotes")
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def build_index(self) -> None:
        if not os.path.exists(self.data_path):
            return
        with open(self.data_path, "r", encoding="utf-8") as f:
            quotes = [json.loads(line) for line in f if line.strip()]
        # Clear and re-add all
        self.collection.delete(where={})
        for i, quote in enumerate(quotes):
            content = quote.get("content") or quote.get("prompt") or str(quote)
            metadata = {"quote_id": quote.get("id", str(i)), **{k: v for k, v in quote.items() if k != "content"}}
            self.collection.add(
                documents=[content],
                metadatas=[metadata],
                ids=[str(metadata["quote_id"])]
            )

    def query(self, prompt: str, top_k: int = 3) -> List[Dict[str, Any]]:
        # Compute embedding using HuggingFaceEmbeddings (offline)
        embedding = self.embedding_model.embed_query(prompt)
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )
        matches = []
        docs = results.get("documents")
        metas = results.get("metadatas")
        ids = results.get("ids")
        if docs and metas and ids:
            docs = docs[0]
            metas = metas[0]
            ids = ids[0]
            for doc, meta, id_ in zip(docs, metas, ids):
                matches.append({
                    "content": doc,
                    "metadata": meta
                })
        return matches
