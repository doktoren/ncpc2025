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
        """Override with desired functionality."""

    def find(self) -> Self:
        if self.parent == self:
            return self
        self.parent = self.parent.find()
        return cast("Self", self.parent)

    def union(self, other: Self) -> Self:
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


def main() -> None:
    test_main()


if __name__ == "__main__":
    main()
