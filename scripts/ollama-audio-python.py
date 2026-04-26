from __future__ import annotations

import argparse
import os

import ollama

from src.ollama_audio import read_wav_as_base64


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", default="data/sample-audio/sample.wav")
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "gemma4:e4b"))
    parser.add_argument(
        "--prompt",
        default=(
            "Analyze this audio directly. "
            "Describe spoken language, speaker count, tone, and relevant acoustic events."
        ),
    )
    args = parser.parse_args()

    audio_b64 = read_wav_as_base64(args.audio)

    response = ollama.chat(
        model=args.model,
        messages=[
            {
                "role": "user",
                "content": args.prompt,
                # Mismo truco: bytes WAV por canal multimodal.
                "images": [audio_b64],
            }
        ],
        stream=False,
    )

    print(response["message"]["content"])


if __name__ == "__main__":
    main()
