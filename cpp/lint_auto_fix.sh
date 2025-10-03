#!/bin/bash
# Auto-fix C++ formatting issues

set -e

ALGORITHM=$1

if [ -n "$ALGORITHM" ]; then
    # Fix specific algorithm
    if [ ! -f "${ALGORITHM}.cpp" ]; then
        echo "Error: ${ALGORITHM}.cpp not found"
        exit 1
    fi
    echo "Auto-fixing formatting for ${ALGORITHM}.cpp..."
    docker run --rm -v $(pwd):/workspace ncpc2025-cpp-lint clang-format -i "${ALGORITHM}.cpp"
    echo "✓ ${ALGORITHM}.cpp formatted!"
else
    # Fix all files
    echo "Auto-fixing formatting for all C++ files..."
    docker run --rm -v $(pwd):/workspace ncpc2025-cpp-lint clang-format -i *.cpp
    echo "✓ All C++ files formatted!"
fi
