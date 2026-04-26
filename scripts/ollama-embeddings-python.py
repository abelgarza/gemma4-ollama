import argparse
import os
from dotenv import load_dotenv
from gemma4_ollama.embeddings import embed_text

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Generate embeddings using Ollama Python library.")
    parser.add_argument("--prompt", default="Hola mundo", help="Text to embed")
    parser.add_argument("--model", default=os.getenv("EMBEDDING_MODEL", "embeddinggemma:300m-qat-q4_0"), help="Embedding model")
    parser.add_argument("--host", default=os.getenv("OLLAMA_HOST", "http://localhost:11434"), help="Ollama host")
    
    args = parser.parse_args()
    
    print(f"Generating embedding for: '{args.prompt}' using {args.model}...")
    vector = embed_text(args.prompt, model=args.model, host=args.host)
    
    print(f"Embedding size: {len(vector)}")
    print(f"Vector (first 5 values): {vector[:5]}...")

if __name__ == "__main__":
    main()
