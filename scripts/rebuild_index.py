#!/usr/bin/env python3
"""Rebuild the FAISS vector index from a directory of docs."""

from __future__ import annotations

import argparse
from pathlib import Path

from logic.kb_ingestor import ingest


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild FAISS index")
    parser.add_argument("--input", type=Path, required=True, help="Docs folder")
    parser.add_argument("--store", type=Path, required=True, help="Vector store path")
    args = parser.parse_args()

    count = ingest(args.input, str(args.store))
    print(f"\u2705 Indexed {count} document chunks into {args.store}")


if __name__ == "__main__":
    main()
