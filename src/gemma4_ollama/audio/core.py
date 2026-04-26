from __future__ import annotations

import base64
from pathlib import Path


def wav_to_base64(path: str | Path) -> str:
    p = Path(path)
    data = p.read_bytes()

    if not (data[:4] == b"RIFF" and data[8:12] == b"WAVE"):
        raise ValueError(f"Expected WAV file: {p}")

    return base64.b64encode(data).decode("utf-8")


# Backward-compatible alias.
read_wav_as_base64 = wav_to_base64
