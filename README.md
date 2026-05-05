# Gemma4 Ollama

This repository is a dedicated environment for exploring the capabilities of the **Gemma4** model—including audio, image, and text—via a local **Ollama** instance.

## Project Structure

* **/src/gemma4_ollama**: Core logic and modular implementation using `src-layout`.
* **/scripts**: Executable scripts for direct testing and interaction.

## Installation

To ensure reliable module resolution, install the package in editable mode:

```bash
pip install -e .
```

## Aprendizaje Matemático (KPIs Vectoriales)

Se han añadido scripts en `/scripts` para aprender la matemática detrás de los embeddings sin librerías de alto nivel:

- `math-cosine-similarity.py`: Similitud de coseno para búsqueda semántica.
- `math-euclidean-distance.py`: Distancia absoluta para detección de anomalías.
- `math-centroid.py`: Creación de perfiles promedio (centroides) para clasificación de temas.
- `math-dot-product.py`: Producto punto para scoring y ranking básico.

---

## License

This project is licensed under the **Apache License 2.0**.

---
