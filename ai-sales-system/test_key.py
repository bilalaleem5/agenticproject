import os
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("OPENROUTER_KEY")
print(f"Testing key: {key[:10]}...")

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
}
data = {
    "model": "meta-llama/llama-3.3-70b-instruct",
    "messages": [{"role": "user", "content": "Say hello"}]
}
r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
print(f"Status Code: {r.status_code}")
print(f"Response: {r.text}")
