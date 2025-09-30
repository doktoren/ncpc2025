"""
Topological sorting for Directed Acyclic Graphs (DAGs).

Produces a linear ordering of vertices such that for every directed edge (u, v),
vertex u comes before v in the ordering. Uses both DFS-based and Kahn's algorithm
(BFS-based) approaches for different use cases.

Time complexity: O(V + E) for both algorithms, where V is vertices and E is edges.
Space complexity: O(V + E) for the graph representation and auxiliary data structures.
"""

from __future__ import annotations

from collections import deque

# Don't use annotations during contest
from typing import Generic, TypeVar

NodeT = TypeVar("NodeT")


class TopologicalSort(Generic[NodeT]):
    def __init__(self) -> None:
        self.graph: dict[NodeT, list[NodeT]] = {}
        self.in_degree: dict[NodeT, int] = {}

    def add_edge(self, u: NodeT, v: NodeT) -> None:
        """Add directed edge from u to v."""
        if u not in self.graph:
            self.graph[u] = []
            self.in_degree[u] = 0
        if v not in self.in_degree:
            self.in_degree[v] = 0
            self.graph[v] = []

        self.graph[u].append(v)
        self.in_degree[v] += 1

    def kahn_sort(self) -> list[NodeT] | None:
        """
        Topological sort using Kahn's algorithm (BFS-based).

        Returns the topological ordering, or None if the graph has a cycle.
        """
        in_deg = self.in_degree.copy()
        queue = deque([node for node, deg in in_deg.items() if deg == 0])
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in self.graph[node]:
                in_deg[neighbor] -= 1
                if in_deg[neighbor] == 0:
                    queue.append(neighbor)

        # Check if all nodes are processed (no cycle)
        if len(result) != len(self.in_degree):
            return None

        return result

    def dfs_sort(self) -> list[NodeT] | None:
        """
        Topological sort using DFS.

        Returns the topological ordering, or None if the graph has a cycle.
        """
        WHITE, GRAY, BLACK = 0, 1, 2
        color = dict.fromkeys(self.in_degree, WHITE)
        result = []

        def dfs(node: NodeT) -> bool:
            if color[node] == GRAY:  # Back edge (cycle)
                return False
            if color[node] == BLACK:  # Already processed
                return True

            color[node] = GRAY
            for neighbor in self.graph[node]:
                if not dfs(neighbor):
                    return False

            color[node] = BLACK
            result.append(node)
            return True

        for node in self.in_degree:
            if color[node] == WHITE and not dfs(node):
                return None

        return result[::-1]

    def has_cycle(self) -> bool:
        """Check if the graph contains a cycle."""
        return self.kahn_sort() is None

    def longest_path(self) -> dict[NodeT, int]:
        """
        Find longest path from each node in the DAG.

        Returns a dictionary mapping each node to its longest path length.
        """
        topo_order = self.kahn_sort()
        if topo_order is None:
            msg = "Graph contains a cycle"
            raise ValueError(msg)

        dist = dict.fromkeys(self.in_degree, 0)

        for node in topo_order:
            for neighbor in self.graph[node]:
                dist[neighbor] = max(dist[neighbor], dist[node] + 1)

        return dist


def test_main() -> None:
    ts: TopologicalSort[int] = TopologicalSort()
    edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    for u, v in edges:
        ts.add_edge(u, v)

    kahn_result = ts.kahn_sort()
    dfs_result = ts.dfs_sort()

    assert kahn_result is not None
    assert dfs_result is not None
    assert not ts.has_cycle()

    # Test with cycle
    ts_cycle: TopologicalSort[int] = TopologicalSort()
    ts_cycle.add_edge(1, 2)
    ts_cycle.add_edge(2, 3)
    ts_cycle.add_edge(3, 1)
    assert ts_cycle.has_cycle()


# Don't write tests below during competition.


def test_empty_graph() -> None:
    ts: TopologicalSort[int] = TopologicalSort()

    # Empty graph should return empty list
    assert ts.kahn_sort() == []
    assert ts.dfs_sort() == []
    assert not ts.has_cycle()


def test_single_node() -> None:
    ts: TopologicalSort[str] = TopologicalSort()
    ts.add_edge("A", "A")  # This creates a self-loop (cycle)

    assert ts.has_cycle()
    assert ts.kahn_sort() is None
    assert ts.dfs_sort() is None

    # Single node without self-loop
    ts2: TopologicalSort[str] = TopologicalSort()
    ts2.in_degree["A"] = 0
    ts2.graph["A"] = []

    result = ts2.kahn_sort()
    assert result == ["A"]
    assert not ts2.has_cycle()


def test_simple_chain() -> None:
    # Linear chain: A -> B -> C -> D
    ts: TopologicalSort[str] = TopologicalSort()
    edges = [("A", "B"), ("B", "C"), ("C", "D")]
    for u, v in edges:
        ts.add_edge(u, v)

    kahn_result = ts.kahn_sort()
    dfs_result = ts.dfs_sort()

    assert kahn_result == ["A", "B", "C", "D"]
    assert dfs_result == ["A", "B", "C", "D"]
    assert not ts.has_cycle()


def test_simple_cycle() -> None:
    # Simple 3-cycle: A -> B -> C -> A
    ts: TopologicalSort[str] = TopologicalSort()
    edges = [("A", "B"), ("B", "C"), ("C", "A")]
    for u, v in edges:
        ts.add_edge(u, v)

    assert ts.has_cycle()
    assert ts.kahn_sort() is None
    assert ts.dfs_sort() is None


def test_disconnected_components() -> None:
    # Two disconnected chains: A->B and C->D
    ts: TopologicalSort[str] = TopologicalSort()
    edges = [("A", "B"), ("C", "D")]
    for u, v in edges:
        ts.add_edge(u, v)

    kahn_result = ts.kahn_sort()
    dfs_result = ts.dfs_sort()

    # Both should work, order might vary for disconnected components
    assert kahn_result is not None
    assert dfs_result is not None
    assert len(kahn_result) == 4
    assert len(dfs_result) == 4
    assert not ts.has_cycle()

    # Check that ordering constraints are satisfied
    assert kahn_result.index("A") < kahn_result.index("B")
    assert kahn_result.index("C") < kahn_result.index("D")


def test_diamond_dag() -> None:
    # Diamond: A -> B,C  B,C -> D
    ts: TopologicalSort[str] = TopologicalSort()
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")]
    for u, v in edges:
        ts.add_edge(u, v)

    kahn_result = ts.kahn_sort()
    dfs_result = ts.dfs_sort()

    assert kahn_result is not None
    assert dfs_result is not None
    assert not ts.has_cycle()

    # Check ordering constraints
    for result in [kahn_result, dfs_result]:
        assert result.index("A") < result.index("B")
        assert result.index("A") < result.index("C")
        assert result.index("B") < result.index("D")
        assert result.index("C") < result.index("D")


def test_complex_dag() -> None:
    # More complex DAG with multiple valid orderings
    ts: TopologicalSort[int] = TopologicalSort()
    edges = [(1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 6), (5, 6)]
    for u, v in edges:
        ts.add_edge(u, v)

    kahn_result = ts.kahn_sort()
    dfs_result = ts.dfs_sort()

    assert kahn_result is not None
    assert dfs_result is not None
    assert not ts.has_cycle()

    # Verify all ordering constraints
    constraints = [(1, 2), (1, 3), (2, 4), (3, 4), (3, 5), (4, 6), (5, 6)]
    for result in [kahn_result, dfs_result]:
        for u, v in constraints:
            assert result.index(u) < result.index(v)


def test_large_cycle() -> None:
    # Large cycle: 0 -> 1 -> 2 -> ... -> 99 -> 0
    ts: TopologicalSort[int] = TopologicalSort()
    n = 100
    for i in range(n):
        ts.add_edge(i, (i + 1) % n)

    assert ts.has_cycle()
    assert ts.kahn_sort() is None
    assert ts.dfs_sort() is None


def test_tree_structure() -> None:
    # Binary tree structure (DAG)
    ts: TopologicalSort[int] = TopologicalSort()
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)]
    for u, v in edges:
        ts.add_edge(u, v)

    kahn_result = ts.kahn_sort()
    dfs_result = ts.dfs_sort()

    assert kahn_result is not None
    assert dfs_result is not None
    assert not ts.has_cycle()

    # Check tree constraints
    for result in [kahn_result, dfs_result]:
        assert result.index(1) < result.index(2)
        assert result.index(1) < result.index(3)
        assert result.index(2) < result.index(4)
        assert result.index(2) < result.index(5)
        assert result.index(3) < result.index(6)
        assert result.index(3) < result.index(7)


def test_longest_path() -> None:
    # Test longest path functionality
    ts: TopologicalSort[str] = TopologicalSort()
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E")]
    for u, v in edges:
        ts.add_edge(u, v)

    longest_paths = ts.longest_path()

    # Expected longest paths from each node
    assert longest_paths["A"] == 0
    assert longest_paths["B"] == 1
    assert longest_paths["C"] == 1
    assert longest_paths["D"] == 2
    assert longest_paths["E"] == 3


def test_longest_path_with_cycle() -> None:
    # Should raise error for graphs with cycles
    ts: TopologicalSort[int] = TopologicalSort()
    edges = [(1, 2), (2, 3), (3, 1)]  # Cycle
    for u, v in edges:
        ts.add_edge(u, v)

    try:
        ts.longest_path()
        assert False, "Should raise ValueError for cyclic graph"
    except ValueError:
        pass


def test_multiple_sources() -> None:
    # Graph with multiple sources (nodes with in-degree 0)
    ts: TopologicalSort[int] = TopologicalSort()
    edges = [(1, 3), (2, 3), (3, 4), (5, 6)]
    for u, v in edges:
        ts.add_edge(u, v)

    kahn_result = ts.kahn_sort()
    dfs_result = ts.dfs_sort()

    assert kahn_result is not None
    assert dfs_result is not None
    assert not ts.has_cycle()

    # Sources (1, 2, 5) should come before their dependents
    for result in [kahn_result, dfs_result]:
        assert result.index(1) < result.index(3)
        assert result.index(2) < result.index(3)
        assert result.index(3) < result.index(4)
        assert result.index(5) < result.index(6)


def test_course_prerequisites() -> None:
    # Real-world example: course prerequisites
    ts: TopologicalSort[str] = TopologicalSort()
    # Math1 -> Math2 -> Math3, Physics1 -> Physics2, Math2 -> Physics2
    edges = [
        ("Math1", "Math2"), ("Math2", "Math3"),
        ("Physics1", "Physics2"), ("Math2", "Physics2")
    ]
    for u, v in edges:
        ts.add_edge(u, v)

    kahn_result = ts.kahn_sort()
    assert kahn_result is not None
    assert not ts.has_cycle()

    # Verify prerequisites
    assert kahn_result.index("Math1") < kahn_result.index("Math2")
    assert kahn_result.index("Math2") < kahn_result.index("Math3")
    assert kahn_result.index("Physics1") < kahn_result.index("Physics2")
    assert kahn_result.index("Math2") < kahn_result.index("Physics2")


def test_complex_dependencies() -> None:
    # Complex dependency graph
    ts: TopologicalSort[str] = TopologicalSort()
    edges = [
        ("underwear", "pants"), ("underwear", "shoes"),
        ("pants", "belt"), ("pants", "shoes"),
        ("shirt", "belt"), ("shirt", "tie"),
        ("tie", "jacket"), ("belt", "jacket"),
        ("socks", "shoes")
    ]
    for u, v in edges:
        ts.add_edge(u, v)

    kahn_result = ts.kahn_sort()
    dfs_result = ts.dfs_sort()

    assert kahn_result is not None
    assert dfs_result is not None
    assert not ts.has_cycle()

    # Check some key dependencies
    for result in [kahn_result, dfs_result]:
        assert result.index("underwear") < result.index("pants")
        assert result.index("pants") < result.index("shoes")
        assert result.index("socks") < result.index("shoes")
        assert result.index("shirt") < result.index("tie")
        assert result.index("tie") < result.index("jacket")


def test_stress_large_dag() -> None:
    # Large DAG: layered graph
    ts: TopologicalSort[int] = TopologicalSort()
    layers = 10
    nodes_per_layer = 10

    # Connect each node in layer i to all nodes in layer i+1
    for layer in range(layers - 1):
        for i in range(nodes_per_layer):
            for j in range(nodes_per_layer):
                u = layer * nodes_per_layer + i
                v = (layer + 1) * nodes_per_layer + j
                ts.add_edge(u, v)

    kahn_result = ts.kahn_sort()
    dfs_result = ts.dfs_sort()

    assert kahn_result is not None
    assert dfs_result is not None
    assert not ts.has_cycle()
    assert len(kahn_result) == layers * nodes_per_layer


def main() -> None:
    test_main()
    test_empty_graph()
    test_single_node()
    test_simple_chain()
    test_simple_cycle()
    test_disconnected_components()
    test_diamond_dag()
    test_complex_dag()
    test_large_cycle()
    test_tree_structure()
    test_longest_path()
    test_longest_path_with_cycle()
    test_multiple_sources()
    test_course_prerequisites()
    test_complex_dependencies()
    test_stress_large_dag()


if __name__ == "__main__":
    main()
