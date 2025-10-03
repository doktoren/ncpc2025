#!/bin/bash
# Check Java code quality using multi-stage Docker build with optimal caching

set -e

TARGET=${1:-all}

if [ "$TARGET" != "all" ] && [ ! -f "${TARGET}.java" ]; then
    echo "Error: ${TARGET}.java not found"
    exit 1
fi

echo "Linting Java (target: ${TARGET})..."
if DOCKER_BUILDKIT=1 docker build \
    --target ${TARGET} \
    -f Dockerfile.lint \
    -q . >/dev/null 2>&1; then
    echo "✓ Linting passed!"
else
    echo "✗ Linting failed! Running again with full output..."
    DOCKER_BUILDKIT=1 docker build \
        --target ${TARGET} \
        -f Dockerfile.lint \
        .
    exit 1
fi
