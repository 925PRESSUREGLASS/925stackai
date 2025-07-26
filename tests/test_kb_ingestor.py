from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import tempfile
import os

from modular_ai_agent.memory.memory_setup import get_vectorstore


def test_cli_ingest_and_search() -> None:
    """CLI ingestion writes docs and allows similarity search."""
    with tempfile.TemporaryDirectory() as tmpdir:
        docs_dir = Path(tmpdir) / "docs"
        docs_dir.mkdir()
        (docs_dir / "a.md").write_text("alpha bravo")
        (docs_dir / "b.md").write_text("charlie delta")
        store_path = Path(tmpdir) / "vs"

        env = dict(os.environ)
        env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1])
        subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts" / "ingest.py"), str(docs_dir), "--store", str(store_path)],
            check=True,
            cwd=Path(__file__).resolve().parents[1],
            env=env,
        )

        vs = get_vectorstore(store_path)
        hits = vs.similarity_search("bravo")
        assert hits
