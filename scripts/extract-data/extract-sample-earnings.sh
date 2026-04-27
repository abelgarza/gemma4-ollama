#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Resolve project root (assumes script is in /scripts)
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Configuration via environment variables or arguments
# Usage: ./script.sh [URL] [RELATIVE_DEST_PATH]
URL="${1:-https://investorstiendas3b.com/files/doc_financials/2025/q4/Tiendas-3B-Fourth-Quarter-2025-Earnings-Call-Audio.mp3}"
RELATIVE_PATH="${2:-data/sample-audio/sample-earnings.mp3}"

# Construct absolute path
DEST_PATH="$PROJECT_ROOT/$RELATIVE_PATH"
DEST_DIR="$(dirname "$DEST_PATH")"

# Ensure target directory exists
mkdir -p "$DEST_DIR"

# Download process
echo "Starting download..."
echo "Target: $DEST_PATH"

curl -L "$URL" -o "$DEST_PATH"

# Validation
if [ $? -eq 0 ]; then
    echo "DONE"
else
    echo "ERROR: Download failed"
    exit 1
fi
