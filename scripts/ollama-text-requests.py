import os
import requests
import json

url = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/") + "/api/generate"
model = os.getenv("OLLAMA_MODEL", "gemma4:latest")

payload = {
    "model": model,
    "prompt": "Hola",
    "stream": False
}

response = requests.post(url, json=payload)

# Comprobar si la petición fue exitosa
if response.status_code == 200:
    data = response.json()
    print(data['response'])
else:
    print(f"Error: {response.status_code}")
    print(response.text)
