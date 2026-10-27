import os
import ollama
from dotenv import load_dotenv

load_dotenv()
from typing import List

def embed_text(
    text: str, 
    model: str | None = None, 
    host: str | None = None
) -> List[float]:
    """
    Produce embeddings for the given text using Ollama.
    """
    client = ollama.Client(host=host or os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    response = client.embeddings(model=model or os.getenv("EMBEDDING_MODEL", "embeddinggemma:300m-qat-q4_0"), prompt=text)
    return response.get("embedding", [])
