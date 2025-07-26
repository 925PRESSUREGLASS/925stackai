import requests
import pytest

pytest.skip("manual API test", allow_module_level=True)

def test_quote_api() -> None:
    url = "http://localhost:8000/quote"
    payload = {"prompt": "How much would it cost to replace a window?"}
    response = requests.post(url, json=payload)
    assert response.status_code == 200

if __name__ == "__main__":  # pragma: no cover - manual invocation
    test_quote_api()
