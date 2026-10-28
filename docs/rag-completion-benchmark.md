# Benchmark estático de completado con RAG (v0)

## Objetivo

Medir si Gemma 4 E2B completa un segmento real de código cuando recibe el código inmediatamente anterior/posterior y fragmentos relevantes de otro código del mismo repositorio, recuperados mediante embeddings. No modifica el repositorio; mide completado, no reparación de bugs ni autonomía.

## Diseño experimental

1. **Congelar** el repositorio con un commit (`git rev-parse HEAD`) y escoger un archivo y líneas continuas que realmente existan.
2. **Ocultar** las líneas seleccionadas. Mostrar hasta 45 líneas anteriores y posteriores (simulación fill-in-the-middle).
3. **Indexar** archivos de texto/código versionados, por fragmentos de 45 líneas; se excluye *todo el archivo objetivo* para evitar filtración directa de la respuesta. SQLite persiste embeddings, claveados por hash de contenido y modelo.
4. **Consultar** EmbeddingGemma con una consulta que describe la posición y sus contextos visibles; ordenar por coseno y seleccionar top-K.
5. **Generar** con `ollama.chat`, `temperature=0`, `num_ctx=4096`, `num_predict=160`, `think=false` (por defecto), sin herramientas ni edición real. Pedir únicamente las líneas faltantes.
6. **Registrar** prompt íntegro, referencias recuperadas, latencias, contadores de tokens de Ollama, salida, solución original, diff, similitud textual, exact match y validez sintáctica para Python.
7. **Comparar** las mismas tareas con `--top-k 0` (sin RAG), `--top-k 2` y `--top-k 4`, manteniendo demás condiciones constantes. Repetir cuando proceda.

## Preparación

```bash
ollama pull gemma4:e2b
ollama pull embeddinggemma:300m-qat-q4_0
# Elige el archivo y las líneas de la respuesta que quieras ocultar.
python scripts/rag_completion_benchmark.py \
  --repo ~/dev/gemma4-ollama \
  --file src/gemma4_ollama/audio/core.py \
  --line 35 --lines 5 \
  --model gemma4:e2b \
  --embed-model embeddinggemma:300m-qat-q4_0 \
  --out ./benchmark-runs
```

`--line 35` es **solo un ejemplo**: examina el archivo antes de elegir una región útil. Para la condición sin RAG, repite con `--top-k 0`.

## Artefactos y criterios

En `benchmark-runs/<fecha>-<id>/`: `summary.txt` (lectura humana), `result.json` (métricas y trazas), `prompt.txt`, `prediction.txt`, `expected.txt`, `diff.txt`, `ollama_response.json` (respuesta completa y metadatos) y `thinking.txt`. La salida registra `done_reason`, el número de líneas y una clasificación de fallo (`empty_output`, `line_count_mismatch`, `invalid_python_syntax`). El índice compartido queda en `benchmark-runs/vectors.sqlite`.

Las coincidencias textuales son estrictas: una alternativa semánticamente equivalente puede puntuar bajo. El AST de Python solo comprueba sintaxis, no corrección funcional. Para resultados serios, añadir pruebas unitarias en aislamiento, un conjunto de múltiples tareas/commits, y medir precisión de recuperación y evaluación de resultados con pruebas reales.

## Riesgos y controles

- **Fuga de respuesta**: se excluye todo el archivo objetivo del índice; otros archivos aún podrían contener una implementación duplicada. Revisar los extractos registrados.
- **Contaminación del modelo**: no asumimos que el modelo desconozca código público ya entrenado; comparar con repositorios privados o modificaciones sintéticas es más estricto.
- **Costo inicial**: la primera indexación hace una llamada de embeddings por fragmento; las siguientes reutilizan SQLite si el contenido no cambia. Evitar repositorios gigantes en v0.
- **Recursos**: el modelo de embeddings también requiere memoria; Ollama puede mantener modelos cargados. Medir consumo del host por separado. El script registra latencia y tokens, no RAM ni GPU.
- **Seguridad**: no ejecuta código del repositorio ni le concede al modelo un shell; no requiere Internet una vez descargados los modelos.
- **Control experimental**: temperatura cero no garantiza identidad bit a bit entre ejecuciones ni entre versiones de Ollama/modelo; guardar versiones y parámetros para una publicación formal.

## Siguiente etapa (fuera de v0)

Completar múltiples posiciones de forma automática con manifiesto congelado; añadir métricas CodeBLEU/tests, indexación por símbolos AST o Tree-sitter, recuperación híbrida BM25+vectores, y carga incremental del índice por commit. Finalmente, solo entonces, integrar con Pi/editor.
## Diagnóstico del primer resultado (2026-10-28)

En dos ejecuciones con E2B, Ollama contabilizó más de 2,000 tokens de salida, pero solo devolvió tres líneas visibles o ninguna. La causa aún no está confirmada. Repetir con `think=false` y límite `--num-predict 160`; inspeccionar `ollama_response.json`, especialmente `message.content`, `message.thinking`, `done_reason` y `eval_count`. Si Ollama rechaza `think=false` para el modelo, el error HTTP es evidencia de incompatibilidad y debe registrarse antes de cambiar estrategia. El benchmark no ha sido ejecutado aquí contra Ollama local.

Prueba sin RAG: `python scripts/rag_completion_benchmark.py --repo ~/dev/benchmark-targets/gemma4-ollama --file src/gemma4_ollama/audio/core.py --line 35 --lines 5 --top-k 0 --model gemma4:e2b --num-predict 160 --out benchmark-runs`.

Prueba con RAG: el mismo comando con `--top-k 4`. `--think` habilita explícitamente el razonamiento para pruebas comparativas posteriores.
