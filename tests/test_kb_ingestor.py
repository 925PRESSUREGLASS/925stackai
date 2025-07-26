from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from logic.kb_ingestor import ingest


def test_ingest_file(tmp_path: Path) -> None:
    # Create a dummy text file
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello world!")
    count = ingest(file_path, str(tmp_path / "vs"))
    assert count == 1


def test_ingest_directory(tmp_path: Path) -> None:
    # Create multiple files in a directory
    dir_path = tmp_path / "docs"
    dir_path.mkdir()
    (dir_path / "a.txt").write_text("A")
    (dir_path / "b.txt").write_text("B")
    count = ingest(dir_path, str(tmp_path / "vs"))
    assert count == 2
