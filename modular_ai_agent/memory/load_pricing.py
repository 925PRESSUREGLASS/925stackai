"""
Helper that loads a pricing CSV into the existing FAISS vector store.

•  Uses the Pydantic `PricingRecord` model for validation.
•  Adds each row as a LangChain Document with `metadata={"doc_type": "pricing"}`.
•  Re-uses `get_vectorstore()` from memory_setup.
•  Provides a CLI:  python -m modular_ai_agent.memory.load_pricing data/pricing_rules.csv
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import List

from pydantic import BaseModel, PositiveFloat, ValidationError
from langchain.schema import Document

from .memory_setup import get_vectorstore


class PricingRecord(BaseModel):
    material: str
    price_per_m2: PositiveFloat
    currency: str = "USD"


def ingest(csv_path: str, store_path: str = "memory/vector_store") -> int:
    """Read the CSV, validate rows, and add them to the FAISS store.

    Returns the number of rows successfully ingested.
    """
    vs = get_vectorstore(store_path)
    added: List[Document] = []

    with Path(csv_path).open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                rec = PricingRecord(**row)  # type: ignore[arg-type]
            except ValidationError as err:
                print(f"⚠️  Skipping invalid row {row}: {err}", file=sys.stderr)
                continue

            added.append(
                Document(
                    page_content=f"{rec.material} costs {rec.price_per_m2} {rec.currency} per m².",
                    metadata={
                        "material": rec.material,
                        "price_per_m2": rec.price_per_m2,
                        "currency": rec.currency,
                        "doc_type": "pricing",
                    },
                )
            )

    if added:
        vs.add_documents(added)
        vs.save_local(str(Path(store_path)))
    print(f"✅  Ingested {len(added)} pricing records into {store_path}")
    return len(added)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(
            "Usage: python -m modular_ai_agent.memory.load_pricing <csv_path> [store_path]"
        )
    ingest(*sys.argv[1:])
