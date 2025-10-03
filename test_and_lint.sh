#!/bin/bash
# Complete test and linting runner for NCPC 2025 algorithms

set -e

echo "Testing and Linting NCPC 2025 Algorithms"
echo "========================================="
echo ""

# Python: Lint + Test
echo "Python algorithms:"
cd python
./lint.sh && ./test.sh
cd ..
echo ""

# C++: Lint + Test
echo "C++ algorithms:"
cd cpp
./lint.sh && ./test.sh
cd ..
echo ""

# Java: Lint + Test
echo "Java algorithms:"
cd java
./lint.sh && ./test.sh
cd ..
echo ""

echo "All linting and tests completed!"
