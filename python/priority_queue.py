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
        """Add new task or update priority. Lower priority = popped first."""
        if key in self._entry_finder:
            self.remove(key)
        self._size += 1
        entry = [priority, key]
        self._entry_finder[key] = entry
        heapq.heappush(self._pq, entry)

    def remove(self, key: KeyT) -> None:
        """Remove task by key. Raises KeyError if not found."""
        entry = self._entry_finder.pop(key)
        entry[-1] = PriorityQueue._REMOVED
        self._size -= 1

    def pop(self) -> tuple[KeyT, PriorityT]:
        """Remove and return (key, priority) with lowest priority. Raises KeyError if empty."""
        while self._pq:
            priority, task = heapq.heappop(self._pq)
            if task is not PriorityQueue._REMOVED:
                del self._entry_finder[cast("KeyT", task)]
                self._size -= 1
                return cast("tuple[KeyT, PriorityT]", (task, priority))
        raise KeyError("pop from an empty priority queue")

    def peek(self) -> tuple[KeyT, PriorityT] | None:
        """Return (key, priority) with lowest priority without removing. Returns None if empty."""
        while self._pq:
            priority, task = self._pq[0]
            if task is not PriorityQueue._REMOVED:
                return cast("tuple[KeyT, PriorityT]", (task, priority))
            # Remove the REMOVED sentinel from the top
            heapq.heappop(self._pq)
        return None

    def __contains__(self, key: KeyT) -> bool:
        """Check if key exists in queue."""
        return key in self._entry_finder

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


def test_basic_operations() -> None:
    """Test basic add, pop, and len operations."""
    pq: PriorityQueue[str, int] = PriorityQueue()

    # Test empty queue
    assert len(pq) == 0
    assert pq.peek() is None

    # Add items
    pq["task1"] = 10
    pq["task2"] = 5
    pq["task3"] = 15

    assert len(pq) == 3
    assert pq.peek() == ("task2", 5)

    # Pop in priority order
    assert pq.pop() == ("task2", 5)
    assert len(pq) == 2
    assert pq.pop() == ("task1", 10)
    assert pq.pop() == ("task3", 15)

    assert len(pq) == 0


def test_update_priority() -> None:
    """Test updating the priority of existing tasks."""
    pq: PriorityQueue[str, int] = PriorityQueue()

    pq["task1"] = 10
    pq["task2"] = 5

    # Update task1 to have higher priority
    pq["task1"] = 3
    assert pq.peek() == ("task1", 3)
    assert len(pq) == 2

    # Pop should now give task1 first
    assert pq.pop() == ("task1", 3)
    assert pq.pop() == ("task2", 5)


def test_remove() -> None:
    """Test removing tasks from the queue."""
    pq: PriorityQueue[str, int] = PriorityQueue()

    pq["task1"] = 10
    pq["task2"] = 5
    pq["task3"] = 15

    # Remove middle priority task
    pq.remove("task1")
    assert len(pq) == 2
    assert "task1" not in pq

    # Verify correct items remain
    assert pq.pop() == ("task2", 5)
    assert pq.pop() == ("task3", 15)


def test_contains() -> None:
    """Test membership checking."""
    pq: PriorityQueue[str, int] = PriorityQueue()

    pq["task1"] = 10
    pq["task2"] = 5

    assert "task1" in pq
    assert "task2" in pq
    assert "task3" not in pq

    pq.remove("task1")
    assert "task1" not in pq


def test_empty_operations() -> None:
    """Test operations on empty queue."""
    pq: PriorityQueue[str, int] = PriorityQueue()

    # Test peek on empty queue
    assert pq.peek() is None

    # Test pop on empty queue
    try:
        pq.pop()
        assert False, "Should raise KeyError"
    except KeyError:
        pass


def test_remove_nonexistent() -> None:
    """Test removing a key that doesn't exist."""
    pq: PriorityQueue[str, int] = PriorityQueue()

    pq["task1"] = 10

    try:
        pq.remove("nonexistent")
        assert False, "Should raise KeyError"
    except KeyError:
        pass


def test_single_element() -> None:
    """Test queue with single element."""
    pq: PriorityQueue[str, int] = PriorityQueue()

    pq["only"] = 42
    assert len(pq) == 1
    assert pq.peek() == ("only", 42)
    assert pq.pop() == ("only", 42)
    assert len(pq) == 0


def test_duplicate_priorities() -> None:
    """Test tasks with the same priority."""
    pq: PriorityQueue[str, int] = PriorityQueue()

    pq["task1"] = 10
    pq["task2"] = 10
    pq["task3"] = 10

    assert len(pq) == 3

    # All should pop eventually
    results = [pq.pop(), pq.pop(), pq.pop()]
    assert len(results) == 3
    assert all(priority == 10 for _, priority in results)


def test_with_floats() -> None:
    """Test priority queue with floating point priorities."""
    pq: PriorityQueue[str, float] = PriorityQueue()

    pq["a"] = 1.5
    pq["b"] = 0.5
    pq["c"] = 2.3

    assert pq.pop() == ("b", 0.5)
    assert pq.pop() == ("a", 1.5)
    assert pq.pop() == ("c", 2.3)


def main() -> None:
    test_basic_operations()
    test_update_priority()
    test_remove()
    test_contains()
    test_empty_operations()
    test_remove_nonexistent()
    test_single_element()
    test_duplicate_priorities()
    test_with_floats()
    test_main()
    print("All priority queue tests passed!")


if __name__ == "__main__":
    main()
