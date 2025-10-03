#!/bin/bash
# Run Java tests using multi-stage Docker build with optimal caching

set -e

TARGET=${1:-all}

if [ "$TARGET" != "all" ] && [ ! -f "${TARGET}.java" ]; then
    echo "Error: ${TARGET}.java not found"
    exit 1
fi

echo "Testing Java (target: ${TARGET})..."
if DOCKER_BUILDKIT=1 docker build \
    --target ${TARGET} \
    -f Dockerfile.test \
    -q . >/dev/null 2>&1; then
    echo "✓ Tests passed!"
else
    echo "✗ Tests failed! Running again with full output..."
    DOCKER_BUILDKIT=1 docker build \
        --target ${TARGET} \
        -f Dockerfile.test \
        .
    exit 1
fi
