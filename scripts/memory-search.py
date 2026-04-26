import argparse
import os
from dotenv import load_dotenv
from gemma4_ollama.embeddings import embed_text
from gemma4_ollama.memory import search_vectors

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Search memory records.")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    
    args = parser.parse_args()
    
    # Configuration from environment
    embedding_model = os.getenv("EMBEDDING_MODEL", "embeddinggemma:300m-qat-q4_0")
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    vector_db_path = os.getenv("VECTOR_DB_PATH", "data/memory/vectors.sqlite")
    
    print(f"Searching for: {args.query}")
    
    # 1. Embed query
    print(f"Generating embedding for query using {embedding_model}...")
    query_vector = embed_text(args.query, model=embedding_model, host=ollama_host)
    
    # 2. Search SQLite
    results = search_vectors(query_vector, top_k=args.top_k, path=vector_db_path)
    
    print(f"\nFound {len(results)} results:")
    for i, res in enumerate(results, 1):
        print(f"\n{i}. [Score: {res['similarity']:.4f}]")
        print(f"Text: {res['text']}")
        print(f"Memory ID: {res['memory_id']}")

if __name__ == "__main__":
    main()
