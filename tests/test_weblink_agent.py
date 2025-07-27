import importlib
import os
from pathlib import Path


def test_index_and_query_roundtrip(tmp_path: Path) -> None:
    os.environ["WEBLINK_GRAPH_PATH"] = str(tmp_path / "graph.json")
    module = importlib.import_module("agents.weblink_agent")
    importlib.reload(module)

    issue = {"id": "1", "description": "leaky faucet under sink"}
    module.index_issue(issue)
    results = module.query_related("faucet")

    assert results
    first_id, snippet = results[0]
    assert first_id == "1"
    assert "faucet" in snippet
