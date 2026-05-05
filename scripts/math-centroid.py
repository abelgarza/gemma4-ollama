import math
from gemma4_ollama.embeddings import embed_text

def calculate_centroid(vectors):
    """Calcula el vector promedio (centroide) de una lista de vectores."""
    num_vectors = len(vectors)
    vector_dim = len(vectors[0])
    
    centroid = [0.0] * vector_dim
    for v in vectors:
        for i in range(vector_dim):
            centroid[i] += v[i]
            
    return [val / num_vectors for val in centroid]

def cosine_similarity(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    mag1 = math.sqrt(sum(a**2 for a in v1))
    mag2 = math.sqrt(sum(a**2 for a in v2))
    return dot_product / (mag1 * mag2) if mag1 and mag2 else 0

def main():
    print("--- KPI: Centroides (Perfilado de Temas) ---\n")
    
    # Definimos un "cluster" o tema
    tema_ia = [
        "Las redes neuronales imitan el cerebro humano",
        "El aprendizaje supervisado requiere datos etiquetados",
        "Los modelos de lenguaje masivos son revolucionarios"
    ]
    
    print(f"Calculando centroide para el tema 'Inteligencia Artificial' basado en {len(tema_ia)} frases...")
    vectors = [embed_text(t) for t in tema_ia]
    centroid = calculate_centroid(vectors)
    
    # Pruebas contra el centroide
    test_cases = [
        "Los LLMs estan democratizando el conocimiento",   # Relacionado
        "El precio del aguacate ha subido este mes"        # No relacionado
    ]

    print("\nEvaluando pertenencia al tema:")

    for test in test_cases:
        test_vector = embed_text(test)
        similarity = cosine_similarity(test_vector, centroid)
        status = "PERTENECE" if similarity > 0.51 else "AJENO"
        print(f"[{similarity:.4f}] -> {status}: '{test}'")

if __name__ == "__main__":
    main()
