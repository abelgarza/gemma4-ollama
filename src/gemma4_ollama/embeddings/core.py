import ollama
from typing import List

def embed_text(
    text: str, 
    model: str = "embeddinggemma:300m-qat-q4_0", 
    host: str = "http://localhost:11434"
) -> List[float]:
    """
    Produce embeddings for the given text using Ollama.
    """
    client = ollama.Client(host=host)
    response = client.embeddings(model=model, prompt=text)
    return response.get("embedding", [])
