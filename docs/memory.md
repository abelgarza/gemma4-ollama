# External Memory Layer for Audio Gemma4

This experimental layer provides long-term memory for the voice assistant, stored outside the model itself.

## Architecture

- **gemma4-audio-memory**: A specialized Modelfile that expects memory context in the prompt.
- **JSONL Storage**: `data/memory/memory.jsonl` stores the full record history.
- **Vector Store**: `data/memory/vectors.sqlite` stores text embeddings for fast retrieval.
- **Embeddings**: Generated using Ollama's `embeddinggemma:300m-qat-q4_0` model.

## Setup

1. **Pull the embedding model**:
   ```bash
   ollama pull embeddinggemma:300m-qat-q4_0
   ```

2. **Create the memory-aware model**:
   ```bash
   ollama create gemma4-audio-memory:latest -f models/gemma4-audio-memory.Modelfile
   ```

## Usage

### Adding Memory

Use `scripts/memory-add.py` to store new information:

```bash
.venv/bin/python scripts/memory-add.py --text "Project uses gemma4-audio:latest for voice-first conversation." --kind technical_context --source text --tag ollama --tag voice
```

### Searching Memory

Use `scripts/memory-search.py` to query existing memories:

```bash
.venv/bin/python scripts/memory-search.py --query "voice model"
```

## Why external memory?

- **Persistence**: Memories survive model reloads and updates.
- **Scale**: External databases can store millions of records efficiently.
- **Control**: You can inspect, edit, or delete memories without retraining the model.
