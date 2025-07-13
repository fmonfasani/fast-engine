#!/usr/bin/env bash
# Simple setup script for the fast-engine project.
# It creates a Python virtual environment and installs the package in editable mode.
set -euo pipefail

# Create virtual environment if it does not exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip
pip install -e .

echo "Setup complete. Activate the virtual environment with 'source .venv/bin/activate'."
echo "FAST_ENGINE_HOME defaults to \$HOME/.fast-engine"

