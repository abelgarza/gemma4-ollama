import requests
import json

url = "http://localhost:11434/api/generate"

payload = {
    "model": "gemma4:latest",
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
