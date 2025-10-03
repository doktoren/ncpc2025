#!/bin/bash
# Check C++ code quality without modifying files

set -e

ALGORITHM=$1

if [ -n "$ALGORITHM" ]; then
    # Lint specific algorithm
    if [ ! -f "${ALGORITHM}.cpp" ]; then
        echo "Error: ${ALGORITHM}.cpp not found"
        exit 1
    fi

    echo "Linting ${ALGORITHM}.cpp..."

    # Run linting in Docker
    docker run --rm -v $(pwd):/workspace ncpc2025-cpp-lint bash -c "
        # Check formatting
        echo 'Checking code formatting...'
        if ! clang-format --dry-run --Werror ${ALGORITHM}.cpp >/dev/null 2>&1; then
            echo 'Formatting issues found in ${ALGORITHM}.cpp'
            clang-format --dry-run --Werror ${ALGORITHM}.cpp 2>&1 || true
            echo ''
            echo 'To fix formatting issues, run: ./lint_auto_fix.sh ${ALGORITHM}'
            exit 1
        fi

        # Run static analysis
        echo 'Running cppcheck static analysis...'
        if ! cppcheck --enable=warning,performance,portability \
            --suppress=assertWithSideEffect \
            --error-exitcode=1 \
            ${ALGORITHM}.cpp 2>&1; then
            echo 'C++ linting FAILED!'
            exit 1
        fi

        echo '✓ ${ALGORITHM} linting passed!'
    "
else
    # Lint all files
    echo "Running C++ linting and formatting..."

    # Run linting in Docker
    docker run --rm -v $(pwd):/workspace ncpc2025-cpp-lint bash -c "
        # Check formatting
        echo 'Checking C++ code formatting...'
        FORMAT_ISSUES=0

        for file in *.cpp; do
            if ! clang-format --dry-run --Werror \$file >/dev/null 2>&1; then
                echo \"Formatting issues found in \$file\"
                clang-format --dry-run --Werror \$file 2>&1 || true
                FORMAT_ISSUES=1
            fi
        done

        if [ \$FORMAT_ISSUES -eq 1 ]; then
            echo ''
            echo 'To fix formatting issues, run: ./lint_auto_fix.sh'
            exit 1
        fi

        echo 'All C++ formatting checks passed!'

        # Run static analysis
        echo 'Running cppcheck static analysis...'
        if ! cppcheck --enable=warning,performance,portability \
            --suppress=assertWithSideEffect \
            --error-exitcode=1 \
            *.cpp 2>&1; then
            echo 'C++ linting FAILED!'
            exit 1
        fi

        echo 'All cppcheck static analysis passed!'
        echo '✓ C++ linting completed successfully!'
    "
fi
