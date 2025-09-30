# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a collection of data structure implementations optimized for programming competitions (specifically NCPC 2025). The algorithms are designed to be printed on paper and typed quickly during contests, with minimal character count being crucial.

**Key constraints**:
- Python 3.9.18 is locked for NCPC 2025 competition environment compatibility
- C++ (g++ version 13.2.0) with compiler flags: `-x c++ -g -O2 -std=gnu++20 -static {files}`

## Development Commands

**Primary development workflow:**
```bash
./test_all.sh  # Test all algorithms (Python + C++)
./lint.sh      # Python linting, type checking, and testing
```

**Individual commands:**
```bash
# Setup Python dependencies
uv sync --no-install-project

# Test Python algorithms only
cd python && python3 <algorithm>.py

# Test C++ algorithms (containerized)
cd cpp && ./test_all.sh

# Test individual C++ algorithm
cd cpp && ./test_single.sh <algorithm>

# Python linting
./lint.sh
```

## Code Architecture

### Competition-Optimized Structure
Each module follows a strict structure optimized for competition typing:

1. **Implementation** (classes/algorithms)
2. **`test_main()`** - The ONLY function to type during competition
3. **Competition barrier**: `// Don't write tests below during competition.` (C++) or `# Don't write tests below during competition.` (Python)
4. **Development tests** (comprehensive test suite)
5. **`main()` function** calling all tests with `test_main()` last

### Module-Specific Architecture

**Data Structures Available:**

**Python (`python/`):**
- `fenwick_tree.py` - Binary Indexed Tree with O(n) from_array construction
- `priority_queue.py` - Generic heap with update/remove operations
- `union_find.py` - Disjoint Set Union with path compression and union by rank
- `prefix_tree.py` - Trie for string prefix operations
- `edmonds_karp.py` - Maximum flow algorithm
- `bipartite_match.py` - Maximum bipartite matching
- `segment_tree.py` - Range query data structure
- `dijkstra.py` - Shortest path algorithm
- `topological_sort.py` - DAG ordering algorithm
- `kmp.py` - String matching algorithm
- `lca.py` - Lowest Common Ancestor queries

**C++ (`cpp/`):**
- `fenwick_tree.cpp` - Binary Indexed Tree template implementation
- `priority_queue.cpp` - Generic priority queue with update/remove operations
- `union_find.cpp` - Disjoint Set Union with inheritance-based design
- `prefix_tree.cpp` - Trie with prefix matching capabilities
- `edmonds_karp.cpp` - Maximum flow algorithm using adjacency matrix

**Key Design Patterns:**

**Python:**
- Generic implementations using protocols (e.g., `Summable`, `Comparable`)
- `Self` return types for proper inheritance support
- `Final` annotations for immutable fields
- Consistent error handling with descriptive messages

**C++:**
- Template-based generic implementations
- RAII for automatic resource management
- STL container usage for efficiency
- Exception-based error handling

### Competition Guidelines

**What to type during contest:**

**Python:**
1. Copy implementation classes/functions
2. Copy `test_main()` function only
3. **Skip all typing imports** (marked with `# Don't use annotations during contest`)

**C++:**
1. Copy implementation classes/functions
2. Copy `test_main()` function only
3. Include necessary headers (`#include` statements)

**What NOT to type:**

**Python:**
- Any `from typing` imports or type annotations
- Any tests below the competition barrier comment

**C++:**
- Any tests below the competition barrier comment
- Unnecessary includes or debugging code

**Test Design:**
- `test_main()` functions use multi-digit expected values (12, 39, etc.) to catch real implementation errors
- Multiple assertions per test to verify different aspects
- No verbose output - silent success, clear failure via assertions

### Type System Usage

**Python:**
The codebase uses advanced typing features for development but they should be completely skipped during competition:
- Protocol-based generics for flexible implementations
- `Self` return types for inheritance-safe APIs
- `Final` annotations for immutable fields
- `TYPE_CHECKING` blocks for complex type relationships

All modules include `# Don't use annotations during contest` comments above typing imports as clear reminders.

**C++:**
Uses modern C++20 features for clean, efficient code:
- Template metaprogramming for generic algorithms
- Auto type deduction where appropriate
- Range-based for loops for readability
- Smart pointers for automatic memory management

### Compilation and Testing

**Python:**
```bash
# Run all tests
python3 python/fenwick_tree.py

# Lint and type check
./lint.sh
```

**C++:**
```bash
# Test all algorithms (containerized - recommended)
cd cpp && ./test_all.sh

# Test single algorithm (containerized)
cd cpp && ./test_single.sh fenwick_tree

# Direct compilation (requires g++ 13.2.0)
cd cpp && g++ -x c++ -g -O2 -std=gnu++20 -static fenwick_tree.cpp -o fenwick_tree && ./fenwick_tree
```

### Docker Environment

The C++ implementations include a Docker setup that ensures consistent compilation and testing across different environments:

**Files:**
- `cpp/Dockerfile` - Container definition with g++ 13.2.0 and NCPC competition flags
- `cpp/test_single.sh` - Script to test individual algorithms in Docker

**Benefits:**
- Exact compiler version matching NCPC 2025 environment
- Consistent flag application: `-x c++ -g -O2 -std=gnu++20 -static`
- Isolated testing environment
- Portable across different host systems

**Usage:**
```bash
# Test all algorithms
cd cpp && docker build -t ncpc-cpp . && docker run --rm ncpc-cpp

# Test specific algorithm
cd cpp && ./test_single.sh fenwick_tree

# Interactive development
cd cpp && docker run -it --rm -v $(pwd):/workspace gcc:13.2.0 bash
```

### Memory Management (C++)

All C++ implementations follow RAII principles:
- Destructors automatically clean up resources
- Smart pointers used where dynamic allocation is necessary
- Stack allocation preferred for performance
- Exception safety guaranteed in all operations

### Performance Considerations

Both Python and C++ implementations are optimized for:
- Minimal code size for fast typing during competition
- Optimal algorithmic complexity
- Clear, readable structure for debugging under pressure
- Comprehensive test coverage to catch errors early

The C++ versions typically offer better performance but Python versions may be faster to implement correctly under time pressure.