"""
Skip list is a probabilistic data structure that maintains a sorted collection of elements.

It uses multiple levels of linked lists to achieve O(log n) average time complexity for
search, insertion, and deletion operations. Elements are inserted with randomly determined
heights, creating express lanes for faster traversal.

Standard library alternatives:
- C++: std::set / std::map (red-black tree, O(log n) guaranteed)
- Python: No built-in sorted set (use bisect module for sorted lists)
- Java: TreeSet / TreeMap (red-black tree, O(log n) guaranteed)

Time complexity: O(log n) average for search, insert, and delete operations.
Space complexity: O(n) on average, where n is the number of elements.
"""

# Don't use annotations during contest
from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from typing_extensions import Self

import random

T = TypeVar("T")


class SkipListNode(Generic[T]):
    def __init__(self, value: T | None, level: int) -> None:
        self.value: T | None = value
        self.forward: list[SkipListNode[T] | None] = [None] * (level + 1)


class SkipList(Generic[T]):
    """Probabilistic data structure for sorted elements with O(log n) operations."""

    def __init__(self, max_level: int = 16, p: float = 0.5) -> None:
        self.max_level = max_level
        self.p = p
        self.level = 0
        self.header: SkipListNode[T] = SkipListNode(None, max_level)

    def _random_level(self) -> int:
        level = 0
        while random.random() < self.p and level < self.max_level:  # noqa: S311
            level += 1
        return level

    def insert(self, value: T) -> Self:
        update: list[SkipListNode[T] | None] = [None] * (self.max_level + 1)
        current: SkipListNode[T] = self.header

        for i in range(self.level, -1, -1):
            while (
                current.forward[i] is not None and current.forward[i].value < value  # type: ignore[union-attr, operator]
            ):
                current = current.forward[i]  # type: ignore[assignment]
            update[i] = current

        level = self._random_level()
        if level > self.level:
            for i in range(self.level + 1, level + 1):
                update[i] = self.header
            self.level = level

        new_node: SkipListNode[T] = SkipListNode(value, level)
        for i in range(level + 1):
            new_node.forward[i] = update[i].forward[i]  # type: ignore[union-attr]
            update[i].forward[i] = new_node  # type: ignore[union-attr]

        return self

    def search(self, value: T) -> bool:
        current: SkipListNode[T] = self.header
        for i in range(self.level, -1, -1):
            while (
                current.forward[i] is not None and current.forward[i].value < value  # type: ignore[union-attr, operator]
            ):
                current = current.forward[i]  # type: ignore[assignment]
        current = current.forward[0]  # type: ignore[assignment]
        return current is not None and current.value == value

    def delete(self, value: T) -> bool:
        update: list[SkipListNode[T] | None] = [None] * (self.max_level + 1)
        current: SkipListNode[T] = self.header

        for i in range(self.level, -1, -1):
            while (
                current.forward[i] is not None and current.forward[i].value < value  # type: ignore[union-attr, operator]
            ):
                current = current.forward[i]  # type: ignore[assignment]
            update[i] = current

        current = current.forward[0]  # type: ignore[assignment]
        if current is None or current.value != value:
            return False

        for i in range(self.level + 1):
            if update[i].forward[i] != current:  # type: ignore[union-attr]
                break
            update[i].forward[i] = current.forward[i]  # type: ignore[union-attr]

        while self.level > 0 and self.header.forward[self.level] is None:
            self.level -= 1

        return True

    # Optional functionality (not always needed during competition)

    def __len__(self) -> int:
        count = 0
        current = self.header.forward[0]
        while current is not None:
            count += 1
            current = current.forward[0]
        return count

    def to_list(self) -> list[T]:
        result: list[T] = []
        current = self.header.forward[0]
        while current is not None:
            result.append(current.value)  # type: ignore[arg-type]
            current = current.forward[0]
        return result

    def __contains__(self, value: T) -> bool:
        return self.search(value)


def test_main() -> None:
    random.seed(42)
    sl: SkipList[int] = SkipList()
    sl.insert(10).insert(20).insert(5).insert(15)
    assert sl.search(10)
    assert sl.search(20)
    assert not sl.search(25)
    assert sl.delete(10)
    assert not sl.search(10)
    assert not sl.delete(30)

    # Optional functionality (not always needed during competition)
    random.seed(42)
    sl2: SkipList[int] = SkipList()
    sl2.insert(3).insert(1).insert(4).insert(1).insert(5)
    assert len(sl2) == 5
    assert sl2.to_list() == [1, 1, 3, 4, 5]
    assert 3 in sl2
    assert 7 not in sl2


# Don't write tests below during competition.


def test_basic_operations() -> None:
    random.seed(123)
    sl: SkipList[int] = SkipList()
    assert not sl.search(1)
    sl.insert(5)
    assert sl.search(5)
    assert not sl.search(4)


def test_multiple_inserts() -> None:
    random.seed(456)
    sl: SkipList[int] = SkipList()
    values = [10, 5, 15, 3, 7, 12, 20]
    for v in values:
        sl.insert(v)
    for v in values:
        assert sl.search(v)
    assert not sl.search(1)
    assert not sl.search(100)


def test_delete_operations() -> None:
    random.seed(789)
    sl: SkipList[int] = SkipList()
    sl.insert(10).insert(20).insert(30)
    assert sl.delete(20)
    assert not sl.search(20)
    assert sl.search(10)
    assert sl.search(30)
    assert not sl.delete(20)
    assert not sl.delete(40)


def test_duplicate_values() -> None:
    random.seed(101)
    sl: SkipList[int] = SkipList()
    sl.insert(5).insert(5).insert(5)
    assert len(sl) == 3
    result = sl.to_list()
    assert result == [5, 5, 5]


def test_ordered_insertion() -> None:
    random.seed(202)
    sl: SkipList[int] = SkipList()
    for i in range(1, 11):
        sl.insert(i)
    assert sl.to_list() == list(range(1, 11))


def test_reverse_insertion() -> None:
    random.seed(303)
    sl: SkipList[int] = SkipList()
    for i in range(10, 0, -1):
        sl.insert(i)
    assert sl.to_list() == list(range(1, 11))


def test_empty_skiplist() -> None:
    random.seed(404)
    sl: SkipList[int] = SkipList()
    assert len(sl) == 0
    assert sl.to_list() == []
    assert not sl.delete(5)


def test_strings() -> None:
    random.seed(505)
    sl: SkipList[str] = SkipList()
    sl.insert("dog").insert("cat").insert("bird").insert("ant")
    assert sl.search("cat")
    assert sl.to_list() == ["ant", "bird", "cat", "dog"]


def main() -> None:
    test_basic_operations()
    test_multiple_inserts()
    test_delete_operations()
    test_duplicate_values()
    test_ordered_insertion()
    test_reverse_insertion()
    test_empty_skiplist()
    test_strings()
    test_main()


if __name__ == "__main__":
    main()
