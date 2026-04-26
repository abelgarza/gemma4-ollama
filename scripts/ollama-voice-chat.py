from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

import ollama

from gemma4_ollama.audio import wav_to_base64


VOICE_TURN_PROMPT = """
The attached audio is the user's next spoken message in this conversation.

Reply naturally as a conversational assistant.
Use the same language as the user.
Do not analyze the audio.
Do not describe the audio.
Do not transcribe unless the user asks.
Do not mention that an audio file was attached.
Keep the conversation going normally.
""".strip()


def field(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def record_wav(
    *,
    source: str,
    output_path: Path,
    seconds: float,
    sample_rate: int,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-f",
        "pulse",
        "-i",
        source,
        "-t",
        str(seconds),
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        "-y",
        str(output_path),
    ]

    subprocess.run(cmd, check=True)


def stream_generate(
    client: ollama.Client,
    *,
    model: str,
    prompt: str,
    image_b64: str,
    context: list[int] | None,
) -> list[int] | None:
    kwargs: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "images": [image_b64],
        "stream": True,
    }

    if context:
        kwargs["context"] = context

    final_context = context

    try:
        for chunk in client.generate(**kwargs):
            text = field(chunk, "response", "")
            if text:
                print(text, end="", flush=True)

            if field(chunk, "done", False):
                final_context = field(chunk, "context", final_context)

        print()
        return final_context

    except Exception as exc:
        print(f"\n[stream failed] {type(exc).__name__}: {exc}", file=sys.stderr)
        print("[fallback] retrying without stream...\n", file=sys.stderr)

        kwargs["stream"] = False
        response = client.generate(**kwargs)

        text = field(response, "response", "")
        if text:
            print(text)

        return field(response, "context", final_context)


DEFAULT_WORKDIR = Path(__file__).parent.parent / "data" / "live-audio"

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemma4:latest")
    parser.add_argument("--host", default="http://localhost:11434")
    parser.add_argument("--source", default="RDPSource")
    parser.add_argument("--seconds", type=float, default=5.0)
    parser.add_argument("--sample-rate", type=int, default=16000)
    parser.add_argument("--workdir", default=str(DEFAULT_WORKDIR))
    parser.add_argument("--keep-audio", action="store_true")
    args = parser.parse_args()

    client = ollama.Client(host=args.host)
    workdir = Path(args.workdir)
    context: list[int] | None = None
    turn = 0

    print(f"model: {args.model}")
    print(f"source: {args.source}")
    print(f"chunk: {args.seconds}s")
    print("Ctrl+C para salir.")
    print()

    try:
        while True:
            turn += 1

            if args.keep_audio:
                wav_path = workdir / f"turn-{turn:04d}.wav"
            else:
                wav_path = workdir / "latest.wav"

            print(f"user: recording {args.seconds:g}s...", flush=True)
            record_wav(
                source=args.source,
                output_path=wav_path,
                seconds=args.seconds,
                sample_rate=args.sample_rate,
            )

            image_b64 = wav_to_base64(wav_path)

            print("assistant: ", end="", flush=True)
            context = stream_generate(
                client,
                model=args.model,
                prompt=VOICE_TURN_PROMPT,
                image_b64=image_b64,
                context=context,
            )

            if not args.keep_audio:
                wav_path.unlink(missing_ok=True)

            print()

    except KeyboardInterrupt:
        print("\nbye")

    except subprocess.CalledProcessError as exc:
        print(f"\nffmpeg failed with exit code {exc.returncode}", file=sys.stderr)
        sys.exit(exc.returncode)


if __name__ == "__main__":
    main()
