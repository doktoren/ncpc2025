"""
Dijkstra's algorithm for single-source shortest path in weighted graphs.

Finds shortest paths from a source vertex to all other vertices in a graph with
non-negative edge weights. Uses a priority queue (heap) for efficient vertex selection.

Time complexity: O((V + E) log V) with binary heap, where V is vertices and E is edges.
Space complexity: O(V + E) for the graph representation and auxiliary data structures.
"""

from __future__ import annotations

import heapq

# Don't use annotations during contest
from typing import Final, Generic, Protocol, TypeVar

from typing_extensions import Self


class Comparable(Protocol):
    def __lt__(self, other: Self, /) -> bool: ...
    def __add__(self, other: Self, /) -> Self: ...


WeightT = TypeVar("WeightT", bound=Comparable)
NodeT = TypeVar("NodeT")


class Dijkstra(Generic[NodeT, WeightT]):
    def __init__(self, infinity: WeightT, zero: WeightT) -> None:
        self.infinity: Final[WeightT] = infinity
        self.zero: Final[WeightT] = zero
        self.graph: dict[NodeT, list[tuple[NodeT, WeightT]]] = {}

    def add_edge(self, u: NodeT, v: NodeT, weight: WeightT) -> None:
        """Add directed edge from u to v with given weight."""
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append((v, weight))

    def shortest_paths(
        self, source: NodeT
    ) -> tuple[dict[NodeT, WeightT], dict[NodeT, NodeT | None]]:
        """
        Find shortest paths from source to all reachable vertices.

        Returns (distances, predecessors) where:
        - distances[v] = shortest distance from source to v
        - predecessors[v] = previous vertex in shortest path to v (None for source)
        """
        distances: dict[NodeT, WeightT] = {source: self.zero}
        predecessors: dict[NodeT, NodeT | None] = {source: None}
        pq: list[tuple[WeightT, NodeT]] = [(self.zero, source)]
        visited: set[NodeT] = set()

        while pq:
            current_dist, u = heapq.heappop(pq)

            if u in visited:
                continue
            visited.add(u)

            if u not in self.graph:
                continue

            for v, weight in self.graph[u]:
                new_dist = current_dist + weight

                if v not in distances or new_dist < distances[v]:
                    distances[v] = new_dist
                    predecessors[v] = u
                    heapq.heappush(pq, (new_dist, v))

        return distances, predecessors

    def shortest_path(self, source: NodeT, target: NodeT) -> list[NodeT] | None:
        """Get the shortest path from source to target, or None if unreachable."""
        _, predecessors = self.shortest_paths(source)

        if target not in predecessors:
            return None

        path = []
        current: NodeT | None = target
        while current is not None:
            path.append(current)
            current = predecessors.get(current)

        return path[::-1]


def test_main() -> None:
    d: Dijkstra[str, float] = Dijkstra(float("inf"), 0.0)
    d.add_edge("A", "B", 4.0)
    d.add_edge("A", "C", 2.0)
    d.add_edge("B", "C", 1.0)
    d.add_edge("B", "D", 5.0)
    d.add_edge("C", "D", 8.0)

    distances, _ = d.shortest_paths("A")
    assert distances["D"] == 9.0

    path = d.shortest_path("A", "D")
    assert path == ["A", "B", "D"]


# Don't write tests below during competition.


def test_single_node() -> None:
    d: Dijkstra[str, float] = Dijkstra(float("inf"), 0.0)

    distances, predecessors = d.shortest_paths("A")
    assert distances == {"A": 0.0}
    assert predecessors == {"A": None}

    path = d.shortest_path("A", "A")
    assert path == ["A"]


def test_unreachable_nodes() -> None:
    d: Dijkstra[int, int] = Dijkstra(999999, 0)
    d.add_edge(1, 2, 5)
    d.add_edge(3, 4, 3)

    distances, _ = d.shortest_paths(1)
    assert distances[2] == 5
    assert 3 not in distances
    assert 4 not in distances

    path = d.shortest_path(1, 4)
    assert path is None


def test_negative_zero_weights() -> None:
    d: Dijkstra[str, float] = Dijkstra(float("inf"), 0.0)
    d.add_edge("A", "B", 0.0)
    d.add_edge("B", "C", 0.0)
    d.add_edge("A", "C", 5.0)

    distances, _ = d.shortest_paths("A")
    assert distances["C"] == 0.0  # Should take A->B->C path


def test_dense_graph() -> None:
    # Complete graph with 5 nodes
    d: Dijkstra[int, int] = Dijkstra(999999, 0)

    # Add edges between all pairs
    weights = {
        (0, 1): 4, (0, 2): 2, (0, 3): 7, (0, 4): 1,
        (1, 0): 4, (1, 2): 3, (1, 3): 2, (1, 4): 5,
        (2, 0): 2, (2, 1): 3, (2, 3): 4, (2, 4): 8,
        (3, 0): 7, (3, 1): 2, (3, 2): 4, (3, 4): 6,
        (4, 0): 1, (4, 1): 5, (4, 2): 8, (4, 3): 6,
    }

    for (u, v), weight in weights.items():
        d.add_edge(u, v, weight)

    distances, _ = d.shortest_paths(0)

    # Verify shortest distances from node 0
    assert distances[1] == 4
    assert distances[2] == 2
    assert distances[3] == 6  # 0->1->3 = 4+2 = 6
    assert distances[4] == 1


def test_large_graph() -> None:
    # Linear chain: 0->1->2->...->99
    d: Dijkstra[int, int] = Dijkstra(999999, 0)

    for i in range(99):
        d.add_edge(i, i + 1, 1)

    distances, _ = d.shortest_paths(0)

    # Distance to node i should be i
    for i in range(100):
        assert distances[i] == i

    # Test path reconstruction
    path = d.shortest_path(0, 50)
    assert path == list(range(51))


def test_multiple_equal_paths() -> None:
    # Diamond-shaped graph with equal path lengths
    d: Dijkstra[str, int] = Dijkstra(999999, 0)
    d.add_edge("S", "A", 2)
    d.add_edge("S", "B", 2)
    d.add_edge("A", "T", 3)
    d.add_edge("B", "T", 3)

    distances, _ = d.shortest_paths("S")
    assert distances["T"] == 5  # Both paths S->A->T and S->B->T have length 5

    path = d.shortest_path("S", "T")
    assert path is not None
    assert len(path) == 3
    assert path[0] == "S"
    assert path[-1] == "T"


def test_self_loops() -> None:
    d: Dijkstra[int, int] = Dijkstra(999999, 0)
    d.add_edge(1, 1, 5)  # Self-loop
    d.add_edge(1, 2, 3)

    distances, _ = d.shortest_paths(1)
    assert distances[1] == 0  # Distance to self is always 0
    assert distances[2] == 3


def test_decimal_weights() -> None:
    from decimal import Decimal

    d: Dijkstra[str, Decimal] = Dijkstra(Decimal(999999), Decimal(0))
    d.add_edge("A", "B", Decimal("1.5"))
    d.add_edge("B", "C", Decimal("2.7"))
    d.add_edge("A", "C", Decimal("5.0"))

    distances, _ = d.shortest_paths("A")
    assert distances["C"] == Decimal("4.2")  # 1.5 + 2.7


def test_stress_many_nodes() -> None:
    # Star graph: center connected to many nodes
    d: Dijkstra[int, int] = Dijkstra(999999, 0)

    center = 0
    for i in range(1, 501):  # 500 nodes connected to center
        d.add_edge(center, i, i)

    distances, _ = d.shortest_paths(center)

    # Distance to node i should be i
    for i in range(1, 501):
        assert distances[i] == i

    # Path from center to any node should be direct
    path = d.shortest_path(center, 100)
    assert path == [0, 100]


def main() -> None:
    test_main()
    test_single_node()
    test_unreachable_nodes()
    test_negative_zero_weights()
    test_dense_graph()
    test_large_graph()
    test_multiple_equal_paths()
    test_self_loops()
    test_decimal_weights()
    test_stress_many_nodes()


if __name__ == "__main__":
    main()
