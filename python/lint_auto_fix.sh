#!/bin/bash
# Auto-fix Python formatting issues

set -e

ALGORITHM=$1

if [ -n "$ALGORITHM" ]; then
    # Lint specific algorithm
    if [ ! -f "${ALGORITHM}.py" ]; then
        echo "Error: ${ALGORITHM}.py not found"
        exit 1
    fi
    echo "Auto-fixing formatting for ${ALGORITHM}.py..."
    uv run ruff check --fix "${ALGORITHM}.py"
    echo "Done!"
else
    # Lint all files
    echo "Auto-fixing formatting for all Python files..."
    uv run ruff check --fix
    echo "Done!"
fi
