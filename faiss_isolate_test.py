import sys

from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

if __name__ == "__main__":
    print("Testing FAISS vector store creation...")
    try:
        embeddings = FakeEmbeddings(size=1536)
        store = FAISS.from_documents([Document(page_content="dummy")], embeddings)
        store.save_local("faiss_test_store")
        print("FAISS vector store created and saved successfully.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    print("Done.")
