from __future__ import annotations

import base64
import subprocess
import tempfile
from pathlib import Path


def audio_to_base64(path: str | Path) -> str:
    p = Path(path).expanduser().resolve()

    if not p.exists():
        raise FileNotFoundError(f"Audio file not found: {p}")

    # For Ollama's gemma4 multimodal hack, it often expects a specific WAV format.
    # We'll use ffmpeg to ensure the file is in a compatible format (48kHz, stereo, wav).
    # This also handles MP3 and other formats automatically.
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
        tmp_path = Path(tmp_wav.name)

    try:
        # Convert to 48kHz, stereo, s16le WAV
        cmd = [
            "ffmpeg",
            "-y",
            "-loglevel", "quiet",
            "-i", str(p),
            "-ar", "48000",
            "-ac", "2",
            "-f", "wav",
            str(tmp_path)
        ]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            raise ValueError(f"Expected audio file, but ffmpeg failed to process: {p}")
        
        data = tmp_path.read_bytes()
        return base64.b64encode(data).decode("utf-8")
    finally:
        if tmp_path.exists():
            tmp_path.unlink()

