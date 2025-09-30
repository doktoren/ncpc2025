"""
A bipartite matching algorithm finds the largest set of pairings between two disjoint vertex sets U and V
in a bipartite graph such that no vertex is in more than one pair.

Augmenting paths: repeatedly search for a path that alternates between unmatched and matched edges,
starting and ending at free vertices. Flipping the edges along such a path increases the matching size by 1.

Time complexity: O(V · E), where V is the number of vertices and E the number of edges.
"""

from __future__ import annotations

from collections import defaultdict

# Don't use annotations during contest
from typing import Final, Generic, Protocol, TypeVar

from typing_extensions import Self


class Comparable(Protocol):
    def __lt__(self, other: Self, /) -> bool: ...


SourceT = TypeVar("SourceT", bound=Comparable)
SinkT = TypeVar("SinkT")


class BipartiteMatch(Generic[SourceT, SinkT]):
    def __init__(self, edges: list[tuple[SourceT, SinkT]]) -> None:
        self.edges: defaultdict[SourceT, list[SinkT]] = defaultdict(list)
        for source, sink in edges:
            self.edges[source].append(sink)

        # For deterministic behaviour
        ordered_sources = sorted(self.edges)

        used_sources: dict[SourceT, SinkT] = {}
        used_sinks: dict[SinkT, SourceT] = {}
        # Initial pass
        for source, sink in edges:
            if used_sources.get(source) is None and used_sinks.get(sink) is None:
                progress = True
                used_sources[source] = sink
                used_sinks[sink] = source
                break

        coloring = dict.fromkeys(ordered_sources, 0)

        def update(source: SourceT, cur_color: int) -> bool:
            sink = used_sources.get(source)
            if sink is not None:
                return False
            source_stack: list[SourceT] = [source]
            sink_stack: list[SinkT] = []
            index_stack: list[int] = [0]

            def flip() -> None:
                while source_stack:
                    used_sources[source_stack[-1]] = sink_stack[-1]
                    used_sinks[sink_stack[-1]] = source_stack[-1]
                    source_stack.pop()
                    sink_stack.pop()

            while True:
                source = source_stack[-1]
                index = index_stack.pop()
                if index == len(self.edges[source]):
                    if not index_stack:
                        return False
                    source_stack.pop()
                    sink_stack.pop()
                    continue
                index_stack.append(index + 1)

                sink = self.edges[source][index]
                sink_stack.append(sink)
                if sink not in used_sinks:
                    flip()
                    return True
                source = used_sinks[sink]
                if coloring[source] == cur_color:
                    sink_stack.pop()
                else:
                    coloring[source] = cur_color
                    source_stack.append(source)
                    index_stack.append(0)

        progress = True
        cur_color = 1
        while progress:
            progress = any(update(source, cur_color) for source in ordered_sources)
            cur_color += 1

        self.match: Final = used_sources


def test_main() -> None:
    b = BipartiteMatch([(1, "X"), (2, "Y"), (3, "X"), (1, "Z"), (2, "Z"), (3, "Y")])
    assert len(b.match) == 3
    assert b.match == {1: "Z", 2: "Y", 3: "X"}


# Don't write tests below during competition.


def test_a() -> None:
    bm: BipartiteMatch[int, float] = BipartiteMatch(
        [
            (1, 2.2),
            (2, 3.3),
            (1, 1.1),
            (2, 2.2),
            (3, 3.3),
        ]
    )
    assert bm.match == {1: 1.1, 2: 2.2, 3: 3.3}


def test_b() -> None:
    bm: BipartiteMatch[str, str] = BipartiteMatch(
        [
            ("1", "3"),
            ("2", "4"),
            ("3", "2"),
            ("4", "4"),
            ("1", "1"),
        ]
    )
    assert bm.match == {"3": "2", "1": "3", "2": "4"}


def test_c() -> None:
    bm: BipartiteMatch[int, str] = BipartiteMatch(
        [
            (1, "B"),
            (2, "A"),
            (3, "A"),
        ]
    )
    assert bm.match == {1: "B", 2: "A"}


def main() -> None:
    test_a()
    test_b()
    test_c()
    test_main()


if __name__ == "__main__":
    main()
