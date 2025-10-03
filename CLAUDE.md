# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a collection of data structure implementations optimized for programming competitions (specifically NCPC 2025). The algorithms are designed to be printed on paper and typed quickly during contests, with minimal character count being crucial.

## Development Commands

**Complete workflow:**
```bash
./test_and_lint.sh  # Lint + test all algorithms (Python + C++ + Java)
```

**Standardized script interface** - Each language folder (`python/`, `cpp/`, `java/`) has 3 scripts:

| Script | Purpose | All files | Single file |
|--------|---------|-----------|-------------|
| `lint.sh` | Check code quality | `./lint.sh` | `./lint.sh skiplist` |
| `lint_auto_fix.sh` | Auto-fix formatting | `./lint_auto_fix.sh` | `./lint_auto_fix.sh skiplist` |
| `test.sh` | Run tests | `./test.sh` | `./test.sh skiplist` |

**Examples:**
```bash
# Lint + test everything
./test_and_lint.sh

# Lint specific algorithm
cd cpp && ./lint.sh skiplist

# Auto-fix then test
cd python && ./lint_auto_fix.sh && ./test.sh
```

**Note:** C++ and Java scripts automatically use Docker for exact NCPC 2025 environment compatibility.

## Documentation Generation

**IMPORTANT:** Regenerate PDFs before committing:
```bash
cd docs-generator && ./generate_docs.sh
```

This generates 6 PDF files (Python/C++/Java, each with competition-only and full versions) for printing during contests.

## Code Quality and Linting

**Linting Policy**:
- Do NOT suppress or whitelist new linting errors/warnings without explicit user approval
- Fix the underlying issue instead of suppressing warnings
- Existing suppressions in lint configurations are approved, but new ones require discussion
- All languages enforce a **100-character line limit** for optimal PDF formatting

**Cross-Language Synchronization**:
All algorithms MUST be kept in sync across Python, C++, and Java implementations:
- Same functionality and API surface
- Same test cases with identical expected values
- Same edge case handling
- Same complexity guarantees
- Consistent documentation and comments
- Generic implementations: All data structures should support generic types where applicable (not restrict to int/long unless necessary)
- Basic vs Optional: Separate basic functionality from optional/extending functionality with comment markers

**Type System and Memory Management**:

**Python:**
- Protocol-based generics, `Self` return types, `TYPE_CHECKING` blocks
- All modules include `# Don't use annotations during contest` comments above typing imports
- During competition: Skip all typing imports and type annotations

**C++:**
- Template-based generics, RAII for automatic resource management
- Delete copy/move operations when not needed (prevents warnings and accidental misuse)

**Java:**
- Generics with bounded type parameters (e.g., `<T extends Comparable<T>>`)
- Static methods within classes matching filename

## Code Architecture

### Language Constraints and Modern Practices

**Environment constraints** (NCPC 2025):
- Python 3.9.18
- C++ with g++ 13.2.0, flags: `-x c++ -g -O2 -std=gnu++20 -static {files}`
- Java OpenJDK 21.0.4, flags: `-encoding UTF-8 -sourcepath . -d .` (compile), `-Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms1024m -Xmx1024m` (runtime)

**Coding principle**: Use the most modern, safe, and simple features allowed by these language versions. Leverage all capabilities (generics, type safety, RAII, standard libraries) to write clean, robust code with minimal boilerplate.

### Competition-Optimized Structure
Each module follows a strict structure optimized for competition typing:

1. **File header** (algorithm description)
   - **Python**: Multi-line docstring starting with `"""` describing the algorithm, its key operations, time complexity, and space complexity
   - **C++/Java**: Multi-line comment starting with `/*` describing the algorithm, its key operations, time complexity, and space complexity
   - Format: Brief description, explanation of how it works, time/space complexity analysis
   - Example from fenwick_tree.cpp:
     ```
     /*
     Fenwick tree (Binary Indexed Tree) for efficient range sum queries and point updates.

     A Fenwick tree maintains cumulative frequency information and supports two main operations:
     * update(i, delta): add delta to the element at index i
     * query(i): return the sum of elements from index 0 to i (inclusive)
     ...

     Time complexity: O(log n) for update and query operations.
     Space complexity: O(n) where n is the size of the array.
     */
     ```
2. **Implementation** (classes/algorithms)
   - Basic functionality (core operations needed in most problems)
   - **Optional marker**: `# Optional functionality (not always needed during competition)` (Python) or `// Optional functionality (not always needed during competition)` (C++/Java)
   - Optional/extending functionality (advanced features, helper methods, optimizations)
2. **`test_main()`** (Python), `testMain()` (Java), or `test_main()` (C++) - The ONLY function to type during competition
   - Same split: basic tests, then optional marker, then optional tests
3. **Competition barrier**:
   - Python: `# Don't write tests below during competition.`
   - Java: `// Don't write tests below during competition.`
   - C++: `// Don't write tests below during competition.`
4. **Development tests** (comprehensive test suite)
5. **`main()` function** calling all tests with `test_main()`/`testMain()` last

### Available Algorithms

See [README.md](README.md) for the complete algorithm list.

**IMPORTANT:** When adding new algorithms, update the table in README.md to keep it synchronized across all three languages.

### Test Design Requirements

- `test_main()` functions use multi-digit expected values (12, 39, etc.) to catch real implementation errors
- Multiple assertions per test to verify different aspects
- No verbose output - silent success, clear failure via assertions
- **Function Coverage Requirements:**
  - All implemented public methods MUST be called in `test_main()` (directly or indirectly)
  - If method A calls method B internally and A is tested, B doesn't need separate testing UNLESS A is optional and B is basic
  - Optional methods should be tested if they provide important functionality (e.g., `from_array`, `peek`)
  - The goal: ensure no write-down-from-paper errors by calling every function at least once
