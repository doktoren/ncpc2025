#!/bin/bash
# Test a single Java algorithm in Docker

if [ -z "$1" ]; then
    echo "Usage: ./test_single.sh <algorithm_name>"
    echo "Example: ./test_single.sh fenwick_tree"
    exit 1
fi

ALGORITHM=$1

if [ ! -f "${ALGORITHM}.java" ]; then
    echo "Error: ${ALGORITHM}.java not found"
    exit 1
fi

echo "Testing ${ALGORITHM} using Docker..."

# Use BuildKit
export DOCKER_BUILDKIT=1

# Build image with just this file
cat > Dockerfile.single << EOF
FROM openjdk:21-slim
WORKDIR /workspace
COPY ${ALGORITHM}.java ./
RUN echo '#!/bin/bash\\n\\
set -e\\n\\
echo "Compiling ${ALGORITHM} with NCPC 2025 flags..."\\n\\
echo "Java version: \$(java -version 2>&1 | head -n1)"\\n\\
echo "Compiler flags: -encoding UTF-8 -sourcepath . -d ."\\n\\
echo ""\\n\\
\\n\\
if javac -encoding UTF-8 -sourcepath . -d . ${ALGORITHM}.java; then\\n\\
    echo "✓ Compilation successful"\\n\\
    echo "Running tests..."\\n\\
    if java -Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms1024m -Xmx1024m ${ALGORITHM}; then\\n\\
        echo "✓ All tests passed!"\\n\\
    else\\n\\
        echo "✗ Runtime tests failed!"\\n\\
        exit 1\\n\\
    fi\\n\\
else\\n\\
    echo "✗ Compilation failed!"\\n\\
    exit 1\\n\\
fi' > test.sh && chmod +x test.sh
CMD ["./test.sh"]
EOF

echo "Building Docker image..."
docker build -f Dockerfile.single -t ncpc-java-test . 2>&1 | grep -v "^#" | grep -v "naming to" | grep -v "writing image"

echo "Running tests..."
docker run --rm ncpc-java-test

# Cleanup
rm -f Dockerfile.single
