import math
import os
import argparse
from dotenv import load_dotenv
from gemma4_ollama.embeddings import embed_text

load_dotenv()

def dot_product(v1, v2):
    """Calcula el producto punto de dos vectores."""
    return sum(a * b for a, b in zip(v1, v2))

def magnitude(v):
    """Calcula la magnitud (norma L2) de un vector."""
    return math.sqrt(sum(a**2 for a in v))

def cosine_similarity(v1, v2):
    """
    Calcula la similitud de coseno entre dos vectores.
    Fórmula: (A . B) / (||A|| * ||B||)
    """
    m1 = magnitude(v1)
    m2 = magnitude(v2)
    if m1 == 0 or m2 == 0:
        return 0
    return dot_product(v1, v2) / (m1 * m2)

def main():
    parser = argparse.ArgumentParser(description="KPI: Similitud de Coseno (Matemática pura)")
    parser.add_argument("--query", default="Tengo mucha hambre", help="Texto a comparar")
    args = parser.parse_args()

    # Base de conocimiento simple
    knowledge_base = [
        "El desarrollo de apps es fascinante",
        "Hoy es un día muy soleado en la montaña",
        "La inteligencia artificial transforma industrias",
        "Me encanta cocinar recetas tradicionales",
        "El compilador marca un error",
        "Los elefantes no son de color rosa"
    ]

    print(f"Query: '{args.query}'\n")
    print("Generando embeddings...")
    
    query_vector = embed_text(args.query)
    
    results = []
    for text in knowledge_base:
        text_vector = embed_text(text)
        score = cosine_similarity(query_vector, text_vector)
        results.append((text, score))
    
    # Ordenar por score descendente
    results.sort(key=lambda x: x[1], reverse=True)

    print("--- Resultados de Similitud de Coseno ---")
    for text, score in results:
        print(f"[{score:.4f}] {text}")

    best_match = results[0]
    print(f"\nEl vecino más cercano es: '{best_match[0]}' con un score de {best_match[1]:.4f}")

if __name__ == "__main__":
    main()
