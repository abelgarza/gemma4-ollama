import argparse
import os
import sys
from pathlib import Path
import ollama

# Ensure src is in the path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from gemma4_ollama.audio.stt import transcribe_audio
from gemma4_ollama.embeddings.core import embed_text
from gemma4_ollama.memory.vector_store import init_db, upsert_vector, search_vectors


def main():
    parser = argparse.ArgumentParser(description="Large Audio Analysis using STT + RAG")
    parser.add_argument("--audio", default="data/sample-audio/sample-earnings.mp3")
    parser.add_argument("--model", default="gemma4:latest")
    parser.add_argument("--embed-model", default="embeddinggemma:300m-qat-q4_0")
    parser.add_argument("--prompt", default="As an investor, what are the 3 most important points I need to consider when deciding whether or not to continue investing with them next year?")
    parser.add_argument("--whisper-model", default="base", help="tiny, base, small, medium, large-v3")
    parser.add_argument("--reset", action="store_true", help="Reset the vector database before starting")
    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"Error: Audio file not found: {audio_path}")
        return

    # 1. Initialize DB
    db_path = "data/memory/audio_rag.sqlite"
    if args.reset and os.path.exists(db_path):
        os.remove(db_path)
    init_db(db_path)

    # 2. Transcribe Audio (STT)
    print(f"--- FASE 1: Transcripción (STT) ---")
    segments = transcribe_audio(audio_path, model_size=args.whisper_model)
    print(f"Transcripción completada. {len(segments)} segmentos generados.")

    # 3. Indexing (Embeddings + Vector Store)
    print(f"\n--- FASE 2: Indexación Vectorial ---")
    for i, segment in enumerate(segments):
        if not segment["text"]:
            continue
            
        print(f"Procesando segmento {i+1}/{len(segments)}...", end="\r")
        vector = embed_text(segment["text"], model=args.embed_model)
        metadata = {
            "start": segment["start"],
            "end": segment["end"],
            "source": audio_path.name
        }
        upsert_vector(
            memory_id=f"{audio_path.stem}_{i}",
            vector=vector,
            text=segment["text"],
            metadata=metadata,
            path=db_path
        )
    print(f"\nIndexación completada.")

    # 4. Search (RAG)
    print(f"\n--- FASE 3: Búsqueda Semántica (RAG) ---")
    query_vector = embed_text(args.prompt, model=args.embed_model)
    relevant_chunks = search_vectors(query_vector, top_k=10, path=db_path)
    
    context_text = ""
    print("Fragmentos más relevantes encontrados:")
    for i, chunk in enumerate(relevant_chunks):
        start = chunk["metadata"]["start"]
        print(f"- [{start:.2f}s] {chunk['text'][:100]}... (Sim: {chunk['similarity']:.4f})")
        context_text += f"\n[Fragment at {start:.2f}s]: {chunk['text']}"

    # 5. Final Generation
    print(f"\n--- FASE 4: Generación de Respuesta Final ---")
    final_prompt = (
        f"You are a financial analyst. Based on the following transcript segments from an earnings call, "
        f"answer the user's question.\n\n"
        f"CONTEXT:\n{context_text}\n\n"
        f"USER QUESTION: {args.prompt}\n\n"
        f"FINAL ANALYSIS:"
    )

    response = ollama.generate(
        model=args.model,
        prompt=final_prompt,
        stream=False
    )

    print("\n" + "="*50)
    print("RESULTADO DEL ANÁLISIS:")
    print("="*50)
    print(response["response"])


if __name__ == "__main__":
    main()
