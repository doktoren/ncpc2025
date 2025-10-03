#!/bin/bash
# Check Python code quality without modifying files

set -e

ALGORITHM=$1

uv sync --no-install-project

if [ -n "$ALGORITHM" ]; then
    # Lint specific algorithm
    if [ ! -f "${ALGORITHM}.py" ]; then
        echo "Error: ${ALGORITHM}.py not found"
        exit 1
    fi
    echo "Linting ${ALGORITHM}.py..."
    echo "Running ruff linting..."
    uv run ruff check "${ALGORITHM}.py"

    echo "Running mypy type checking..."
    uv run mypy --config-file mypy.ini "${ALGORITHM}.py"

    echo "✓ ${ALGORITHM} linting passed!"
else
    # Lint all files
    echo "Running ruff linting..."
    uv run ruff check

    echo "Running mypy type checking..."
    uv run mypy --config-file mypy.ini .

    echo "✓ All linting passed!"
fi
