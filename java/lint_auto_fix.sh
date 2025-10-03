#!/bin/bash
# Auto-fix Java formatting issues

set -e

ALGORITHM=$1

if [ -n "$ALGORITHM" ]; then
    # Fix specific algorithm
    if [ ! -f "${ALGORITHM}.java" ]; then
        echo "Error: ${ALGORITHM}.java not found"
        exit 1
    fi
    echo "Auto-fixing formatting for ${ALGORITHM}.java..."
    docker run --rm -v $(pwd):/workspace ncpc2025-java-lint \
        java -jar /opt/tools/google-java-format.jar --aosp --replace "${ALGORITHM}.java"
    echo "✓ ${ALGORITHM}.java formatted!"
else
    # Fix all files
    echo "Auto-fixing formatting for all Java files..."
    docker run --rm -v $(pwd):/workspace ncpc2025-java-lint \
        java -jar /opt/tools/google-java-format.jar --aosp --replace *.java
    echo "✓ All Java files formatted!"
fi
