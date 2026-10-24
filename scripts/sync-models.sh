#!/usr/bin/env bash
set -euo pipefail

# Sync external Modelfile repositories without embedding their content in this Git repo.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PUBLIC_URL="${PUBLIC_MODELS_URL:-https://github.com/abelgarza/ollama-public-modelfiles.git}"
PRIVATE_URL="${PRIVATE_MODELS_URL:-git@github.com:abelgarza/ollama-private-modelfiles.git}"
INCLUDE_PRIVATE=false
if [[ "${1:-}" == "--with-private" ]]; then INCLUDE_PRIVATE=true
elif [[ $# -gt 0 ]]; then
  echo "Usage: bash scripts/sync-models.sh [--with-private]" >&2
  exit 2
fi

sync_repo() {
  local url="$1" target="$2"
  if [[ -d "$target/.git" ]]; then
    echo "Updating $target"
    git -C "$target" pull --ff-only
  elif [[ -e "$target" ]]; then
    echo "Refusing to overwrite existing non-git path: $target" >&2
    return 1
  else
    echo "Cloning $url -> $target"
    git clone "$url" "$target"
  fi
}

sync_repo "$PUBLIC_URL" "$ROOT/models/public"
if [[ "$INCLUDE_PRIVATE" == true ]]; then
  sync_repo "$PRIVATE_URL" "$ROOT/models/private"
else
  echo "Private models skipped (use --with-private after creating its initial commit and configuring Git access)."
fi
