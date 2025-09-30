# Dockerfile for NCPC 2025 Java environment
# Uses OpenJDK 21.0.4 with competition-standard flags

FROM openjdk:21-slim

# Set working directory
WORKDIR /workspace

# Install tools (cached layer)
RUN apt-get update && apt-get install -y \
    parallel \
    && rm -rf /var/lib/apt/lists/*

# Copy Java source files
COPY *.java ./

# Create optimized test script with parallel compilation
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Compiling and testing Java algorithms with NCPC 2025 flags..."\n\
echo "Java version: $(java -version 2>&1 | head -n1)"\n\
echo "Compiler flags: -encoding UTF-8 -sourcepath . -d ."\n\
echo "Runtime flags: -Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms1024m -Xmx1024m"\n\
echo ""\n\
\n\
# Compile and test function\n\
compile_and_test() {\n\
    file=$1\n\
    name=$(basename "$file" .java)\n\
    \n\
    # Compile with NCPC flags\n\
    if javac -encoding UTF-8 -sourcepath . -d . "$file" 2>/dev/null; then\n\
        # Run the test with NCPC runtime flags\n\
        if java -Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms1024m -Xmx1024m "$name" >/dev/null 2>&1; then\n\
            echo "  ✓ $name: PASSED"\n\
            return 0\n\
        else\n\
            echo "  ✗ $name: RUNTIME FAILED"\n\
            return 1\n\
        fi\n\
    else\n\
        echo "  ✗ $name: COMPILATION FAILED"\n\
        return 1\n\
    fi\n\
}\n\
export -f compile_and_test\n\
\n\
# Run tests in parallel\n\
failed=0\n\
total=$(ls -1 *.java 2>/dev/null | wc -l)\n\
\n\
if ! ls -1 *.java 2>/dev/null | parallel -j$(nproc) --halt soon,fail=1 compile_and_test; then\n\
    failed=1\n\
fi\n\
\n\
echo ""\n\
if [ $failed -eq 0 ]; then\n\
    echo "Results: $total/$total tests passed"\n\
    echo "All tests PASSED!"\n\
    exit 0\n\
else\n\
    echo "Some tests FAILED!"\n\
    exit 1\n\
fi' > test_all.sh && chmod +x test_all.sh

# Default command runs all tests
CMD ["./test_all.sh"]
