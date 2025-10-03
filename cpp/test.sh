#!/bin/bash
# Run C++ tests

set -e

ALGORITHM=$1

if [ -n "$ALGORITHM" ]; then
    # Test specific algorithm
    if [ ! -f "${ALGORITHM}.cpp" ]; then
        echo "Error: ${ALGORITHM}.cpp not found"
        exit 1
    fi

    echo "Testing ${ALGORITHM} using Docker..."
    docker run --rm -v $(pwd):/workspace gcc:13.2.0 bash -c "\
        cd /workspace && \
        g++ -x c++ -g -O2 -std=gnu++20 -static ${ALGORITHM}.cpp -o ${ALGORITHM} && \
        ./${ALGORITHM} && \
        rm ${ALGORITHM}"
    echo "✓ ${ALGORITHM} tests passed!"
else
    # Test all algorithms
    echo "Testing all C++ algorithms with Docker..."
    echo "Compiler: g++ 13.2.0 with NCPC 2025 flags"
    echo ""

    # Use BuildKit for better caching
    export DOCKER_BUILDKIT=1

    # Calculate checksum of all .cpp files
    SOURCE_HASH=$(find . -name "*.cpp" -type f -exec md5sum {} \; | sort | md5sum | cut -d' ' -f1)
    CACHE_FILE=".docker_build_cache"

    # Check if we need to rebuild
    if [ ! -f "$CACHE_FILE" ] || [ "$(cat $CACHE_FILE)" != "$SOURCE_HASH" ]; then
        echo "Source files changed, rebuilding Docker image..."
        docker build -t ncpc-cpp .
        echo "$SOURCE_HASH" > "$CACHE_FILE"
    else
        echo "Source unchanged, using cached image..."
    fi

    # Run tests
    docker run --rm ncpc-cpp
fi
