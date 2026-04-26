from __future__ import annotations

import base64
from pathlib import Path


IMAGE_SIGNATURES = {
    "png": b"\x89PNG\r\n\x1a\n",
    "jpg": b"\xff\xd8\xff",
    "jpeg": b"\xff\xd8\xff",
    "webp": b"RIFF",  # requiere check extra abajo
}


def image_to_base64(path: str | Path) -> str:
    p = Path(path).expanduser().resolve()

    if not p.exists():
        raise FileNotFoundError(f"Image not found: {p}")

    data = p.read_bytes()

    is_png = data.startswith(b"\x89PNG\r\n\x1a\n")
    is_jpeg = data.startswith(b"\xff\xd8\xff")
    is_webp = data[:4] == b"RIFF" and data[8:12] == b"WEBP"

    if not (is_png or is_jpeg or is_webp):
        raise ValueError(f"Expected image file PNG/JPEG/WEBP: {p}")

    return base64.b64encode(data).decode("utf-8")

