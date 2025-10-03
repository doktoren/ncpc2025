#!/bin/bash
# Auto-fix Java formatting issues

set -e

# Build toolchain image with linting tools
echo "Building toolchain image..."
DOCKER_BUILDKIT=1 docker build \
    --target toolchain \
    -f Dockerfile.lint \
    -t ncpc2025-java-lint-toolchain \
    -q . >/dev/null 2>&1

# Format specified file(s) or all files
FILES="${1:-*.java}"
echo "Auto-fixing formatting for ${FILES}..."
docker run --rm -v $(pwd):/workspace ncpc2025-java-lint-toolchain \
    java -jar /opt/tools/google-java-format.jar --aosp --replace ${FILES}
echo "✓ Formatting complete!"
