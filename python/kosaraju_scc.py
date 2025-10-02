"""
Kosaraju's algorithm for finding strongly connected components (SCCs) in directed graphs.

A strongly connected component is a maximal set of vertices where every vertex is
reachable from every other vertex in the set. Uses two DFS passes: one on original
graph to compute finish times, another on transpose graph to extract SCCs.

Time complexity: O(V + E) where V is vertices and E is edges.
Space complexity: O(V + E) for graph representation and auxiliary structures.
"""

from __future__ import annotations

# Don't use annotations during contest
from typing import Generic, TypeVar

NodeT = TypeVar("NodeT")


class KosarajuSCC(Generic[NodeT]):
    def __init__(self) -> None:
        self.graph: dict[NodeT, list[NodeT]] = {}
        self.transpose: dict[NodeT, list[NodeT]] = {}

    def add_edge(self, u: NodeT, v: NodeT) -> None:
        """Add directed edge from u to v."""
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        if u not in self.transpose:
            self.transpose[u] = []
        if v not in self.transpose:
            self.transpose[v] = []

        self.graph[u].append(v)
        self.transpose[v].append(u)

    def find_sccs(self) -> list[list[NodeT]]:
        """
        Find all strongly connected components.

        Returns list of SCCs, where each SCC is a list of vertices.
        SCCs are returned in reverse topological order of the condensation graph.
        """
        # First DFS pass: compute finish order on original graph
        visited: set[NodeT] = set()
        finish_order: list[NodeT] = []

        def dfs1(node: NodeT) -> None:
            visited.add(node)
            if node in self.graph:
                for neighbor in self.graph[node]:
                    if neighbor not in visited:
                        dfs1(neighbor)
            finish_order.append(node)

        for node in self.graph:
            if node not in visited:
                dfs1(node)

        # Second DFS pass: find SCCs on transpose graph in reverse finish order
        visited.clear()
        sccs: list[list[NodeT]] = []

        def dfs2(node: NodeT, scc: list[NodeT]) -> None:
            visited.add(node)
            scc.append(node)
            if node in self.transpose:
                for neighbor in self.transpose[node]:
                    if neighbor not in visited:
                        dfs2(neighbor, scc)

        for node in reversed(finish_order):
            if node not in visited:
                scc: list[NodeT] = []
                dfs2(node, scc)
                sccs.append(scc)

        return sccs


def test_main() -> None:
    g: KosarajuSCC[int] = KosarajuSCC()
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(1, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 3)

    sccs = g.find_sccs()
    assert len(sccs) == 2
    assert sorted([sorted(scc) for scc in sccs]) == [[0, 1, 2], [3, 4, 5]]


# Don't write tests below during competition.


def test_single_node() -> None:
    g: KosarajuSCC[str] = KosarajuSCC()
    g.add_edge("A", "A")

    sccs = g.find_sccs()
    assert len(sccs) == 1
    assert sccs[0] == ["A"]


def test_no_edges() -> None:
    g: KosarajuSCC[int] = KosarajuSCC()
    g.add_edge(1, 2)
    g.add_edge(3, 4)

    sccs = g.find_sccs()
    assert len(sccs) == 4
    assert sorted([sorted(scc) for scc in sccs]) == [[1], [2], [3], [4]]


def test_fully_connected() -> None:
    g: KosarajuSCC[int] = KosarajuSCC()
    # Create cycle: 0->1->2->3->0
    for i in range(4):
        g.add_edge(i, (i + 1) % 4)

    sccs = g.find_sccs()
    assert len(sccs) == 1
    assert sorted(sccs[0]) == [0, 1, 2, 3]


def test_linear_chain() -> None:
    g: KosarajuSCC[int] = KosarajuSCC()
    # Linear: 0->1->2->3->4
    for i in range(4):
        g.add_edge(i, i + 1)

    sccs = g.find_sccs()
    assert len(sccs) == 5
    # Each node is its own SCC
    assert sorted([sorted(scc) for scc in sccs]) == [[0], [1], [2], [3], [4]]


def test_multiple_components() -> None:
    g: KosarajuSCC[str] = KosarajuSCC()
    # First SCC: A->B->C->A
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")
    # Second SCC: D->E->D
    g.add_edge("D", "E")
    g.add_edge("E", "D")
    # Connection between SCCs
    g.add_edge("C", "D")

    sccs = g.find_sccs()
    assert len(sccs) == 2
    assert sorted([sorted(scc) for scc in sccs]) == [["A", "B", "C"], ["D", "E"]]


def test_complex_graph() -> None:
    g: KosarajuSCC[int] = KosarajuSCC()
    # SCC1: 0->1->2->0
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    # SCC2: 3->4->3
    g.add_edge(3, 4)
    g.add_edge(4, 3)
    # SCC3: 5->6->7->5
    g.add_edge(5, 6)
    g.add_edge(6, 7)
    g.add_edge(7, 5)
    # Connections between SCCs
    g.add_edge(2, 3)
    g.add_edge(4, 5)

    sccs = g.find_sccs()
    assert len(sccs) == 3
    assert sorted([sorted(scc) for scc in sccs]) == [[0, 1, 2], [3, 4], [5, 6, 7]]


def test_single_node_no_self_loop() -> None:
    g: KosarajuSCC[int] = KosarajuSCC()
    g.graph[42] = []
    g.transpose[42] = []

    sccs = g.find_sccs()
    assert len(sccs) == 1
    assert sccs[0] == [42]


def test_bidirectional_edges() -> None:
    g: KosarajuSCC[int] = KosarajuSCC()
    # Bidirectional edges form SCC
    g.add_edge(1, 2)
    g.add_edge(2, 1)
    g.add_edge(2, 3)
    g.add_edge(3, 2)

    sccs = g.find_sccs()
    assert len(sccs) == 1
    assert sorted(sccs[0]) == [1, 2, 3]


def test_large_graph() -> None:
    g: KosarajuSCC[int] = KosarajuSCC()
    # Create 10 SCCs, each with 5 nodes in a cycle
    for scc_id in range(10):
        base = scc_id * 5
        for i in range(5):
            g.add_edge(base + i, base + (i + 1) % 5)
        # Connect to next SCC
        if scc_id < 9:
            g.add_edge(base + 4, (scc_id + 1) * 5)

    sccs = g.find_sccs()
    assert len(sccs) == 10
    # Each SCC should have 5 nodes
    for scc in sccs:
        assert len(scc) == 5


def main() -> None:
    test_main()
    test_single_node()
    test_no_edges()
    test_fully_connected()
    test_linear_chain()
    test_multiple_components()
    test_complex_graph()
    test_single_node_no_self_loop()
    test_bidirectional_edges()
    test_large_graph()


if __name__ == "__main__":
    main()
