from __future__ import annotations

import torch
from faster_whisper import WhisperModel
from pathlib import Path
from typing import List, Dict, Any


def transcribe_audio(
    file_path: str | Path, 
    model_size: str = "base", 
    device: str = "auto", 
    compute_type: str = "float16"
) -> List[Dict[str, Any]]:
    """
    Transcribes an audio file into segments using faster-whisper.
    Returns a list of dictionaries with text and timestamps.
    """
    p = Path(file_path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"Audio file not found: {p}")

    # Determine device automatically if auto is selected
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # On CPU, float16 is not supported, so we fall back to float32 or int8
    if device == "cpu" and compute_type == "float16":
        compute_type = "int8"

    print(f"Loading Whisper model '{model_size}' on {device} ({compute_type})...")
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    print(f"Transcribing: {p.name}...")
    segments, info = model.transcribe(str(p), beam_size=5)

    results = []
    for segment in segments:
        results.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })
        # Optional: Print progress for long files
        # print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

    return results
