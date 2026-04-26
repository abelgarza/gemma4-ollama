import sqlite3
import json
import math
import os
from typing import List, Dict, Any, Tuple

def init_db(path: str = "data/memory/vectors.sqlite"):
    """
    Initialize the SQLite database for vector storage.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vectors (
            memory_id TEXT PRIMARY KEY,
            vector TEXT,
            text TEXT,
            metadata TEXT
        )
    """)
    conn.commit()
    conn.close()

def upsert_vector(memory_id: str, vector: List[float], text: str, metadata: Dict[str, Any], path: str = "data/memory/vectors.sqlite"):
    """
    Insert or update a vector in the database.
    """
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO vectors (memory_id, vector, text, metadata)
        VALUES (?, ?, ?, ?)
    """, (memory_id, json.dumps(vector), text, json.dumps(metadata)))
    conn.commit()
    conn.close()

def dot_product(v1: List[float], v2: List[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))

def norm(v: List[float]) -> float:
    return math.sqrt(sum(a * a for a in v))

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    n1 = norm(v1)
    n2 = norm(v2)
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot_product(v1, v2) / (n1 * n2)

def search_vectors(query_vector: List[float], top_k: int = 5, path: str = "data/memory/vectors.sqlite") -> List[Dict[str, Any]]:
    """
    Search for the most similar vectors using cosine similarity.
    """
    if not os.path.exists(path):
        return []
        
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute("SELECT memory_id, vector, text, metadata FROM vectors")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for memory_id, vector_json, text, metadata_json in rows:
        vector = json.loads(vector_json)
        similarity = cosine_similarity(query_vector, vector)
        results.append({
            "memory_id": memory_id,
            "text": text,
            "metadata": json.loads(metadata_json),
            "similarity": similarity
        })

    # Sort by similarity descending
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]
