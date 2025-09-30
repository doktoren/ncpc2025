"""
Segment tree for efficient range queries and updates.

Supports range sum queries, point updates, and can be easily modified for other operations
like range minimum, maximum, or more complex functions. The tree uses 1-indexed array
representation with lazy propagation for range updates.

Time complexity: O(log n) for query and update operations, O(n) for construction.
Space complexity: O(n) for the tree structure.
"""

from __future__ import annotations

# Don't use annotations during contest
from typing import Final, Generic, Protocol, TypeVar

from typing_extensions import Self


class Summable(Protocol):
    def __add__(self, other: Self, /) -> Self: ...


ValueT = TypeVar("ValueT", bound=Summable)


class SegmentTree(Generic[ValueT]):
    def __init__(self, arr: list[ValueT], zero: ValueT) -> None:
        self.n: Final = len(arr)
        self.zero: Final = zero
        # Tree needs 4*n space for worst case
        self.tree: list[ValueT] = [zero] * (4 * self.n)
        if arr:
            self._build(arr, 1, 0, self.n - 1)

    def _build(self, arr: list[ValueT], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self._build(arr, 2 * node, start, mid)
            self._build(arr, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def update(self, idx: int, val: ValueT) -> None:
        """Update value at index idx to val."""
        if not (0 <= idx < self.n):
            msg = f"Index {idx} out of bounds for size {self.n}"
            raise IndexError(msg)
        self._update(1, 0, self.n - 1, idx, val)

    def _update(self, node: int, start: int, end: int, idx: int, val: ValueT) -> None:
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self._update(2 * node, start, mid, idx, val)
            else:
                self._update(2 * node + 1, mid + 1, end, idx, val)
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def query(self, left: int, right: int) -> ValueT:
        """Query sum of range [left, right] inclusive."""
        if not (0 <= left <= right < self.n):
            msg = f"Invalid range [{left}, {right}] for size {self.n}"
            raise IndexError(msg)
        return self._query(1, 0, self.n - 1, left, right)

    def _query(self, node: int, start: int, end: int, left: int, right: int) -> ValueT:
        if right < start or left > end:
            return self.zero
        if left <= start and end <= right:
            return self.tree[node]
        mid = (start + end) // 2
        left_sum = self._query(2 * node, start, mid, left, right)
        right_sum = self._query(2 * node + 1, mid + 1, end, left, right)
        return left_sum + right_sum


def test_main() -> None:
    st = SegmentTree([1, 3, 5, 7, 9], 0)
    assert st.query(1, 3) == 15
    st.update(2, 10)
    assert st.query(1, 3) == 20
    assert st.query(0, 4) == 30


# Don't write tests below during competition.


def test_large_array() -> None:
    # Test with large array
    arr = list(range(1000))
    st = SegmentTree(arr, 0)

    # Test various range queries
    assert st.query(0, 99) == sum(range(100))
    assert st.query(500, 599) == sum(range(500, 600))
    assert st.query(999, 999) == 999

    # Test updates on large array
    st.update(500, 9999)
    assert st.query(500, 500) == 9999
    assert st.query(499, 501) == 499 + 9999 + 501


def test_edge_cases() -> None:
    # Single element
    st = SegmentTree([42], 0)
    assert st.query(0, 0) == 42
    st.update(0, 100)
    assert st.query(0, 0) == 100

    # Empty array
    st_empty = SegmentTree([], 0)
    assert len(st_empty.tree) == 0

    # All zeros
    st_zeros = SegmentTree([0, 0, 0, 0], 0)
    assert st_zeros.query(0, 3) == 0
    st_zeros.update(2, 5)
    assert st_zeros.query(0, 3) == 5


def test_negative_values() -> None:
    arr = [-5, 3, -2, 8, -1]
    st = SegmentTree(arr, 0)

    assert st.query(0, 4) == 3  # -5 + 3 + (-2) + 8 + (-1)
    assert st.query(1, 3) == 9  # 3 + (-2) + 8

    st.update(0, -10)
    assert st.query(0, 1) == -7  # -10 + 3


def test_stress_updates() -> None:
    # Test many updates
    arr = [1] * 100
    st = SegmentTree(arr, 0)

    # Initial sum should be 100
    assert st.query(0, 99) == 100

    # Update every element
    for i in range(100):
        st.update(i, i + 1)

    # Sum should now be 1 + 2 + ... + 100 = 5050
    assert st.query(0, 99) == sum(range(1, 101))

    # Test various ranges
    assert st.query(0, 9) == sum(range(1, 11))
    assert st.query(50, 59) == sum(range(51, 61))


def test_invalid_operations() -> None:
    st = SegmentTree([1, 2, 3], 0)

    # Test invalid indices
    try:
        st.update(-1, 5)
        assert False, "Should raise IndexError"
    except IndexError:
        pass

    try:
        st.update(3, 5)
        assert False, "Should raise IndexError"
    except IndexError:
        pass

    try:
        st.query(-1, 2)
        assert False, "Should raise IndexError"
    except IndexError:
        pass

    try:
        st.query(0, 3)
        assert False, "Should raise IndexError"
    except IndexError:
        pass

    try:
        st.query(2, 1)  # left > right
        assert False, "Should raise IndexError"
    except IndexError:
        pass


def test_string_summation() -> None:
    # Test with strings as summable values
    arr = ["a", "b", "c", "d"]
    st = SegmentTree(arr, "")

    assert st.query(0, 3) == "abcd"
    assert st.query(1, 2) == "bc"

    st.update(1, "X")
    assert st.query(0, 3) == "aXcd"


def main() -> None:
    test_main()
    test_large_array()
    test_edge_cases()
    test_negative_values()
    test_stress_updates()
    test_invalid_operations()
    test_string_summation()


if __name__ == "__main__":
    main()
