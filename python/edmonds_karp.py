"""
Edmonds-Karp is a specialization of the Ford-Fulkerson method for computing the maximum flow in a directed graph.

* It repeatedly searches for an augmenting path from source to sink.
* The search is done with BFS, guaranteeing the path found is the shortest (fewest edges).
* Each augmentation increases the total flow, and each edge's residual capacity is updated.
* The algorithm terminates when no augmenting path exists.

Time complexity: O(V · E²), where V is the number of vertices and E the number of edges.
"""

from __future__ import annotations

from collections import deque
from decimal import Decimal

# Don't use annotations during contest
from typing import Final, Generic, TypeVar

DEBUG: Final = True

CapacityT = TypeVar("CapacityT", int, float, Decimal)
NodeT = TypeVar("NodeT")


class Edge(Generic[NodeT, CapacityT]):
    def __init__(
        self,
        source: Node[NodeT, CapacityT],
        sink: Node[NodeT, CapacityT],
        capacity: CapacityT,
    ) -> None:
        self.source: Final[Node[NodeT, CapacityT]] = source
        self.sink: Final[Node[NodeT, CapacityT]] = sink
        self.original = True  # Part of the input graph or added for the algorithm?
        # Modified by EdmondsKarp.run
        self.initial_capacity: CapacityT = capacity
        self.capacity: CapacityT = capacity

    @property
    def rev(self) -> Edge[NodeT, CapacityT]:
        return self.sink.edges[self.source.node]

    @property
    def flow(self) -> CapacityT:
        return self.initial_capacity - self.capacity

    def __str__(self) -> str:
        return f"Edge({self.source.node}, {self.sink.node}, {self.capacity})"


class Node(Generic[NodeT, CapacityT]):
    def __init__(self, node: NodeT) -> None:
        self.node: Final = node
        self.edges: dict[NodeT, Edge[NodeT, CapacityT]] = {}
        # Modified by EdmondsKarp.run
        self.color = 0
        self.used_edge: Edge[NodeT, CapacityT] | None = None

    def __str__(self) -> str:
        return "Node({}, out={}, color={}, used_edge={})".format(
            self.node,
            ", ".join(str(edge) for edge in self.edges.values()),
            self.color,
            self.used_edge,
        )


class EdmondsKarp(Generic[NodeT, CapacityT]):
    def __init__(
        self,
        edges: list[tuple[NodeT, NodeT, CapacityT]],
        main_source: NodeT,
        main_sink: NodeT,
        zero: CapacityT,
    ) -> None:
        self.main_source: Final = main_source
        self.main_sink: Final = main_sink
        self.zero: Final[CapacityT] = zero
        self.color = 1
        self.total_flow: CapacityT = self.zero

        def init_nodes() -> dict[NodeT, Node[NodeT, CapacityT]]:
            nodes: dict[NodeT, Node[NodeT, CapacityT]] = {}
            for source_t, sink_t, capacity in edges:
                source = nodes.setdefault(source_t, Node(source_t))
                assert sink_t not in source.edges, f"The edge ({source_t}, {sink_t}) is specified more than once"
                source.edges[sink_t] = Edge(source, nodes.setdefault(sink_t, Node(sink_t)), capacity)
            for source_t, sink_t, _ in edges:
                sink = nodes[sink_t]
                if source_t not in sink.edges:
                    edge = Edge(sink, nodes[source_t], zero)
                    edge.original = False
                    sink.edges[source_t] = edge
            nodes.setdefault(main_source, Node(main_source))
            nodes.setdefault(main_sink, Node(main_sink))
            return nodes

        self.nodes: dict[NodeT, Node[NodeT, CapacityT]] = init_nodes()

    def change_initial_capacities(self, edges: list[tuple[NodeT, NodeT, CapacityT]]) -> None:
        """Update edge capacities. REQUIRES: new capacity >= current flow."""
        for source, sink, capacity in edges:
            edge = self.nodes[source].edges[sink]
            assert capacity >= edge.flow
            increase = capacity - edge.initial_capacity
            edge.initial_capacity += increase
            edge.capacity += increase

    def reset_flows(self) -> None:
        """Reset all flows to zero, keeping capacities."""
        self.total_flow = self.zero
        for node in self.nodes.values():
            for edge in node.edges.values():
                edge.capacity = edge.initial_capacity

    def run(self) -> None:
        """Run max-flow algorithm from source to sink."""
        self.color += 1
        progress = True
        while progress:
            progress = False

            border: deque[Node[NodeT, CapacityT]] = deque()
            self.nodes[self.main_source].color = self.color
            border.append(self.nodes[self.main_source])
            while border:
                source = border.popleft()
                for edge in source.edges.values():
                    sink = edge.sink
                    if sink.color == self.color or edge.capacity == self.zero:
                        continue

                    sink.used_edge = edge
                    sink.color = self.color
                    border.append(sink)

                    if sink.node == self.main_sink:
                        used_edge = edge
                        flow = used_edge.capacity
                        while used_edge.source.node != self.main_source:
                            assert used_edge.source.used_edge is not None
                            used_edge = used_edge.source.used_edge
                            flow = min(flow, used_edge.capacity)

                        self.total_flow += flow

                        used_edge = sink.used_edge
                        used_edge.capacity -= flow
                        used_edge.rev.capacity += flow
                        while used_edge.source.node != self.main_source:
                            assert used_edge.source.used_edge is not None
                            used_edge = used_edge.source.used_edge
                            used_edge.capacity -= flow
                            used_edge.rev.capacity += flow

                        progress = True
                        self.color += 1
                        border.clear()
                        break

    def print(self) -> None:
        """Print all edges with non-zero flow for debugging."""
        if DEBUG:
            for node in self.nodes.values():
                for edge in node.edges.values():
                    if edge.capacity < edge.initial_capacity:
                        print(f"Flow {edge.source.node} ---{edge.flow}/{edge.initial_capacity}---> {edge.sink.node}")


def test_main() -> None:
    e = EdmondsKarp([(0, 1, 10), (0, 2, 8), (1, 2, 2), (1, 3, 5), (2, 3, 7)], 0, 3, 0)
    e.run()
    assert e.total_flow == 12


# Don't write tests below during competition.


def test_a() -> None:
    bm = EdmondsKarp(
        [
            (0, 1, 1),
            (0, 2, 1),
            (0, 3, 1),
            (1, 12, 1),
            (2, 13, 1),
            (1, 11, 1),
            (2, 12, 1),
            (3, 13, 1),
            (11, 42, 1),
            (12, 42, 1),
            (13, 42, 1),
        ],
        main_source=0,
        main_sink=42,
        zero=0,
    )
    bm.run()
    bm.print()
    assert bm.total_flow == 3, bm.total_flow


def test_b() -> None:
    bm = EdmondsKarp(
        [
            # The +1 is to truncate to current decimal precision
            (0, 1, Decimal(1 / 3) + 0),
            (1, 2, Decimal(1 / 7) + 0),
            (2, 0, Decimal(1 / 9) + 0),
        ],
        main_source=1,
        main_sink=0,
        zero=Decimal(0),
    )
    bm.run()
    bm.print()
    assert bm.total_flow == Decimal(1 / 9) + 0, bm.total_flow


def test_c() -> None:
    bm = EdmondsKarp(
        [
            ("source", "a", 1),
            ("source", "b", 2),
            ("b", "a", 1),
            ("a", "sink", 2),
            ("b", "sink", 1),
        ],
        main_source="source",
        main_sink="sink",
        zero=0,
    )
    bm.run()
    bm.print()
    assert bm.total_flow == 3, bm.total_flow


def test_d() -> None:
    bm = EdmondsKarp([], main_source="source", main_sink="sink", zero=0)
    bm.run()
    bm.print()
    assert bm.total_flow == 0, bm.total_flow


def test_single_edge() -> None:
    bm = EdmondsKarp([(0, 1, 5)], main_source=0, main_sink=1, zero=0)
    bm.run()
    assert bm.total_flow == 5


def test_no_path() -> None:
    # No path from source to sink
    bm = EdmondsKarp([(0, 1, 5), (2, 3, 5)], main_source=0, main_sink=3, zero=0)
    bm.run()
    assert bm.total_flow == 0


def test_bottleneck() -> None:
    # Path with bottleneck
    bm = EdmondsKarp([(0, 1, 100), (1, 2, 1), (2, 3, 100)], main_source=0, main_sink=3, zero=0)
    bm.run()
    assert bm.total_flow == 1


def test_parallel_edges() -> None:
    # Multiple parallel paths
    bm = EdmondsKarp(
        [(0, 1, 5), (0, 2, 5), (1, 3, 5), (2, 3, 5)],
        main_source=0,
        main_sink=3,
        zero=0,
    )
    bm.run()
    assert bm.total_flow == 10


def test_reset_flows() -> None:
    bm = EdmondsKarp([(0, 1, 10), (1, 2, 10)], main_source=0, main_sink=2, zero=0)
    bm.run()
    assert bm.total_flow == 10

    bm.reset_flows()
    assert bm.total_flow == 0

    bm.run()
    assert bm.total_flow == 10


def test_change_capacity() -> None:
    bm = EdmondsKarp([(0, 1, 5), (1, 2, 10)], main_source=0, main_sink=2, zero=0)
    bm.run()
    assert bm.total_flow == 5

    # Increase capacity of bottleneck edge
    bm.change_initial_capacities([(0, 1, 8)])
    bm.run()
    assert bm.total_flow == 8  # Can now push 3 more


def main() -> None:
    test_a()
    print()
    test_b()
    print()
    test_c()
    print()
    test_d()
    print()
    test_single_edge()
    test_no_path()
    test_bottleneck()
    test_parallel_edges()
    test_reset_flows()
    test_change_capacity()
    test_main()


if __name__ == "__main__":
    main()
