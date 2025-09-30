"""
Lowest Common Ancestor (LCA) using binary lifting preprocessing.

Finds the lowest common ancestor of two nodes in a tree efficiently after O(n log n)
preprocessing. Binary lifting allows answering LCA queries in O(log n) time by
maintaining ancestors at powers-of-2 distances.

Time complexity: O(n log n) preprocessing, O(log n) per LCA query.
Space complexity: O(n log n) for the binary lifting table.
"""

from __future__ import annotations

# Don't use annotations during contest
from typing import Final, Generic, TypeVar

NodeT = TypeVar("NodeT")


class LCA(Generic[NodeT]):
    def __init__(self, root: NodeT) -> None:
        self.root: Final = root
        self.graph: dict[NodeT, list[NodeT]] = {}
        self.depth: dict[NodeT, int] = {}
        self.parent: dict[NodeT, list[NodeT | None]] = {}
        self.max_log = 0

    def add_edge(self, u: NodeT, v: NodeT) -> None:
        """Add undirected edge between u and v."""
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)

    def preprocess(self) -> None:
        """Build the binary lifting table. Call after adding all edges."""
        # Find max depth to determine log table size
        self._dfs_depth(self.root, None, 0)

        nodes = list(self.depth.keys())
        n = len(nodes)
        self.max_log = n.bit_length()

        # Initialize parent table
        for node in nodes:
            self.parent[node] = [None] * self.max_log

        # Fill first column (direct parents) and compute binary lifting
        self._dfs_parents(self.root, None)

        # Fill binary lifting table
        for j in range(1, self.max_log):
            for node in nodes:
                parent_j_minus_1 = self.parent[node][j - 1]
                if parent_j_minus_1 is not None:
                    self.parent[node][j] = self.parent[parent_j_minus_1][j - 1]

    def _dfs_depth(self, node: NodeT, par: NodeT | None, d: int) -> None:
        """Compute depths of all nodes."""
        self.depth[node] = d
        for neighbor in self.graph.get(node, []):
            if neighbor != par:
                self._dfs_depth(neighbor, node, d + 1)

    def _dfs_parents(self, node: NodeT, par: NodeT | None) -> None:
        """Set direct parents for all nodes."""
        self.parent[node][0] = par
        for neighbor in self.graph.get(node, []):
            if neighbor != par:
                self._dfs_parents(neighbor, node)

    def lca(self, u: NodeT, v: NodeT) -> NodeT:
        """Find lowest common ancestor of u and v."""
        if self.depth[u] < self.depth[v]:
            u, v = v, u

        # Bring u to same level as v
        diff = self.depth[u] - self.depth[v]
        for i in range(self.max_log):
            if (diff >> i) & 1:
                u_parent = self.parent[u][i]
                if u_parent is not None:
                    u = u_parent

        if u == v:
            return u

        # Binary search for LCA
        for i in range(self.max_log - 1, -1, -1):
            if self.parent[u][i] != self.parent[v][i]:
                u_parent = self.parent[u][i]
                v_parent = self.parent[v][i]
                if u_parent is not None and v_parent is not None:
                    u = u_parent
                    v = v_parent

        result = self.parent[u][0]
        if result is None:
            msg = "LCA computation failed - invalid tree structure"
            raise ValueError(msg)
        return result

    def distance(self, u: NodeT, v: NodeT) -> int:
        """Calculate distance between two nodes."""
        lca_node = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[lca_node]


def test_main() -> None:
    lca = LCA(1)
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]
    for u, v in edges:
        lca.add_edge(u, v)

    lca.preprocess()

    assert lca.lca(4, 5) == 2
    assert lca.lca(4, 6) == 1
    assert lca.distance(4, 6) == 4


# Don't write tests below during competition.


def test_linear_chain() -> None:
    # Test on a simple linear chain: 1-2-3-4-5
    lca = LCA(1)
    edges = [(1, 2), (2, 3), (3, 4), (4, 5)]
    for u, v in edges:
        lca.add_edge(u, v)

    lca.preprocess()

    # LCA of nodes at different depths
    assert lca.lca(1, 5) == 1
    assert lca.lca(2, 5) == 2
    assert lca.lca(3, 5) == 3
    assert lca.lca(4, 5) == 4
    assert lca.lca(5, 5) == 5

    # Distance tests
    assert lca.distance(1, 5) == 4
    assert lca.distance(2, 4) == 2
    assert lca.distance(3, 3) == 0


def test_single_node() -> None:
    lca = LCA("root")
    lca.preprocess()

    assert lca.lca("root", "root") == "root"
    assert lca.distance("root", "root") == 0


def test_star_graph() -> None:
    # Star graph: center connected to many leaves
    lca = LCA(0)
    for i in range(1, 6):
        lca.add_edge(0, i)

    lca.preprocess()

    # All leaf pairs should have LCA = center
    for i in range(1, 6):
        for j in range(i + 1, 6):
            assert lca.lca(i, j) == 0
            assert lca.distance(i, j) == 2  # Through center

    # Center to leaf
    for i in range(1, 6):
        assert lca.lca(0, i) == 0
        assert lca.distance(0, i) == 1


def test_deep_tree() -> None:
    # Deep binary tree
    lca = LCA(1)
    # Build tree: 1 -> 2,3  2 -> 4,5  3 -> 6,7  4 -> 8,9
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9)]
    for u, v in edges:
        lca.add_edge(u, v)

    lca.preprocess()

    # Test various LCA queries
    assert lca.lca(8, 9) == 4
    assert lca.lca(4, 5) == 2
    assert lca.lca(2, 3) == 1
    assert lca.lca(8, 5) == 2
    assert lca.lca(8, 6) == 1
    assert lca.lca(6, 7) == 3

    # Distance tests
    assert lca.distance(8, 9) == 2
    assert lca.distance(8, 5) == 3
    assert lca.distance(6, 7) == 2
    assert lca.distance(8, 6) == 5


def test_unbalanced_tree() -> None:
    # Highly unbalanced tree (essentially a path with some branches)
    lca = LCA("A")
    edges = [
        ("A", "B"), ("B", "C"), ("C", "D"), ("D", "E"),
        ("B", "X"), ("C", "Y"), ("D", "Z")
    ]
    for u, v in edges:
        lca.add_edge(u, v)

    lca.preprocess()

    assert lca.lca("E", "Z") == "D"
    assert lca.lca("X", "Y") == "B"
    assert lca.lca("X", "E") == "B"
    assert lca.lca("Y", "Z") == "C"

    # Distance in unbalanced tree
    assert lca.distance("X", "E") == 4  # X->B->C->D->E
    assert lca.distance("Y", "Z") == 3  # Y->C->D->Z


def test_large_balanced_tree() -> None:
    # Complete binary tree with 15 nodes (4 levels)
    lca = LCA(1)
    edges = []
    for i in range(1, 8):  # Internal nodes
        left_child = 2 * i
        right_child = 2 * i + 1
        if left_child <= 15:
            edges.append((i, left_child))
        if right_child <= 15:
            edges.append((i, right_child))

    for u, v in edges:
        lca.add_edge(u, v)

    lca.preprocess()

    # Test leaf nodes
    assert lca.lca(8, 9) == 4
    assert lca.lca(10, 11) == 5
    assert lca.lca(8, 10) == 2
    assert lca.lca(12, 13) == 6
    assert lca.lca(8, 15) == 1

    # Distance between leaves
    assert lca.distance(8, 9) == 2
    assert lca.distance(8, 15) == 6


def test_string_nodes() -> None:
    # Test with string node labels
    lca = LCA("root")
    edges = [
        ("root", "left"), ("root", "right"),
        ("left", "left_left"), ("left", "left_right"),
        ("right", "right_left"), ("right", "right_right")
    ]
    for u, v in edges:
        lca.add_edge(u, v)

    lca.preprocess()

    assert lca.lca("left_left", "left_right") == "left"
    assert lca.lca("left_left", "right_left") == "root"
    assert lca.distance("left_left", "right_right") == 4


def test_complex_tree() -> None:
    # More complex tree structure
    lca = LCA(0)
    edges = [
        (0, 1), (0, 2), (0, 3),
        (1, 4), (1, 5),
        (2, 6), (2, 7), (2, 8),
        (3, 9),
        (4, 10), (4, 11),
        (6, 12), (6, 13),
        (9, 14), (9, 15)
    ]
    for u, v in edges:
        lca.add_edge(u, v)

    lca.preprocess()

    # Test various combinations
    assert lca.lca(10, 11) == 4
    assert lca.lca(4, 5) == 1
    assert lca.lca(10, 5) == 1
    assert lca.lca(12, 8) == 2
    assert lca.lca(14, 15) == 9
    assert lca.lca(10, 14) == 0

    # Complex distance calculations
    assert lca.distance(10, 11) == 2  # 10->4->11
    assert lca.distance(10, 14) == 6  # 10->4->1->0->3->9->14
    assert lca.distance(12, 8) == 3   # 12->6->2->8


def test_edge_cases() -> None:
    # Test edge cases and boundary conditions

    # Tree with only two nodes
    lca = LCA("A")
    lca.add_edge("A", "B")
    lca.preprocess()

    assert lca.lca("A", "B") == "A"
    assert lca.lca("B", "A") == "A"
    assert lca.distance("A", "B") == 1

    # Same node queries
    assert lca.lca("A", "A") == "A"
    assert lca.lca("B", "B") == "B"


def test_large_star() -> None:
    # Large star graph to test scalability
    lca = LCA(0)
    n = 100
    for i in range(1, n + 1):
        lca.add_edge(0, i)

    lca.preprocess()

    # All leaves should have distance 2 from each other
    assert lca.lca(1, 50) == 0
    assert lca.lca(25, 75) == 0
    assert lca.distance(1, 50) == 2
    assert lca.distance(25, 100) == 2


def test_long_path() -> None:
    # Very long path to test binary lifting efficiency
    lca = LCA(0)
    n = 64  # Power of 2 for clean binary lifting
    for i in range(n):
        lca.add_edge(i, i + 1)

    lca.preprocess()

    # Test LCA at various distances
    assert lca.lca(0, 64) == 0
    assert lca.lca(32, 64) == 32
    assert lca.lca(16, 48) == 16

    # Distance should be difference in path positions
    assert lca.distance(0, 64) == 64
    assert lca.distance(16, 48) == 32
    assert lca.distance(30, 35) == 5


def test_fibonacci_tree() -> None:
    # Tree based on Fibonacci structure
    lca = LCA(1)
    # Build: 1->2,3  2->4,5  3->6  4->7  5->8,9
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (5, 9)]
    for u, v in edges:
        lca.add_edge(u, v)

    lca.preprocess()

    assert lca.lca(7, 8) == 2
    assert lca.lca(7, 6) == 1
    assert lca.lca(8, 9) == 5
    assert lca.distance(7, 9) == 4  # 7->4->2->5->9


def main() -> None:
    test_main()
    test_linear_chain()
    test_single_node()
    test_star_graph()
    test_deep_tree()
    test_unbalanced_tree()
    test_large_balanced_tree()
    test_string_nodes()
    test_complex_tree()
    test_edge_cases()
    test_large_star()
    test_long_path()
    test_fibonacci_tree()


if __name__ == "__main__":
    main()
