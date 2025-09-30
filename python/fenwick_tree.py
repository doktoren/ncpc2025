"""
Fenwick tree (Binary Indexed Tree) for efficient range sum queries and point updates.

A Fenwick tree maintains cumulative frequency information and supports two main operations:
* update(i, delta): add delta to the element at index i
* query(i): return the sum of elements from index 0 to i (inclusive)
* range_query(left, right): return the sum of elements from left to right (inclusive)

The tree uses a clever indexing scheme based on the binary representation of indices
to achieve logarithmic time complexity for both operations.

Time complexity: O(log n) for update and query operations.
Space complexity: O(n) where n is the size of the array.
"""

from __future__ import annotations

# Don't use annotations during contest
from typing import Final, Generic, Protocol, TypeVar

from typing_extensions import Self


class Summable(Protocol):
    def __add__(self, other: Self, /) -> Self: ...
    def __sub__(self, other: Self, /) -> Self: ...


ValueT = TypeVar("ValueT", bound=Summable)


class FenwickTree(Generic[ValueT]):
    def __init__(self, size: int, zero: ValueT) -> None:
        self.size: Final = size
        self.zero: Final = zero
        # 1-indexed tree for easier bit manipulation
        self.tree: list[ValueT] = [zero] * (size + 1)

    @classmethod
    def from_array(cls, arr: list[ValueT], zero: ValueT) -> Self:
        """Create a Fenwick tree from an existing array in O(n) time."""
        n = len(arr)
        tree = cls(n, zero)

        # Compute prefix sums
        prefix = [zero] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + arr[i]

        # Build tree in O(n): each tree[i] contains sum of range [i - (i & -i) + 1, i]
        for i in range(1, n + 1):
            range_start = i - (i & (-i)) + 1
            tree.tree[i] = prefix[i] - prefix[range_start - 1]

        return tree

    def update(self, index: int, delta: ValueT) -> None:
        """Add delta to the element at the given index."""
        if not (0 <= index < self.size):
            msg = f"Index {index} out of bounds for size {self.size}"
            raise IndexError(msg)

        # Convert to 1-indexed
        index += 1
        while index <= self.size:
            self.tree[index] = self.tree[index] + delta
            # Move to next index by adding the lowest set bit
            index += index & (-index)

    def query(self, index: int) -> ValueT:
        """Return the sum of elements from 0 to index (inclusive)."""
        if not (0 <= index < self.size):
            msg = f"Index {index} out of bounds for size {self.size}"
            raise IndexError(msg)

        # Convert to 1-indexed
        index += 1
        result = self.zero
        while index > 0:
            result = result + self.tree[index]
            # Move to parent by removing the lowest set bit
            index -= index & (-index)
        return result

    def range_query(self, left: int, right: int) -> ValueT:
        """Return the sum of elements from left to right (inclusive)."""
        if left > right:
            return self.zero
        if left == 0:
            return self.query(right)
        return self.query(right) - self.query(left - 1)

    def get_value(self, index: int) -> ValueT:
        """Get the current value at a specific index."""
        if index == 0:
            return self.query(0)
        return self.query(index) - self.query(index - 1)

    def __len__(self) -> int:
        return self.size


def test_main() -> None:
    f = FenwickTree(5, 0)
    f.update(0, 7)
    f.update(2, 13)
    f.update(4, 19)
    assert f.query(4) == 39
    assert f.range_query(1, 3) == 13
    assert f.get_value(2) == 13


# Don't write tests below during competition.


def test_basic() -> None:
    # Test with integers
    ft = FenwickTree(5, 0)

    # Initial array: [0, 0, 0, 0, 0]
    assert ft.query(0) == 0
    assert ft.query(4) == 0
    assert ft.range_query(1, 3) == 0

    # Update operations
    ft.update(0, 5)  # [5, 0, 0, 0, 0]
    ft.update(2, 3)  # [5, 0, 3, 0, 0]
    ft.update(4, 7)  # [5, 0, 3, 0, 7]

    # Query operations
    assert ft.query(0) == 5
    assert ft.query(2) == 8  # 5 + 0 + 3
    assert ft.query(4) == 15  # 5 + 0 + 3 + 0 + 7

    # Range queries
    assert ft.range_query(0, 2) == 8
    assert ft.range_query(2, 4) == 10
    assert ft.range_query(1, 3) == 3

    # Get individual values
    assert ft.get_value(0) == 5
    assert ft.get_value(2) == 3
    assert ft.get_value(4) == 7


def test_from_array() -> None:
    arr = [1, 3, 5, 7, 9, 11]
    ft = FenwickTree.from_array(arr, 0)

    # Test that prefix sums match
    expected_sum = 0
    for i in range(len(arr)):
        expected_sum += arr[i]
        assert ft.query(i) == expected_sum

    # Test range queries
    assert ft.range_query(1, 3) == 3 + 5 + 7  # 15
    assert ft.range_query(2, 4) == 5 + 7 + 9  # 21

    # Test updates
    ft.update(2, 10)  # arr[2] becomes 15
    assert ft.get_value(2) == 15
    assert ft.range_query(1, 3) == 3 + 15 + 7  # 25


def test_edge_cases() -> None:
    ft = FenwickTree(1, 0)

    # Single element tree
    ft.update(0, 42)
    assert ft.query(0) == 42
    assert ft.range_query(0, 0) == 42
    assert ft.get_value(0) == 42

    # Empty range
    ft_large = FenwickTree(10, 0)
    assert ft_large.range_query(5, 3) == 0  # left > right


def test_negative_values() -> None:
    ft = FenwickTree(4, 0)

    # Mix of positive and negative updates
    ft.update(0, 10)
    ft.update(1, -5)
    ft.update(2, 8)
    ft.update(3, -3)

    assert ft.query(3) == 10  # 10 + (-5) + 8 + (-3)
    assert ft.range_query(1, 2) == 3  # (-5) + 8

    # Update with negative delta
    ft.update(0, -5)  # Subtract 5 from position 0
    assert ft.get_value(0) == 5
    assert ft.query(3) == 5  # 5 + (-5) + 8 + (-3)


def test_linear_from_array() -> None:
    """Test that the optimized from_array produces identical results."""
    import time

    # Test arrays of different sizes
    test_cases = [
        [1, 3, 5, 7, 9, 11],
        [10, -5, 8, -3, 15, 2, -7, 12],
        list(range(100)),
    ]

    for arr in test_cases:
        ft = FenwickTree.from_array(arr, 0)

        # Verify all prefix sums match expected
        expected_sum = 0
        for i in range(len(arr)):
            expected_sum += arr[i]
            assert ft.query(i) == expected_sum, f"Mismatch at index {i}"

        # Verify individual values
        for i in range(len(arr)):
            assert ft.get_value(i) == arr[i], f"Value mismatch at index {i}"

        # Test range queries
        if len(arr) >= 3:
            assert ft.range_query(1, 2) == sum(arr[1:3])

    # Simple performance comparison for large array
    large_arr = list(range(1000))

    # Time the optimized version (should be faster)
    start = time.perf_counter()
    ft_optimized = FenwickTree.from_array(large_arr, 0)
    optimized_time = time.perf_counter() - start

    # Verify correctness on large array
    for i in [0, 100, 500, 999]:
        expected = sum(large_arr[:i + 1])
        assert ft_optimized.query(i) == expected

    print(f"Linear from_array time for 1000 elements: {optimized_time:.6f}s")


def main() -> None:
    test_basic()
    test_from_array()
    test_edge_cases()
    test_negative_values()
    test_linear_from_array()
    test_main()
    print("All Fenwick tree tests passed!")


if __name__ == "__main__":
    main()
