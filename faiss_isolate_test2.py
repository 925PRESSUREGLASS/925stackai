import os
import sys
from pathlib import Path

from langchain_community.embeddings import FakeEmbeddings, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

if __name__ == "__main__":
    print("Testing FAISS vector store with memory_setup logic...")
    try:
        # Use the same logic as _get_embeddings
        if os.getenv("OPENAI_API_KEY"):
            embeddings = OpenAIEmbeddings()
        else:
            embeddings = FakeEmbeddings(size=1536)
        path = Path("faiss_test_store2")
        if (path / "index.faiss").exists():
            print("Loading existing FAISS index...")
            store = FAISS.load_local(
                str(path), embeddings, allow_dangerous_deserialization=True
            )
        else:
            print("Creating new FAISS index...")
            path.mkdir(parents=True, exist_ok=True)
            store = FAISS.from_documents([Document(page_content="dummy")], embeddings)
            store.save_local(str(path))
        # Add a document and save
        store.add_documents([Document(page_content="hello world")])
        store.save_local(str(path))
        print("FAISS vector store add/save successful.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    print("Done.")
