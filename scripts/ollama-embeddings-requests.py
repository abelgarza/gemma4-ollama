import requests
import json
import argparse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Generate embeddings using Ollama HTTP API (requests).")
    parser.add_argument("--prompt", default="Hola mundo", help="Text to embed")
    parser.add_argument("--model", default=os.getenv("EMBEDDING_MODEL", "embeddinggemma:300m-qat-q4_0"), help="Embedding model")
    parser.add_argument("--url", default=f"{os.getenv('OLLAMA_HOST', 'http://localhost:11434')}/api/embeddings", help="Ollama embeddings API URL")
    
    args = parser.parse_args()

    payload = {
        "model": args.model,
        "prompt": args.prompt
    }

    print(f"Post to: {args.url}")
    response = requests.post(args.url, json=payload)

    if response.status_code == 200:
        data = response.json()
        vector = data.get('embedding', [])
        print(f"Embedding size: {len(vector)}")
        print(f"Vector (first 5 values): {vector[:5]}...")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    main()
