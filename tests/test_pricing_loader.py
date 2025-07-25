from pathlib import Path
import tempfile

from modular_ai_agent.memory.load_pricing import ingest
from modular_ai_agent.memory.memory_setup import get_vectorstore


def test_ingest_and_query() -> None:
    # copy sample CSV into a tmp dir so we don't pollute repo store
    tmp = tempfile.TemporaryDirectory()
    csv_path = Path(tmp.name) / "pricing.csv"
    csv_path.write_text("material,price_per_m2,currency\nepoxy,42,USD\n")
    store_path = Path(tmp.name) / "vs"

    # ingest
    rows = ingest(str(csv_path), str(store_path))
    assert rows == 1

    # simple similarity query
    vs = get_vectorstore(str(store_path))
    docs = vs.similarity_search("epoxy price", k=1)
    assert docs and "42" in docs[0].page_content
