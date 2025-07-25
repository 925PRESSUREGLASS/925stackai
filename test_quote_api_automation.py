import requests
import time

PROMPT = "25 large windows, exterior only, 2nd storey, urgent"
API_URL = "http://localhost:8000/quote"

for i in range(5):
    response = requests.post(API_URL, json={"prompt": PROMPT})
    print(f"Response {i+1}:", response.json())
    time.sleep(1)
