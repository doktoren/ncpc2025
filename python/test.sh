#!/bin/bash
# Run Python tests

set -e

ALGORITHM=$1

if [ -n "$ALGORITHM" ]; then
    # Test specific algorithm
    if [ ! -f "${ALGORITHM}.py" ]; then
        echo "Error: ${ALGORITHM}.py not found"
        exit 1
    fi
    echo "Testing ${ALGORITHM}.py..."
    python3 "${ALGORITHM}.py"
    echo "✓ ${ALGORITHM} tests passed!"
else
    # Test all files
    echo "Running all Python tests..."
    uv run pytest
fi
