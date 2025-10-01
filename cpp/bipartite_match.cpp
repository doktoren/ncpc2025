/*
A bipartite matching algorithm finds the largest set of pairings between two disjoint vertex sets U and V
in a bipartite graph such that no vertex is in more than one pair.

Augmenting paths: repeatedly search for a path that alternates between unmatched and matched edges,
starting and ending at free vertices. Flipping the edges along such a path increases the matching size by 1.

Time complexity: O(V · E), where V is the number of vertices and E the number of edges.
*/

#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
#include <cassert>

template<typename SourceT, typename SinkT>
class BipartiteMatch {
private:
    std::map<SourceT, std::vector<SinkT>> edges;
    std::map<SourceT, SinkT> used_sources;
    std::map<SinkT, SourceT> used_sinks;
    std::map<SourceT, int> coloring;

    void flip(std::vector<SourceT>& source_stack, std::vector<SinkT>& sink_stack) {
        while (!source_stack.empty()) {
            used_sources[source_stack.back()] = sink_stack.back();
            used_sinks[sink_stack.back()] = source_stack.back();
            source_stack.pop_back();
            sink_stack.pop_back();
        }
    }

    bool update(SourceT start_source, int cur_color) {
        if (used_sources.find(start_source) != used_sources.end()) {
            return false;
        }

        std::vector<SourceT> source_stack = {start_source};
        std::vector<SinkT> sink_stack;
        std::vector<size_t> index_stack = {0};

        while (true) {
            SourceT source = source_stack.back();
            size_t index = index_stack.back();
            index_stack.pop_back();

            if (index == edges[source].size()) {
                if (index_stack.empty()) {
                    return false;
                }
                source_stack.pop_back();
                sink_stack.pop_back();
                continue;
            }
            index_stack.push_back(index + 1);

            SinkT sink = edges[source][index];
            sink_stack.push_back(sink);

            if (used_sinks.find(sink) == used_sinks.end()) {
                flip(source_stack, sink_stack);
                return true;
            }

            source = used_sinks[sink];
            if (coloring[source] == cur_color) {
                sink_stack.pop_back();
            } else {
                coloring[source] = cur_color;
                source_stack.push_back(source);
                index_stack.push_back(0);
            }
        }
    }

public:
    std::map<SourceT, SinkT> match;

    BipartiteMatch(const std::vector<std::pair<SourceT, SinkT>>& edge_list) {
        for (const auto& [source, sink] : edge_list) {
            edges[source].push_back(sink);
        }

        // Get ordered sources for deterministic behavior
        std::vector<SourceT> ordered_sources;
        for (const auto& [source, _] : edges) {
            ordered_sources.push_back(source);
            coloring[source] = 0;
        }

        // Initial pass
        for (const auto& [source, sink] : edge_list) {
            if (used_sources.find(source) == used_sources.end() &&
                used_sinks.find(sink) == used_sinks.end()) {
                used_sources[source] = sink;
                used_sinks[sink] = source;
                break;
            }
        }

        bool progress = true;
        int cur_color = 1;
        while (progress) {
            progress = false;
            for (const auto& source : ordered_sources) {
                if (update(source, cur_color)) {
                    progress = true;
                }
            }
            cur_color++;
        }

        match = used_sources;
    }
};

void test_main() {
    BipartiteMatch<int, std::string> b({
        {1, "X"}, {2, "Y"}, {3, "X"}, {1, "Z"}, {2, "Z"}, {3, "Y"}
    });
    assert(b.match.size() == 3);
    assert(b.match[1] == "Z");
    assert(b.match[2] == "Y");
    assert(b.match[3] == "X");
}

// Don't write tests below during competition.

void test_a() {
    BipartiteMatch<int, double> bm({
        {1, 2.2}, {2, 3.3}, {1, 1.1}, {2, 2.2}, {3, 3.3}
    });
    assert(bm.match[1] == 1.1);
    assert(bm.match[2] == 2.2);
    assert(bm.match[3] == 3.3);
}

void test_b() {
    BipartiteMatch<std::string, std::string> bm({
        {"1", "3"}, {"2", "4"}, {"3", "2"}, {"4", "4"}, {"1", "1"}
    });
    assert(bm.match["3"] == "2");
    assert(bm.match["1"] == "3");
    assert(bm.match["2"] == "4");
}

void test_c() {
    BipartiteMatch<int, std::string> bm({
        {1, "B"}, {2, "A"}, {3, "A"}
    });
    assert(bm.match[1] == "B");
    assert(bm.match[2] == "A");
    assert(bm.match.size() == 2);
}

void test_empty_graph() {
    BipartiteMatch<int, int> bm({});
    assert(bm.match.empty());
}

void test_single_edge() {
    BipartiteMatch<int, int> bm({{1, 2}});
    assert(bm.match.size() == 1);
    assert(bm.match[1] == 2);
}

void test_no_matching() {
    // All sources want same sink
    BipartiteMatch<int, std::string> bm({
        {1, "A"}, {2, "A"}, {3, "A"}
    });
    // Only one can be matched
    assert(bm.match.size() == 1);
    assert(bm.match[bm.match.begin()->first] == "A");
}

void test_perfect_matching() {
    // Perfect matching possible
    BipartiteMatch<int, int> bm({
        {1, 10}, {2, 20}, {3, 30}
    });
    assert(bm.match.size() == 3);
}

void test_augmenting_path() {
    // Requires augmenting path to find maximum matching
    BipartiteMatch<int, std::string> bm({
        {1, "A"}, {1, "B"},
        {2, "B"}, {2, "C"},
        {3, "C"}
    });
    assert(bm.match.size() == 3);
}

void test_large_bipartite() {
    // Larger graph
    std::vector<std::pair<int, int>> edges;
    for (int i = 0; i < 10; i++) {
        for (int j = i; j < std::min(i + 3, 10); j++) {
            edges.push_back({i, j + 100});
        }
    }

    BipartiteMatch<int, int> bm(edges);
    // Should find a good matching
    assert(bm.match.size() >= 8);
}

int main() {
    test_a();
    test_b();
    test_c();
    test_empty_graph();
    test_single_edge();
    test_no_matching();
    test_perfect_matching();
    test_augmenting_path();
    test_large_bipartite();
    test_main();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}
