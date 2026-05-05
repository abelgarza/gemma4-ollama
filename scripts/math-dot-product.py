import argparse
from gemma4_ollama.embeddings import embed_text

def dot_product(v1, v2):
    """Calcula el producto punto de dos vectores."""
    return sum(a * b for a, b in zip(v1, v2))

def main():
    parser = argparse.ArgumentParser(description="KPI: Producto Punto (Ranking base)")
    parser.add_argument("--query", default="Receta de paella", help="Consulta de búsqueda")
    args = parser.parse_args()

    # Documentos candidatos
    docs = [
        "Cómo cocinar un arroz con mariscos delicioso",
        "Manual de reparación de motores diesel",
        "Ingredientes para una paella valenciana auténtica",
        "Guía de viaje por el centro de Madrid"
    ]

    print(f"Query: '{args.query}'\n")
    query_vec = embed_text(args.query)

    print("--- Ranking por Producto Punto ---")
    print("(Asumiendo vectores del modelo, el score más alto indica mayor relevancia)\n")

    rankings = []
    for doc in docs:
        doc_vec = embed_text(doc)
        score = dot_product(query_vec, doc_vec)
        rankings.append((doc, score))

    # Ordenar por score descendente
    rankings.sort(key=lambda x: x[1], reverse=True)

    for doc, score in rankings:
        print(f"[{score:.4f}] {doc}")

if __name__ == "__main__":
    main()
