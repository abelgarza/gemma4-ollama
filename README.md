# Gemma4 Ollama

A Python project demonstrating audio, text, and embeddings interaction capabilities with the Gemma4 model via a local Ollama instance. This project uses a modular `src-layout` (`gemma4_ollama`) for reliable module resolution, features an experimental external memory layer, and includes a modern graphical UI for Voice Chat.

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

## Project Structure

The codebase is organized into modular components under `src/gemma4_ollama/`:

- **`gemma4_ollama.audio`**: Handling WAV to Base64 conversion and Text-to-Speech (TTS).
- **`gemma4_ollama.memory`**: Core logic for JSONL storage and SQLite vector search.
- **`gemma4_ollama.embeddings`**: Simple wrapper for generating text embeddings via Ollama.

## Voice Chat GUI (`main.py`)

The `main.py` file launches a modern, dark-themed graphical user interface (GUI) using `customtkinter`. 

**Execution:**
```bash
python main.py
```

**Features:**
- **Push-to-Talk (PTT):** Hold the `SPACE` bar (or click and hold the microphone button).
- **Visual Feedback:** Dynamic status updates ("Grabando...", "Pensando...").
- **Chat History:** Displays the conversation log.

## External Memory Layer

This project implements a clean experimental memory layer that lives outside the LLM.

### Managing Memory

#### 1. Adding Memory (`scripts/memory-add.py`)
Stores new information in both a history file (`JSONL`) and a semantic vector database (`SQLite`).

```bash
python scripts/memory-add.py --text "User likes coffee" --kind "preference" --source "user_input"
```

#### 2. Searching Memory (`scripts/memory-search.py`)
Queries the stored memories using text embeddings.

```bash
python scripts/memory-search.py --query "What does the user like?"
```

## Exploratory Scripts (`scripts/`)

The `scripts/` directory contains various tools for direct interaction with Ollama.

### Embeddings
- `ollama-embeddings-python.py`: Generate embeddings using the internal library.
- `ollama-embeddings-requests.py`: Generate embeddings via direct HTTP requests.

### Audio & Voice
- `ollama-audio-python.py`: Analyze a specific `.wav` file.
- `ollama-voice-chat.py`: CLI-based voice interaction (continuous chunks).
- `ollama-audio-requests.py`: Direct API interaction for audio processing.

### Text
- `ollama-text-python.py`: Standard text interaction (Library).
- `ollama-text-requests.py`: Standard text interaction (HTTP).

## Testing

The package is tested using `pytest`.

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 -m pytest tests/
```

## License

This project is licensed under the **Apache License 2.0** - see the [LICENSE](LICENSE) file for details.
