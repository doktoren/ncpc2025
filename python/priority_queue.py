"""
Priority queue implementation using a binary heap.

This module provides a generic priority queue that supports adding items with priorities,
updating priorities, removing items, and popping the item with the lowest priority.
The implementation uses Python's heapq module for efficient heap operations.

Time complexity: O(log n) for add/update and pop operations, O(log n) for remove.
Space complexity: O(n) where n is the number of items in the queue.
"""

import heapq
import itertools

# Don't use annotations during contest
from typing import Final, Generic, Protocol, TypeVar, cast

from typing_extensions import Self


class Comparable(Protocol):
    def __lt__(self, other: Self, /) -> bool: ...


KeyT = TypeVar("KeyT")
PriorityT = TypeVar("PriorityT", bound=Comparable)


class PriorityQueue(Generic[KeyT, PriorityT]):
    _REMOVED: Final = object()  # placeholder for a removed task

    def __init__(self) -> None:
        self._size = 0
        # list of entries arranged in a heap
        self._pq: list[list[object]] = []
        # mapping of tasks to entries
        self._entry_finder: dict[KeyT, list[object]] = {}
        self._counter: Final = itertools.count()  # unique sequence count

    def __setitem__(self, key: KeyT, priority: PriorityT) -> None:
        """Add a new task or update the priority of an existing task"""
        if key in self._entry_finder:
            self.remove(key)
        self._size += 1
        entry = [priority, key]
        self._entry_finder[key] = entry
        heapq.heappush(self._pq, entry)

    def remove(self, key: KeyT) -> None:
        """Mark an existing task as REMOVED.  Raise KeyError if not found."""
        entry = self._entry_finder.pop(key)
        entry[-1] = PriorityQueue._REMOVED
        self._size -= 1

    def pop(self) -> tuple[KeyT, PriorityT]:
        """Remove and return the lowest priority task. Raise KeyError if empty."""
        while self._pq:
            priority, task = heapq.heappop(self._pq)
            if task is not PriorityQueue._REMOVED:
                del self._entry_finder[cast("KeyT", task)]
                self._size -= 1
                return cast("tuple[KeyT, PriorityT]", (task, priority))
        raise KeyError("pop from an empty priority queue")

    def __len__(self) -> int:
        return self._size


def test_main() -> None:
    p: PriorityQueue[str, int] = PriorityQueue()
    p["x"] = 15
    p["y"] = 23
    p["z"] = 8
    assert p.pop() == ("z", 8)
    assert p.pop() == ("x", 15)


# Don't write tests below during competition.


def main() -> None:
    test_main()


if __name__ == "__main__":
    main()
