#!/bin/bash
# Check Python code quality without modifying files

set -e

TARGET=${1:-all}

if [ "$TARGET" != "all" ] && [ ! -f "${TARGET}.py" ]; then
    echo "Error: ${TARGET}.py not found"
    exit 1
fi

# Only sync dependencies once at the start
uv sync --no-install-project

echo "Linting Python (target: ${TARGET})..."

if [ "$TARGET" = "all" ]; then
    uv run ruff check
    uv run mypy --config-file mypy.ini .
else
    uv run ruff check "${TARGET}.py"
    uv run mypy --config-file mypy.ini "${TARGET}.py"
fi

echo "✓ Linting passed!"
