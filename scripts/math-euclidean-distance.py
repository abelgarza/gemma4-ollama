import math
import argparse
from gemma4_ollama.embeddings import embed_text

def euclidean_distance(v1, v2):
    """
    Calcula la distancia euclidiana entre dos vectores.
    Fórmula: sqrt(sum((a - b)^2))
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

def main():
    parser = argparse.ArgumentParser(description="KPI: Distancia Euclidiana (Matemática pura)")
    parser.add_argument("--query", default="El cielo está despejado y azul", help="Texto a comparar")
    args = parser.parse_args()

    # Comparativa para ver distancias relativas
    comparisons = [
        "Hace un día muy bonito y soleado",   # Similar
        "La economía mundial está en crisis",  # Diferente
        "Las estrellas brillan en la noche"    # Relacionado pero distinto
    ]

    print(f"Query: '{args.query}'\n")
    query_vector = embed_text(args.query)

    print("--- Resultados de Distancia Euclidiana ---")
    print("(Menor distancia = Mayor similitud absoluta)\n")

    results = []
    for text in comparisons:
        text_vector = embed_text(text)
        dist = euclidean_distance(query_vector, text_vector)
        results.append((text, dist))

    # Ordenar por distancia ascendente (más cerca primero)
    results.sort(key=lambda x: x[1])

    for text, dist in results:
        print(f"[{dist:.4f}] {text}")

    print(f"\nEl concepto más cercano geométricamente es: '{results[0][0]}'")

if __name__ == "__main__":
    main()
