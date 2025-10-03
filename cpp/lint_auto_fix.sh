#!/bin/bash
# Auto-fix C++ formatting issues

set -e

# Build toolchain image with linting tools
echo "Building toolchain image..."
DOCKER_BUILDKIT=1 docker build \
    --target toolchain \
    -f Dockerfile.lint \
    -t ncpc2025-cpp-lint-toolchain \
    -q . >/dev/null 2>&1

# Format specified file(s) or all files
FILES="${1:-*.cpp}"
echo "Auto-fixing formatting for ${FILES}..."
docker run --rm -v $(pwd):/workspace ncpc2025-cpp-lint-toolchain clang-format -i ${FILES}
echo "✓ Formatting complete!"
