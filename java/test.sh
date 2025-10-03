#!/bin/bash
# Run Java tests

set -e

ALGORITHM=$1

if [ -n "$ALGORITHM" ]; then
    # Test specific algorithm
    if [ ! -f "${ALGORITHM}.java" ]; then
        echo "Error: ${ALGORITHM}.java not found"
        exit 1
    fi

    echo "Testing ${ALGORITHM} using Docker..."
    docker run --rm -v $(pwd):/workspace openjdk:21-slim bash -c "\
        cd /workspace && \
        javac -encoding UTF-8 -sourcepath . -d . ${ALGORITHM}.java && \
        java -Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms1024m -Xmx1024m -ea ${ALGORITHM}"
    echo "✓ ${ALGORITHM} tests passed!"
else
    # Test all algorithms
    echo "Testing all Java algorithms with Docker..."
    echo "Java: OpenJDK 21.0.4 with NCPC 2025 flags"
    echo ""

    # Use BuildKit for better caching
    export DOCKER_BUILDKIT=1

    # Calculate checksum of all .java files
    SOURCE_HASH=$(find . -name "*.java" -type f -exec md5sum {} \; | sort | md5sum | cut -d' ' -f1)
    CACHE_FILE=".docker_build_cache"

    # Check if we need to rebuild
    if [ ! -f "$CACHE_FILE" ] || [ "$(cat $CACHE_FILE)" != "$SOURCE_HASH" ]; then
        echo "Source files changed, rebuilding Docker image..."
        docker build -t ncpc-java .
        echo "$SOURCE_HASH" > "$CACHE_FILE"
    else
        echo "Source unchanged, using cached image..."
    fi

    # Run tests
    docker run --rm ncpc-java
fi
