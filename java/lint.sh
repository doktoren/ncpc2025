#!/bin/bash

set -e

echo "Running Java linting and formatting..."

# Check formatting
echo "Checking Java code formatting..."
FORMAT_ISSUES=0

for file in *.java; do
    if ! java -jar /opt/tools/google-java-format.jar --aosp --dry-run --set-exit-if-changed "$file" >/dev/null 2>&1; then
        echo "Formatting issues found in $file"
        FORMAT_ISSUES=1
    fi
done

if [ "$FORMAT_ISSUES" -eq 1 ]; then
    echo ""
    echo "To fix formatting issues, run: java -jar /opt/tools/google-java-format.jar --aosp --replace *.java"
    exit 1
fi

echo "All Java formatting checks passed!"

# Run checkstyle analysis
echo "Running checkstyle static analysis..."
if ! java -jar /opt/tools/checkstyle.jar -c checkstyle.xml *.java; then
    echo "Checkstyle issues found!"
    exit 1
fi

echo "All checkstyle static analysis passed!"
echo "Java linting completed successfully!"