#!/bin/bash
# Check Java code quality without modifying files

set -e

ALGORITHM=$1

if [ -n "$ALGORITHM" ]; then
    # Lint specific algorithm
    if [ ! -f "${ALGORITHM}.java" ]; then
        echo "Error: ${ALGORITHM}.java not found"
        exit 1
    fi

    echo "Linting ${ALGORITHM}.java..."

    # Run linting in Docker
    docker run --rm -v $(pwd):/workspace ncpc2025-java-lint bash -c "
        # Check formatting
        echo 'Checking code formatting...'
        if ! java -jar /opt/tools/google-java-format.jar --aosp --dry-run --set-exit-if-changed ${ALGORITHM}.java >/dev/null 2>&1; then
            echo 'Formatting issues found in ${ALGORITHM}.java'
            echo ''
            echo 'To fix formatting issues, run: ./lint_auto_fix.sh ${ALGORITHM}'
            exit 1
        fi

        # Run checkstyle analysis
        echo 'Running checkstyle static analysis...'
        if ! java -jar /opt/tools/checkstyle.jar -c checkstyle.xml ${ALGORITHM}.java; then
            echo 'Checkstyle issues found!'
            exit 1
        fi

        echo '✓ ${ALGORITHM} linting passed!'
    "
else
    # Lint all files
    echo "Running Java linting and formatting..."

    # Run linting in Docker
    docker run --rm -v $(pwd):/workspace ncpc2025-java-lint bash -c "
        # Check formatting
        echo 'Checking Java code formatting...'
        FORMAT_ISSUES=0

        for file in *.java; do
            if ! java -jar /opt/tools/google-java-format.jar --aosp --dry-run --set-exit-if-changed \$file >/dev/null 2>&1; then
                echo \"Formatting issues found in \$file\"
                FORMAT_ISSUES=1
            fi
        done

        if [ \$FORMAT_ISSUES -eq 1 ]; then
            echo ''
            echo 'To fix formatting issues, run: ./lint_auto_fix.sh'
            exit 1
        fi

        echo 'All Java formatting checks passed!'

        # Run checkstyle analysis
        echo 'Running checkstyle static analysis...'
        if ! java -jar /opt/tools/checkstyle.jar -c checkstyle.xml *.java; then
            echo 'Checkstyle issues found!'
            exit 1
        fi

        echo 'All checkstyle static analysis passed!'
        echo '✓ Java linting completed successfully!'
    "
fi
