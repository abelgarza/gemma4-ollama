import argparse
import uuid
import os
from dotenv import load_dotenv
from audio_gemma4_ollama.memory import append_memory
from audio_gemma4_ollama.embeddings import embed_text
from audio_gemma4_ollama.vector_store import init_db, upsert_vector

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Add a memory record.")
    parser.add_argument("--text", required=True, help="Text to remember")
    parser.add_argument("--kind", required=True, help="Kind of memory")
    parser.add_argument("--source", required=True, help="Source of memory")
    parser.add_argument("--tag", action="append", help="Tags for the memory")
    parser.add_argument("--confidence", type=float, default=1.0, help="Confidence score")
    
    args = parser.parse_args()
    
    # Configuration from environment
    embedding_model = os.getenv("EMBEDDING_MODEL", "embeddinggemma:300m-qat-q4_0")
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    memory_path = os.getenv("MEMORY_JSONL_PATH", "data/memory/memory.jsonl")
    vector_db_path = os.getenv("VECTOR_DB_PATH", "data/memory/vectors.sqlite")
    
    memory_id = str(uuid.uuid4())
    tags = args.tag if args.tag else []
    
    record = {
        "id": memory_id,
        "kind": args.kind,
        "text": args.text,
        "source": args.source,
        "tags": tags,
        "confidence": args.confidence,
        "metadata": {}
    }
    
    print(f"Adding memory: {args.text[:50]}...")
    
    # 1. Append to JSONL
    append_memory(record, path=memory_path)
    
    # 2. Embed text
    print(f"Generating embedding using {embedding_model}...")
    vector = embed_text(args.text, model=embedding_model, host=ollama_host)
    
    # 3. Store in SQLite
    print(f"Storing in vector store: {vector_db_path}")
    init_db(path=vector_db_path)
    upsert_vector(memory_id, vector, args.text, record["metadata"], path=vector_db_path)
    
    print(f"Successfully added memory {memory_id}")

if __name__ == "__main__":
    main()
