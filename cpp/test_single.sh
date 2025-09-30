#!/bin/bash
# Script to test a single C++ algorithm file in Docker

if [ $# -eq 0 ]; then
    echo "Usage: $0 <algorithm_name>"
    echo "Example: $0 fenwick_tree"
    echo ""
    echo "Available algorithms:"
    ls *.cpp 2>/dev/null | sed 's/.cpp$//' | sed 's/^/  /'
    exit 1
fi

ALGORITHM=$1
CPP_FILE="${ALGORITHM}.cpp"

if [ ! -f "$CPP_FILE" ]; then
    echo "Error: $CPP_FILE not found"
    exit 1
fi

echo "Testing $ALGORITHM using Docker..."
echo "Building Docker image..."

# Build the Docker image with just this file
docker build -t ncpc-cpp-test --build-arg ALGORITHM="$ALGORITHM" -f - . << EOF
FROM gcc:13.2.0
WORKDIR /workspace
COPY $CPP_FILE ./
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Compiling $ALGORITHM with NCPC 2025 flags..."\n\
echo "Compiler: \$(g++ --version | head -n1)"\n\
echo "Flags: -x c++ -g -O2 -std=gnu++20 -static"\n\
echo ""\n\
\n\
if g++ -x c++ -g -O2 -std=gnu++20 -static $CPP_FILE -o $ALGORITHM; then\n\
    echo "✓ Compilation successful"\n\
    echo "Running tests..."\n\
    if ./$ALGORITHM; then\n\
        echo "✓ All tests passed!"\n\
    else\n\
        echo "✗ Runtime tests failed!"\n\
        exit 1\n\
    fi\n\
else\n\
    echo "✗ Compilation failed!"\n\
    exit 1\n\
fi' > test.sh && chmod +x test.sh
CMD ["./test.sh"]
EOF

echo "Running tests..."
docker run --rm ncpc-cpp-test