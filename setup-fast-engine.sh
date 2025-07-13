#!/usr/bin/env bash

# Fast-Engine setup script
# Creates a virtual environment and installs project dependencies.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r "$ROOT_DIR/requirements.txt"

# Install project in editable mode
pip install -e "$ROOT_DIR"

echo "\nFast-Engine setup complete. Activate the environment with:\n  source $VENV_DIR/bin/activate"
echo "Refer to README.md for usage instructions."
