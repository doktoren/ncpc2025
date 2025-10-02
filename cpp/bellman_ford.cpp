/*
Bellman-Ford algorithm for single-source shortest paths with negative edge weights.

Time complexity: O(VE) where V is vertices and E is edges.
Space complexity: O(V + E).
*/

#include <algorithm>
#include <cassert>
#include <iostream>
#include <limits>
#include <map>
#include <optional>
#include <set>
#include <vector>

template <typename NodeT, typename WeightT>
class BellmanFord {
  private:
    struct Edge {
        NodeT from, to;
        WeightT weight;
    };

    std::vector<Edge> edges;
    std::set<NodeT> nodes;
    WeightT infinity;

  public:
    BellmanFord(WeightT infinity) : infinity(infinity) {}

    void add_edge(NodeT u, NodeT v, WeightT weight) {
        edges.push_back({u, v, weight});
        nodes.insert(u);
        nodes.insert(v);
    }

    std::optional<std::map<NodeT, WeightT>> shortest_paths(NodeT source) {
        std::map<NodeT, WeightT> distances;
        for (const auto& node : nodes) { distances[node] = infinity; }
        distances[source] = 0;

        for (size_t i = 0; i < nodes.size() - 1; i++) {
            for (const auto& e : edges) {
                if (distances[e.from] != infinity &&
                    distances[e.from] + e.weight < distances[e.to]) {
                    distances[e.to] = distances[e.from] + e.weight;
                }
            }
        }

        for (const auto& e : edges) {
            if (distances[e.from] != infinity && distances[e.from] + e.weight < distances[e.to]) {
                return std::nullopt;
            }
        }

        return distances;
    }
};

void test_main() {
    BellmanFord<int, int> bf(999999);
    bf.add_edge(0, 1, 4);
    bf.add_edge(0, 2, 2);
    bf.add_edge(1, 2, -3);
    bf.add_edge(2, 3, 2);
    bf.add_edge(3, 1, 1);

    auto result = bf.shortest_paths(0);
    assert(result.has_value());
    assert(result.value()[2] == 1);
    assert(result.value()[3] == 3);
}

// Don't write tests below during competition.

void test_negative_cycle() {
    BellmanFord<int, int> bf(999999);
    bf.add_edge(0, 1, 1);
    bf.add_edge(1, 2, -3);
    bf.add_edge(2, 0, 1);
    assert(!bf.shortest_paths(0).has_value());
}

void test_unreachable_nodes() {
    BellmanFord<int, int> bf(999999);
    bf.add_edge(1, 2, 5);
    bf.add_edge(3, 4, 3);
    auto result = bf.shortest_paths(1);
    assert(result.has_value());
    assert(result.value()[2] == 5);
    assert(result.value()[3] == 999999);
}

void test_all_negative_edges() {
    BellmanFord<int, int> bf(999999);
    bf.add_edge(0, 1, -1);
    bf.add_edge(1, 2, -2);
    bf.add_edge(2, 3, -3);
    auto result = bf.shortest_paths(0);
    assert(result.has_value());
    assert(result.value()[3] == -6);
}

int main() {
    test_main();
    test_negative_cycle();
    test_unreachable_nodes();
    test_all_negative_edges();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}
