from __future__ import annotations

import argparse
import os
from pathlib import Path

import ollama

from gemma4_ollama.image import image_to_base64

DEFAULT_IMAGE = Path(__file__).parent.parent / "data" / "sample-image" / "sample.png"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default=str(DEFAULT_IMAGE))
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL_AUDIO", "gemma4:latest"))
    parser.add_argument(
        "--prompt",
        default=(
            "Analyze the attached image directly."
        ),
    )
    args = parser.parse_args()

    image_b64 = image_to_base64(args.image)

    response = ollama.generate(
        model=args.model,
        prompt=args.prompt,
        images=[image_b64],
        stream=False,
    )

    print(response["response"])


if __name__ == "__main__":
    main()
