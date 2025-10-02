#!/bin/bash

set -e

echo "Running C++ linting and formatting..."

# Check formatting
echo "Checking C++ code formatting..."
FORMAT_ISSUES=0

for file in *.cpp; do
    if ! clang-format --dry-run --Werror "$file" >/dev/null 2>&1; then
        echo "Formatting issues found in $file"
        clang-format --dry-run --Werror "$file" 2>&1 || true
        FORMAT_ISSUES=1
    fi
done

if [ "$FORMAT_ISSUES" -eq 1 ]; then
    echo ""
    echo "To fix formatting issues, run: clang-format -i *.cpp"
    exit 1
fi

echo "All C++ formatting checks passed!"

# Run static analysis (more lenient for competition code)
echo "Running cppcheck static analysis..."
# Suppress common false positives for competition code:
# - assertWithSideEffect: common in test code
# - noExplicitConstructor: often not needed in competition
# - unassignedVariable: structured bindings may have unused parts
cppcheck --enable=warning,performance,portability \
    --suppress=assertWithSideEffect \
    --suppress=noExplicitConstructor \
    --suppress=unassignedVariable \
    --suppress=useStlAlgorithm \
    --suppress=stlFindInsert \
    --suppress=passedByValue \
    --suppress=stlIfStrFind \
    --error-exitcode=1 \
    --quiet *.cpp

echo "All cppcheck static analysis passed!"
echo "C++ linting completed successfully!"