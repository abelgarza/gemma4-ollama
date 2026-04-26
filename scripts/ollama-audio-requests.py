from __future__ import annotations

import argparse
import requests
from pathlib import Path

from audio_gemma4_ollama import wav_to_base64

DEFAULT_AUDIO = Path(__file__).parent.parent / "data" / "sample-audio" / "sample.wav"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemma4:latest")
    parser.add_argument("--audio", default=str(DEFAULT_AUDIO))
    parser.add_argument("--url", default="http://localhost:11434/api/generate")
    parser.add_argument(
        "--prompt",
        default=(
            "Analyze the attached audio directly. "
            "Tell me language, speaker count, tone, what is being said, "
            "and relevant acoustic events."
        ),
    )
    args = parser.parse_args()

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "images": [wav_to_base64(args.audio)],
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
