# Audio Gemma4 Ollama

A Python project demonstrating audio and text interaction capabilities with the Gemma4 model via a local Ollama instance. This project uses a proper `src-layout` for reliable module resolution and includes an experimental external memory layer.

## Installation

To set up the project locally, create a virtual environment and install the package in editable mode along with its development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

*Note: You must have `ffmpeg` installed on your system for the voice recording features to work.*

## Configuration

The project uses environment variables for configuration. Copy the example file and adjust the values as needed:

```bash
cp .env.example .env
```

The default configuration points to:
- **Model**: `gemma4-audio:latest` (Memory-aware)
- **Embedding**: `embeddinggemma:300m-qat-q4_0`
- **Ollama**: `http://localhost:11434`

## External Memory Layer

This project implements a clean experimental memory layer that lives outside the LLM. The `gemma4-audio:latest` model is designed to be "memory-aware", meaning it can utilize context injected into the prompt via the following placeholders:
- `MEMORY`: High-confidence relevant context.
- `MEMORY_CANDIDATES`: Potential matches for the current interaction.

### Memory Setup

1. **Pull the embedding model**:
   ```bash
   ollama pull embeddinggemma:300m-qat-q4_0
   ```

2. **Create the memory-aware model**:
   ```bash
   ollama create gemma4-audio:latest -f models/gemma4-audio.Modelfile
   ```

### Managing Memory

- **Add Memory**: `.venv/bin/python scripts/memory-add.py --text "User likes coffee" --kind preference --source text --tag user`
- **Search Memory**: `.venv/bin/python scripts/memory-search.py --query "What does the user like?"`

## Usage and Examples

The `scripts/` directory contains several examples for interacting with the model via both text and audio.

### 1. Voice Chat (`ollama-voice-chat.py`)
Interact with the assistant using your microphone. The script records short audio chunks, converts them to base64, and streams the assistant's text response.

**Basic usage:**
```bash
python scripts/ollama-voice-chat.py
```

**Advanced usage with parameters:**
You can customize the recording duration, the model, and whether to keep the audio history.

```bash
python scripts/ollama-voice-chat.py --seconds 3.5 --keep-audio --model gemma4:latest
```

**Key Parameters:**
* `--seconds`: Duration of each audio recording turn in seconds (default: `5.0`).
* `--keep-audio`: Flag to save all recorded `.wav` files (e.g., `turn-0001.wav`) instead of overwriting `latest.wav`.
* `--model`: The Ollama model to use (default: `gemma4:latest`).
* `--source`: The audio input source used by `ffmpeg` (default: `RDPSource`).
* `--sample-rate`: Audio sample rate (default: `16000`).
* `--workdir`: Directory to store the live audio files (default: `data/live-audio`).

### 2. Audio File Processing (`ollama-audio-python.py`)
Analyze a specific existing `.wav` file.

```bash
python scripts/ollama-audio-python.py --audio data/sample-audio/sample.wav
```

### 3. Text Generation (`ollama-text-python.py`)
Standard text-based interaction using the Ollama Python client.

```bash
python scripts/ollama-text-python.py
```

## Testing

The package is thoroughly tested using `pytest`. To run the test suite:

```bash
pytest tests/
```

## Benchmarks and Reports

Performance testing and evaluation results are generated separately. **All benchmark logs, metrics, and generated performance reports will be deposited in the `benchmarks/` directory for consultation.** 

## License

Copyright (c) 2026 Abel Garza Ramírez. All rights reserved.
