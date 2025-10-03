#!/bin/bash
# Run Python tests

set -e

TARGET=${1:-all}

if [ "$TARGET" != "all" ] && [ ! -f "${TARGET}.py" ]; then
    echo "Error: ${TARGET}.py not found"
    exit 1
fi

echo "Testing Python (target: ${TARGET})..."
if [ "$TARGET" = "all" ]; then
    uv run pytest
else
    python3 "${TARGET}.py"
fi
echo "✓ Tests passed!"
