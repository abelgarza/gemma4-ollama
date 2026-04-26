import os
import argparse
from dotenv import load_dotenv
from gemma4_ollama.memory import init_db

def main():
    parser = argparse.ArgumentParser(description="Hard reset the memory storage.")
    parser.add_argument("--force", action="store_true", help="Force reset without asking for confirmation")
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    memory_path = os.getenv("MEMORY_JSONL_PATH", "data/memory/memory.jsonl")
    vector_db_path = os.getenv("VECTOR_DB_PATH", "data/memory/vectors.sqlite")
    
    print("WARNING: This will permanently delete your memory files:")
    print(f"  - {memory_path}")
    print(f"  - {vector_db_path}")
    
    if not args.force:
        confirm = input("\nAre you sure you want to completely wipe the memory? (y/N): ")
        if confirm.lower() != 'y':
            print("Reset cancelled.")
            return

    # Delete JSONL
    if os.path.exists(memory_path):
        os.remove(memory_path)
        print(f"Deleted {memory_path}")
    else:
        print(f"File not found, skipping {memory_path}")

    # Delete SQLite DB
    if os.path.exists(vector_db_path):
        os.remove(vector_db_path)
        print(f"Deleted {vector_db_path}")
    else:
        print(f"File not found, skipping {vector_db_path}")

    # Ensure directories exist
    os.makedirs(os.path.dirname(memory_path), exist_ok=True)
    os.makedirs(os.path.dirname(vector_db_path), exist_ok=True)

    # Initialize new database structure
    print("\nInitializing new empty vector database...")
    init_db(path=vector_db_path)
    
    # Touch the JSONL file to ensure it exists
    open(memory_path, 'a').close()
    
    print("Memory has been successfully reset.")

if __name__ == "__main__":
    main()
