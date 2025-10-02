#!/bin/bash
# Complete test and linting runner for NCPC 2025 algorithms

set -e

echo "Testing and Linting NCPC 2025 Algorithms"
echo "========================================="
echo ""

# Python: Lint + Type Check + Test
echo "Python algorithms (linting, type checking, and testing):"
cd python && ./lint.sh
cd ..
echo ""

# C++: Lint + Test
echo "C++ algorithms (linting and testing):"
cd cpp
echo "Running linting..."
docker run --rm -v $(pwd):/workspace ncpc2025-cpp-lint
echo ""
echo "Running tests..."
./test_all.sh
cd ..
echo ""

# Java: Lint + Test
echo "Java algorithms (linting and testing):"
cd java
echo "Running linting..."
docker run --rm -v $(pwd):/workspace ncpc2025-java-lint
echo ""
echo "Running tests..."
./test_all.sh
cd ..
echo ""

echo "All linting and tests completed!"