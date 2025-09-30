#!/bin/bash
# Fast C++ algorithm testing with smart Docker caching

set -e

echo "Testing C++ algorithms with Docker..."
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