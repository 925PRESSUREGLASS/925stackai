"""Manual automation script (skipped in CI)."""

import time

import pytest
import requests

pytest.skip("manual script", allow_module_level=True)

PROMPT = "25 large windows, exterior only, 2nd storey, urgent"
API_URL = "http://localhost:8000/quote"

for i in range(5):  # pragma: no cover - manual loop
    response = requests.post(API_URL, json={"prompt": PROMPT})
    print(f"Response {i+1}:", response.json())
    time.sleep(1)
