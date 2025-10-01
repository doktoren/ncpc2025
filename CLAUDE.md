# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a collection of data structure implementations optimized for programming competitions (specifically NCPC 2025). The algorithms are designed to be printed on paper and typed quickly during contests, with minimal character count being crucial.

**Key constraints**:
- Python 3.9.18 is locked for NCPC 2025 competition environment compatibility
- C++ (g++ version 13.2.0) with compiler flags: `-x c++ -g -O2 -std=gnu++20 -static {files}`
- Java (OpenJDK 21.0.4) with compiler flags: `-encoding UTF-8 -sourcepath . -d . {files}` and runtime flags: `-Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms1024m -Xmx1024m`

**CRITICAL: Cross-Language Synchronization**:
All algorithms MUST be kept in sync across Python, C++, and Java implementations:
- Same functionality and API surface
- Same test cases with identical expected values
- Same edge case handling
- Same complexity guarantees
- Consistent documentation and comments

## Development Commands

**Primary development workflow:**
```bash
./test_all.sh  # Test all algorithms (Python + C++ + Java)
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

# Test Java algorithms (containerized)
cd java && ./test_all.sh

# Test individual Java algorithm
cd java && ./test_single.sh <algorithm>

# Python linting
./lint.sh
```

## Code Architecture

### Competition-Optimized Structure
Each module follows a strict structure optimized for competition typing:

1. **Implementation** (classes/algorithms)
2. **`test_main()`** (Python), `testMain()` (Java), or `test_main()` (C++) - The ONLY function to type during competition
3. **Competition barrier**:
   - Python: `# Don't write tests below during competition.`
   - Java: `// Don't write tests below during competition.`
   - C++: `// Don't write tests below during competition.`
4. **Development tests** (comprehensive test suite)
5. **`main()` function** calling all tests with `test_main()`/`testMain()` last

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
- `polygon_area.py` - Shoelace formula for polygon area

**C++ (`cpp/`):**
- `fenwick_tree.cpp` - Binary Indexed Tree template implementation
- `priority_queue.cpp` - Generic priority queue with update/remove operations
- `union_find.cpp` - Disjoint Set Union with inheritance-based design
- `prefix_tree.cpp` - Trie with prefix matching capabilities
- `edmonds_karp.cpp` - Maximum flow algorithm using adjacency matrix
- `bipartite_match.cpp` - Maximum bipartite matching
- `segment_tree.cpp` - Range query data structure
- `dijkstra.cpp` - Shortest path algorithm
- `topological_sort.cpp` - DAG ordering algorithm
- `kmp.cpp` - String matching algorithm
- `lca.cpp` - Lowest Common Ancestor with binary lifting
- `polygon_area.cpp` - Shoelace formula for polygon area

**Java (`java/`):**
- `fenwick_tree.java` - Binary Indexed Tree implementation
- `priority_queue.java` - Generic heap with update/remove operations
- `union_find.java` - Disjoint Set Union with path compression and union by rank
- `prefix_tree.java` - Trie for string prefix operations
- `edmonds_karp.java` - Maximum flow algorithm
- `bipartite_match.java` - Maximum bipartite matching
- `segment_tree.java` - Range query data structure
- `dijkstra.java` - Shortest path algorithm
- `topological_sort.java` - DAG ordering algorithm
- `kmp.java` - String matching algorithm
- `lca.java` - Lowest Common Ancestor with binary lifting
- `polygon_area.java` - Shoelace formula for polygon area

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

**Java:**
- Generic implementations with bounded type parameters
- Standard library collections (ArrayList, HashMap, PriorityQueue)
- Static methods within classes matching filename
- Exception-based error handling with descriptive messages

### Competition Guidelines

**What to type during contest:**

**Python:**
1. Copy implementation classes/functions
2. Copy `test_main()` function only
3. **Skip all typing imports** (marked with `# Don't use annotations during contest`)

**Java:**
1. Copy implementation classes/functions
2. Copy `testMain()` function only
3. Include necessary imports (`import` statements)

**C++:**
1. Copy implementation classes/functions
2. Copy `test_main()` function only
3. Include necessary headers (`#include` statements)

**What NOT to type:**

**Python:**
- Any `from typing` imports or type annotations
- Any tests below the competition barrier comment

**Java:**
- Any tests below the competition barrier comment
- Unnecessary imports or debugging code

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

**Java:**
Uses standard Java features for clean, efficient code:
- Generics with bounded type parameters (e.g., `<T extends Comparable<T>>`)
- Standard library collections (ArrayList, HashMap, PriorityQueue, etc.)
- Static methods within classes (no instances needed)
- Import statements only for java.util.* when needed

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

**Java:**
```bash
# Test all algorithms (containerized - recommended)
cd java && ./test_all.sh

# Test single algorithm (containerized)
cd java && ./test_single.sh fenwick_tree
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

Both C++ and Java implementations include Docker setups that ensure consistent compilation and testing across different environments:

**Java Files:**
- `java/Dockerfile` - Container definition with OpenJDK 21 and NCPC competition flags
- `java/test_all.sh` - Script to test all algorithms with smart caching
- `java/test_single.sh` - Script to test individual algorithms in Docker

**Java Benefits:**
- Exact JDK version matching NCPC 2025 environment
- Consistent flag application: `-encoding UTF-8 -sourcepath . -d .` (compile) and `-Dfile.encoding=UTF-8 -XX:+UseSerialGC -Xss64m -Xms1024m -Xmx1024m` (runtime)
- Isolated testing environment
- Portable across different host systems
- Smart caching to avoid unnecessary rebuilds
- Parallel compilation for fast testing

**C++ Files:**
- `cpp/Dockerfile` - Container definition with g++ 13.2.0 and NCPC competition flags
- `cpp/test_all.sh` - Script to test all algorithms with smart caching
- `cpp/test_single.sh` - Script to test individual algorithms in Docker

**C++ Benefits:**
- Exact compiler version matching NCPC 2025 environment
- Consistent flag application: `-x c++ -g -O2 -std=gnu++20 -static`
- Isolated testing environment
- Portable across different host systems
- Smart caching to avoid unnecessary rebuilds
- Parallel compilation for fast testing

**Usage:**
```bash
# Test all Java algorithms
cd java && ./test_all.sh

# Test specific Java algorithm
cd java && ./test_single.sh fenwick_tree

# Test all C++ algorithms
cd cpp && ./test_all.sh

# Test specific C++ algorithm
cd cpp && ./test_single.sh fenwick_tree

# Interactive development
cd cpp && docker run -it --rm -v $(pwd):/workspace gcc:13.2.0 bash
cd java && docker run -it --rm -v $(pwd):/workspace openjdk:21-slim bash
```

### Memory Management (C++)

All C++ implementations follow RAII principles:
- Destructors automatically clean up resources
- Smart pointers used where dynamic allocation is necessary
- Stack allocation preferred for performance
- Exception safety guaranteed in all operations

### Performance Considerations

All three language implementations (Python, Java, C++) are optimized for:
- Minimal code size for fast typing during competition
- Optimal algorithmic complexity
- Clear, readable structure for debugging under pressure
- Comprehensive test coverage to catch errors early

Performance hierarchy:
- C++ typically offers best runtime performance
- Java offers good performance with simpler syntax than C++
- Python may be fastest to implement correctly under time pressure