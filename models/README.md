# External Ollama Modelfiles

`models/gemma4-audio.Modelfile` belongs to this project and stays tracked.

External Modelfiles are **independent Git repositories** cloned locally:

- `models/public/` → [ollama-public-modelfiles](https://github.com/abelgarza/ollama-public-modelfiles)
- `models/private/` → `abelgarza/ollama-private-modelfiles` (optional, restricted access)

Their contents and Git metadata are ignored by this parent repository; private Modelfiles are **never copied into its commits** by this sync workflow.

## Sync

From the project root:

```bash
bash scripts/sync-models.sh
```

To also clone or update the private repository:

```bash
bash scripts/sync-models.sh --with-private
```

The private repository must first have an initial commit/branch and your local Git credentials must permit access. The script uses SSH for private access by default; override `PRIVATE_MODELS_URL` to use an appropriate authenticated remote if needed. Never embed tokens in repository files or commit URLs.

The sync performs `git pull --ff-only` for existing clones; it will not discard local changes or overwrite an existing non-Git folder. To publish changes, commit and push **within the corresponding external repository**, not from the parent.

Optional remote overrides: `PUBLIC_MODELS_URL` and `PRIVATE_MODELS_URL`.

## Notes

- Clone the main project normally, then run the sync command. These are **not** Git submodules.
- A fresh clone of this public project will not contain private models, and private access is not required to use its existing features.
- Ollama models themselves are installed separately; these files configure model behavior and do not download model weights.
