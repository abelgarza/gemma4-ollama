from __future__ import annotations

import argparse
import os
from pathlib import Path

import ollama

from gemma4_ollama.audio import wav_to_base64

DEFAULT_AUDIO = Path(__file__).parent.parent / "data" / "sample-audio" / "sample.wav"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", default=str(DEFAULT_AUDIO))
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "gemma4:latest"))
    parser.add_argument(
        "--prompt",
        default=(
            "The attached audio is the user's message. "
            "Reply naturally in the same language. "
            "Do not analyze, describe, or mention the audio."
        ),
    )
    args = parser.parse_args()

    audio_b64 = wav_to_base64(args.audio)

    response = ollama.generate(
        model=args.model,
        prompt=args.prompt,
        images=[audio_b64],
        stream=False,
    )

    print(response["response"])


if __name__ == "__main__":
    main()
