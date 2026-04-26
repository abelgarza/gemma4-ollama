# Audio Gemma4 Ollama

A Python project demonstrating audio and text interaction capabilities with the Gemma4 model via a local Ollama instance. This project uses a proper `src-layout` for reliable module resolution, features an experimental external memory layer, and includes a modern graphical UI for Voice Chat.

## Installation

To set up the project locally, create a virtual environment and install the package in editable mode along with its development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

*Note: You must have `ffmpeg` installed on your system for the voice recording and audio decoding features to work.*

## Configuration

The project uses environment variables for configuration. Copy the example file and adjust the values as needed:

```bash
cp .env.example .env
```

The default configuration points to:
- **Model**: `gemma4-audio:latest`
- **Embedding**: `embeddinggemma:300m-qat-q4_0`
- **Ollama**: `http://localhost:11434`
- **TTS_SPEED**: `1.2` (Adjust speech speed without pitch distortion)

## Voice Chat GUI (`main.py`)

The `main.py` file is the primary entry point for the end-to-end Voice Chat experience. It launches a modern, dark-themed graphical user interface (GUI) using `customtkinter`. 

**Execution:**
```bash
python main.py
```

**Features:**
- **Push-to-Talk (PTT):** Hold the `SPACE` bar (or click and hold the microphone button) to record your message.
- **Visual Feedback:** The UI dynamically updates to show states like "Grabando...", "Pensando...", and "Reproduciendo audio...".
- **Chat History:** A scrollable log displays the transcription/response exchange.
- **Asynchronous Execution:** Audio processing and TTS run in background threads, keeping the UI perfectly responsive.
- **Configurable Speed:** Reads `TTS_SPEED` from the `.env` to playback responses faster natively using `ffmpeg`.

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

The project uses two primary scripts to interact with the external memory layer.

#### 1. Adding Memory (`scripts/memory-add.py`)
Stores new information in both a history file (`JSONL`) and a semantic vector database (`SQLite`).

**Example:**
```bash
python scripts/memory-add.py --text "User likes coffee" --kind "preference" --source "user_input" --tag "user" --tag "beverage" --confidence 1.0
```

#### 2. Searching Memory (`scripts/memory-search.py`)
Queries the stored memories using Gemma's text embeddings.

**Example:**
```bash
python scripts/memory-search.py --query "What does the user like?" --top-k 3
```

#### 3. Resetting Memory (`scripts/memory-reset.py`)
Performs a hard reset by deleting the existing memory files (`JSONL` and `SQLite`).

**Example:**
```bash
python scripts/memory-reset.py
```

## Legacy Scripts (`scripts/`)

The `scripts/` directory contains legacy tools for granular interaction with the model via terminal.

### 1. Legacy Voice Chat (`ollama-voice-chat.py`)
Interact with the assistant using your microphone via CLI (Continuous listening chunks instead of PTT).

```bash
python scripts/ollama-voice-chat.py --seconds 3.5 --keep-audio
```

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

## License

Copyright (c) 2026 Abel Garza Ramírez. All rights reserved.
