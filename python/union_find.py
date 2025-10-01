"""
Union-find (disjoint-set union, DSU) maintains a collection of disjoint sets under two operations:

* find(x): return the representative (root) of the set containing x.
* union(x, y): merge the sets containing x and y.

Time complexity: O(alpha(n)) per operation with path compression and union by rank,
where alpha is the inverse Ackermann function (effectively constant for practical purposes).
"""

from __future__ import annotations

# Don't use annotations during contest
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from typing_extensions import Self


class UnionFind:
    def __init__(self) -> None:
        self.parent = self
        self.rank = 0

    def merge(self, other: Self) -> None:
        """Override to define custom merge behavior when sets are united."""

    def find(self) -> Self:
        """Return root of this set with path compression."""
        if self.parent == self:
            return self
        self.parent = self.parent.find()
        return cast("Self", self.parent)

    def union(self, other: Self) -> Self:
        """Unite sets containing self and other. Returns the new root."""
        x = self.find()
        y = other.find()
        if x is y:
            return x
        if x.rank < y.rank:
            x.parent = y
            y.merge(x)
            return y
        if x.rank > y.rank:
            y.parent = x
            x.merge(y)
            return x
        x.parent = y
        y.merge(x)
        y.rank += 1
        return y


class Test(UnionFind):
    """Better to modify copy of UnionFind class and avoid having to type cast everywhere."""

    def __init__(self) -> None:
        super().__init__()
        self.size = 1

    def merge(self, other: Self) -> None:
        assert isinstance(other, Test)
        self.size += other.size


def test_main() -> None:
    a, b, c = Test(), Test(), Test()
    d = a.union(b)
    e = d.union(c)
    assert e.find().size == 3
    assert a.find().size == 3


# Don't write tests below during competition.


def test_single_element() -> None:
    a = Test()
    assert a.find() is a
    assert a.size == 1


def test_union_same_set() -> None:
    a = Test()
    b = Test()
    a.union(b)
    # Unioning again should be safe
    root = a.union(b)
    assert a.find() is b.find()
    assert root.size == 2


def test_multiple_unions() -> None:
    nodes = [Test() for _ in range(10)]
    # Chain union: 0-1-2-3-4-5-6-7-8-9
    for i in range(9):
        nodes[i].union(nodes[i + 1])

    # All should have same root
    root = nodes[0].find()
    for node in nodes:
        assert node.find() is root

    assert root.size == 10


def test_union_order_independence() -> None:
    # Test that union order doesn't affect final result
    a1, b1, c1 = Test(), Test(), Test()
    a1.union(b1).union(c1)
    root1 = a1.find()

    a2, b2, c2 = Test(), Test(), Test()
    c2.union(b2).union(a2)
    root2 = a2.find()

    assert root1.size == root2.size == 3


def test_disconnected_sets() -> None:
    # Create two separate sets
    a, b = Test(), Test()
    c, d = Test(), Test()

    a.union(b)
    c.union(d)

    assert a.find() is b.find()
    assert c.find() is d.find()
    assert a.find() is not c.find()

    assert a.find().size == 2
    assert c.find().size == 2


def test_large_set() -> None:
    # Create a large union-find structure
    nodes = [Test() for _ in range(100)]

    # Union in pairs
    for i in range(0, 100, 2):
        nodes[i].union(nodes[i + 1])

    # Now we have 50 sets of size 2
    roots = set()
    for node in nodes:
        roots.add(id(node.find()))
    assert len(roots) == 50

    # Union all pairs together
    for i in range(0, 100, 4):
        if i + 2 < 100:
            nodes[i].union(nodes[i + 2])

    # Now we have 25 sets of size 4
    roots = set()
    for node in nodes:
        roots.add(id(node.find()))
    assert len(roots) == 25


def main() -> None:
    test_single_element()
    test_union_same_set()
    test_multiple_unions()
    test_union_order_independence()
    test_disconnected_sets()
    test_large_set()
    test_main()


if __name__ == "__main__":
    main()
