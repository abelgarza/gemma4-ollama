from __future__ import annotations

import argparse
import os
import requests
from pathlib import Path

from gemma4_ollama.image import image_to_base64

DEFAULT_IMAGE = Path(__file__).parent.parent / "data" / "sample-image" / "sample.png"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "gemma4:latest"))
    parser.add_argument("--image", default=str(DEFAULT_IMAGE))
    parser.add_argument("--url", default="http://localhost:11434/api/generate")
    parser.add_argument(
        "--prompt",
        default=(
            "Analyze the attached image directly."
        ),
    )
    args = parser.parse_args()

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "images": [image_to_base64(args.image)],
        "stream": False,
    }

    response = requests.post(args.url, json=payload, timeout=300)

    if response.status_code == 200:
        print(response.json()["response"])
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


if __name__ == "__main__":
    main()
