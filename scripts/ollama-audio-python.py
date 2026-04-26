from __future__ import annotations

import argparse
import os

import ollama

from audio_gemma4_ollama import wav_to_base64


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", default="data/sample-audio/sample.wav")
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
