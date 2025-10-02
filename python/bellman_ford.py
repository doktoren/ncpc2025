"""
Bellman-Ford algorithm for single-source shortest paths with negative edge weights.

Finds shortest paths from a source vertex to all other vertices, even with negative
edge weights. Can detect negative cycles reachable from the source. Uses edge relaxation
V-1 times, then checks for negative cycles.

Time complexity: O(VE) where V is vertices and E is edges.
Space complexity: O(V + E) for graph representation and distance array.
"""

from __future__ import annotations

# Don't use annotations during contest
from typing import Final, Generic, Protocol, TypeVar

from typing_extensions import Self


class Comparable(Protocol):
    def __lt__(self, other: Self, /) -> bool: ...
    def __add__(self, other: Self, /) -> Self: ...


WeightT = TypeVar("WeightT", bound=Comparable)
NodeT = TypeVar("NodeT")


class BellmanFord(Generic[NodeT, WeightT]):
    def __init__(self, infinity: WeightT, zero: WeightT) -> None:
        self.infinity: Final[WeightT] = infinity
        self.zero: Final[WeightT] = zero
        self.edges: list[tuple[NodeT, NodeT, WeightT]] = []
        self.nodes: set[NodeT] = set()

    def add_edge(self, u: NodeT, v: NodeT, weight: WeightT) -> None:
        """Add directed edge from u to v with given weight."""
        self.edges.append((u, v, weight))
        self.nodes.add(u)
        self.nodes.add(v)

    def shortest_paths(
        self, source: NodeT
    ) -> tuple[dict[NodeT, WeightT], dict[NodeT, NodeT | None]] | None:
        """
        Find shortest paths from source to all reachable vertices.

        Returns (distances, predecessors) if no negative cycle reachable from source,
        None if negative cycle detected.
        - distances[v] = shortest distance from source to v
        - predecessors[v] = previous vertex in shortest path to v (None for source)
        """
        distances: dict[NodeT, WeightT] = {}
        predecessors: dict[NodeT, NodeT | None] = {}

        # Initialize distances
        for node in self.nodes:
            distances[node] = self.infinity
        distances[source] = self.zero
        predecessors[source] = None

        # Relax edges V-1 times
        for _ in range(len(self.nodes) - 1):
            for u, v, weight in self.edges:
                if distances[u] != self.infinity and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u

        # Check for negative cycles
        for u, v, weight in self.edges:
            if distances[u] != self.infinity and distances[u] + weight < distances[v]:
                return None  # Negative cycle detected

        return distances, predecessors

    def shortest_path(self, source: NodeT, target: NodeT) -> list[NodeT] | None:
        """
        Get the shortest path from source to target.

        Returns path as list of nodes, or None if unreachable or negative cycle detected.
        """
        result = self.shortest_paths(source)
        if result is None:
            return None  # Negative cycle

        _, predecessors = result
        if target not in predecessors:
            return None  # Unreachable

        path = []
        current: NodeT | None = target
        while current is not None:
            path.append(current)
            current = predecessors.get(current)

        return path[::-1]


def test_main() -> None:
    bf: BellmanFord[str, float] = BellmanFord(float("inf"), 0.0)
    bf.add_edge("A", "B", 4.0)
    bf.add_edge("A", "C", 2.0)
    bf.add_edge("B", "C", -3.0)  # Negative edge makes A->B->C better than A->C
    bf.add_edge("C", "D", 2.0)
    bf.add_edge("D", "B", 1.0)

    result = bf.shortest_paths("A")
    assert result is not None
    distances, _ = result
    # A->B: 4, A->C: min(2, 4+(-3)) = 1, A->D: 1+2 = 3
    assert distances["C"] == 1.0
    assert distances["D"] == 3.0

    path = bf.shortest_path("A", "D")
    assert path is not None
    assert path[0] == "A"
    assert path[-1] == "D"


# Don't write tests below during competition.


def test_negative_cycle() -> None:
    bf: BellmanFord[int, int] = BellmanFord(999999, 0)
    bf.add_edge(0, 1, 1)
    bf.add_edge(1, 2, -3)
    bf.add_edge(2, 0, 1)  # Cycle: 0->1->2->0 with total weight 1 + (-3) + 1 = -1

    result = bf.shortest_paths(0)
    assert result is None  # Should detect negative cycle


def test_single_node() -> None:
    bf: BellmanFord[str, float] = BellmanFord(float("inf"), 0.0)
    bf.nodes.add("A")

    result = bf.shortest_paths("A")
    assert result is not None
    distances, predecessors = result
    assert distances["A"] == 0.0
    assert predecessors["A"] is None


def test_unreachable_nodes() -> None:
    bf: BellmanFord[int, int] = BellmanFord(999999, 0)
    bf.add_edge(1, 2, 5)
    bf.add_edge(3, 4, 3)

    result = bf.shortest_paths(1)
    assert result is not None
    distances, _ = result
    assert distances[2] == 5
    assert distances[3] == 999999  # Unreachable
    assert distances[4] == 999999  # Unreachable


def test_all_negative_edges() -> None:
    bf: BellmanFord[str, int] = BellmanFord(999999, 0)
    bf.add_edge("A", "B", -1)
    bf.add_edge("B", "C", -2)
    bf.add_edge("C", "D", -3)

    result = bf.shortest_paths("A")
    assert result is not None
    distances, _ = result
    assert distances["D"] == -6  # -1 + (-2) + (-3)


def test_path_reconstruction() -> None:
    bf: BellmanFord[int, int] = BellmanFord(999999, 0)
    bf.add_edge(0, 1, 5)
    bf.add_edge(1, 2, 3)
    bf.add_edge(0, 2, 10)

    path = bf.shortest_path(0, 2)
    assert path is not None
    assert path == [0, 1, 2]  # Should take 0->1->2 (cost 8) not 0->2 (cost 10)


def test_negative_edge_relaxation() -> None:
    # Test that negative edges properly relax distances
    bf: BellmanFord[int, int] = BellmanFord(999999, 0)
    bf.add_edge(0, 1, 10)
    bf.add_edge(0, 2, 5)
    bf.add_edge(2, 1, -8)  # This should make path 0->2->1 better than 0->1

    result = bf.shortest_paths(0)
    assert result is not None
    distances, _ = result
    assert distances[1] == -3  # 5 + (-8) = -3, better than direct path of 10


def test_disconnected_graph() -> None:
    bf: BellmanFord[int, int] = BellmanFord(999999, 0)
    bf.add_edge(0, 1, 1)
    bf.add_edge(2, 3, 1)

    result = bf.shortest_paths(0)
    assert result is not None
    distances, _ = result
    assert distances[1] == 1
    assert distances[2] == 999999
    assert distances[3] == 999999


def test_self_loop_negative() -> None:
    bf: BellmanFord[int, int] = BellmanFord(999999, 0)
    bf.add_edge(0, 0, -1)  # Negative self-loop

    result = bf.shortest_paths(0)
    assert result is None  # Should detect negative cycle


def test_complex_graph() -> None:
    bf: BellmanFord[str, int] = BellmanFord(999999, 0)
    bf.add_edge("S", "A", 10)
    bf.add_edge("S", "E", 8)
    bf.add_edge("A", "C", 2)
    bf.add_edge("C", "D", 5)  # Changed to avoid negative cycle
    bf.add_edge("D", "B", 3)
    bf.add_edge("E", "D", 1)

    result = bf.shortest_paths("S")
    assert result is not None
    distances, _ = result
    # S->E->D: 8 + 1 = 9
    # S->E->D->B: 9 + 3 = 12
    assert distances["D"] == 9
    assert distances["B"] == 12


def main() -> None:
    test_main()
    test_negative_cycle()
    test_single_node()
    test_unreachable_nodes()
    test_all_negative_edges()
    test_path_reconstruction()
    test_negative_edge_relaxation()
    test_disconnected_graph()
    test_self_loop_negative()
    test_complex_graph()


if __name__ == "__main__":
    main()
