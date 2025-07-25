def _loader_for(path: Path) -> Any:
def main() -> None:
#!/usr/bin/env python3
"""
CLI helper that ingests files or folders into the FAISS vector store.
"""

from logic.kb_ingestor import ingest_cli

if __name__ == "__main__":
    ingest_cli()
