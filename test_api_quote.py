import requests

def test_quote_api():
    url = "http://localhost:8000/quote"
    payload = {"prompt": "How much would it cost to replace a window?"}
    response = requests.post(url, json=payload)
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

if __name__ == "__main__":
    test_quote_api()
