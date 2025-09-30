# Dockerfile for NCPC 2025 C++ environment
# Uses g++ 13.2.0 with competition-standard flags

FROM gcc:13.2.0

# Set working directory
WORKDIR /workspace

# Install tools (cached layer)
RUN apt-get update && apt-get install -y \
    make \
    parallel \
    && rm -rf /var/lib/apt/lists/*

# Copy C++ source files
COPY *.cpp ./

# Create optimized test script with parallel compilation
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Compiling and testing C++ algorithms with NCPC 2025 flags..."\n\
echo "Compiler: $(g++ --version | head -n1)"\n\
echo "Flags: -x c++ -g -O2 -std=gnu++20 -static"\n\
echo ""\n\
\n\
# Compile all files in parallel\n\
compile_and_test() {\n\
    file=$1\n\
    name=$(basename "$file" .cpp)\n\
    \n\
    if g++ -x c++ -g -O2 -std=gnu++20 -static "$file" -o "$name" 2>/dev/null; then\n\
        if ./"$name" >/dev/null 2>&1; then\n\
            echo "  ✓ $name: PASSED"\n\
            rm -f "$name"\n\
            return 0\n\
        else\n\
            echo "  ✗ $name: RUNTIME FAILED"\n\
            rm -f "$name"\n\
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
total=$(ls -1 *.cpp 2>/dev/null | wc -l)\n\
\n\
if ! ls -1 *.cpp 2>/dev/null | parallel -j$(nproc) --halt soon,fail=1 compile_and_test; then\n\
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