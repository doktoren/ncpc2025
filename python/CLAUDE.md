# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is a collection of data structure implementations optimized for programming competitions (specifically NCPC 2025). The algorithms are designed to be printed on paper and typed quickly during contests, with minimal character count being crucial.

**Key constraint**: Python 3.9.18 is locked for NCPC 2025 competition environment compatibility.

## Development Commands

**Primary development workflow:**
```bash
./lint.sh  # Runs complete linting, type checking, and testing pipeline
```

**Individual commands:**
```bash
# Setup dependencies
uv sync --no-install-project

# Linting
./lint.sh
```

## Code Architecture

### Competition-Optimized Structure
Each module follows a strict structure optimized for competition typing:

1. **Implementation** (classes/algorithms)
2. **`test_main()`** - The ONLY function to type during competition
3. **Competition barrier**: `# Don't write tests below during competition.`
4. **Development tests** (comprehensive test suite)
5. **`main()` function** calling all tests with `test_main()` last

### Module-Specific Architecture

**Data Structures Available:**
- `fenwick_tree.py` - Binary Indexed Tree with O(n) from_array construction
- `priority_queue.py` - Generic heap with update/remove operations
- `union_find.py` - Disjoint Set Union with path compression and union by rank
- `prefix_tree.py` - Trie for string prefix operations
- `edmonds_karp.py` - Maximum flow algorithm
- `bipartite_match.py` - Maximum bipartite matching

**Key Design Patterns:**
- Generic implementations using protocols (e.g., `Summable`, `Comparable`)
- `Self` return types for proper inheritance support
- `Final` annotations for immutable fields
- Consistent error handling with descriptive messages

### Competition Guidelines

**What to type during contest:**
1. Copy implementation classes/functions
2. Copy `test_main()` function only
3. **Skip all typing imports** (marked with `# Don't use annotations during contest`)

**What NOT to type:**
- Any `from typing` imports or type annotations
- Any tests below the competition barrier comment

**Test Design:**
- `test_main()` functions use multi-digit expected values (12, 39, etc.) to catch real implementation errors
- Multiple assertions per test to verify different aspects
- No verbose output - silent success, clear failure via assertions

### Type System Usage

The codebase uses advanced typing features for development but they should be completely skipped during competition:
- Protocol-based generics for flexible implementations
- `Self` return types for inheritance-safe APIs
- `Final` annotations for immutable fields
- `TYPE_CHECKING` blocks for complex type relationships

All modules include `# Don't use annotations during contest` comments above typing imports as clear reminders.
