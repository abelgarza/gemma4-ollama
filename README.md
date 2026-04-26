# Audio Gemma4 Ollama

A Python project demonstrating audio and text interaction capabilities with the Gemma4 model via a local Ollama instance. This project uses a proper `src-layout` for reliable module resolution and includes an experimental external memory layer.

## Installation

To set up the project locally, create a virtual environment and install the package in editable mode along with its development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

*Note: You must have `ffmpeg` installed on your system for the voice recording features to work, and a system audio player like `mpv` or `mpg123` for the TTS functionality.*

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

The project uses two primary scripts to interact with the external memory layer.

#### 1. Adding Memory (`scripts/memory-add.py`)
Stores new information in both a history file (`JSONL`) and a semantic vector database (`SQLite`).

**Required Parameters:**
* `--text`: The content or fact to remember (e.g., `"The production server IP is 192.168.1.100"`).
* `--kind`: The category of the information (e.g., `preference`, `technical_context`, `fact`, `rule`).
* `--source`: Where this memory came from (e.g., `user_input`, `text`, `audio_chat`).

**Optional Parameters:**
* `--tag`: Tags to organize or filter memories. Can be used multiple times (e.g., `--tag devops --tag server`).
* `--confidence`: A float indicating the certainty of the memory (default: `1.0`).

**Example:**
```bash
.venv/bin/python scripts/memory-add.py --text "User likes coffee" --kind "preference" --source "user_input" --tag "user" --tag "beverage" --confidence 1.0
```

#### 2. Searching Memory (`scripts/memory-search.py`)
Queries the stored memories using Gemma's text embeddings.

**Parameters:**
* `--query` (Required): The phrase or concept to search for.
* `--top-k` (Optional): The maximum number of results to return.

**Example:**
```bash
.venv/bin/python scripts/memory-search.py --query "What does the user like?" --top-k 3
```

#### 3. Resetting Memory (`scripts/memory-reset.py`)
Performs a hard reset by deleting the existing memory files (`JSONL` and `SQLite`) and initializing fresh, empty databases.

**Parameters:**
* `--force` (Optional): Bypasses the interactive confirmation prompt.

**Example:**
```bash
.venv/bin/python scripts/memory-reset.py
# Or to skip confirmation:
.venv/bin/python scripts/memory-reset.py --force
```

## Voice Chat Orchestrator (`main.py`)

The `main.py` file is the primary entry point for the end-to-end Voice Chat experience. It orchestrates the entire interaction loop:
`Audio Input` $\rightarrow$ `Ollama Processing` $\rightarrow$ `Text Response` $\rightarrow$ `TTS (Sintesis de Voz)` $\rightarrow$ `Audio Output`.

**Execution:**
```bash
python main.py
```

**How it works:**
1. **Monitoring**: It polls `data/live-audio/latest.wav` for new recordings.
2. **Processing**: Converts the WAV file to base64 and sends it to the `gemma4-audio` model.
3. **Synthesis**: The text response is converted to speech using `gTTS` (Google Text-to-Speech).
4. **Playback**: The resulting audio is played automatically via the system player.

### Scripts and Examples

The `scripts/` directory contains specialized tools for granular interaction with the model.


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
