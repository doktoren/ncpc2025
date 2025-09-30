#!/bin/bash
# Simple test runner for NCPC 2025 algorithms

set -e

echo "Testing NCPC 2025 Algorithms"
echo "============================"
echo ""

# Test Python algorithms
echo "Python algorithms:"
cd python
for file in *.py; do
    if [ -f "$file" ]; then
        echo "Testing $(basename "$file" .py)..."
        python3 "$file" > /dev/null 2>&1 && echo "  ✓ PASSED" || echo "  ✗ FAILED"
    fi
done
cd ..
echo ""

# Test C++ algorithms
echo "C++ algorithms:"
cd cpp && ./test_all.sh
cd ..
echo ""

echo "All tests completed!"