import requests

response = requests.post(
    "http://localhost:12434/engines/llama.cpp/v1/chat/completions",
    json={
        "model": "ai/gemma4:E2B",
        "messages": [{"role": "user", "content": "Explain what Docker is in one sentence."}]
    }
)
print(response.json())