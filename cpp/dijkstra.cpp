/*
Dijkstra's algorithm for single-source shortest path in weighted graphs.

Finds shortest paths from a source vertex to all other vertices in a graph with
non-negative edge weights. Uses a priority queue (heap) for efficient vertex selection.

Time complexity: O((V + E) log V) with binary heap, where V is vertices and E is edges.
Space complexity: O(V + E) for the graph representation and auxiliary data structures.
*/

#include <iostream>
#include <vector>
#include <map>
#include <queue>
#include <set>
#include <optional>
#include <algorithm>
#include <cassert>
#include <limits>

template<typename NodeT, typename WeightT>
class Dijkstra {
private:
    WeightT infinity;
    WeightT zero;
    std::map<NodeT, std::vector<std::pair<NodeT, WeightT>>> graph;

public:
    Dijkstra(WeightT infinity, WeightT zero) : infinity(infinity), zero(zero) {}

    void add_edge(NodeT u, NodeT v, WeightT weight) {
        graph[u].push_back({v, weight});
    }

    std::pair<std::map<NodeT, WeightT>, std::map<NodeT, std::optional<NodeT>>>
    shortest_paths(NodeT source) {
        std::map<NodeT, WeightT> distances;
        std::map<NodeT, std::optional<NodeT>> predecessors;
        distances[source] = zero;
        predecessors[source] = std::nullopt;

        // Min heap: pair of (distance, node)
        std::priority_queue<
            std::pair<WeightT, NodeT>,
            std::vector<std::pair<WeightT, NodeT>>,
            std::greater<std::pair<WeightT, NodeT>>
        > pq;

        pq.push({zero, source});
        std::set<NodeT> visited;

        while (!pq.empty()) {
            auto [current_dist, u] = pq.top();
            pq.pop();

            if (visited.count(u)) {
                continue;
            }
            visited.insert(u);

            if (graph.find(u) == graph.end()) {
                continue;
            }

            for (const auto& [v, weight] : graph[u]) {
                WeightT new_dist = current_dist + weight;

                if (distances.find(v) == distances.end() || new_dist < distances[v]) {
                    distances[v] = new_dist;
                    predecessors[v] = u;
                    pq.push({new_dist, v});
                }
            }
        }

        return {distances, predecessors};
    }

    std::optional<std::vector<NodeT>> shortest_path(NodeT source, NodeT target) {
        auto [distances, predecessors] = shortest_paths(source);

        if (predecessors.find(target) == predecessors.end()) {
            return std::nullopt;
        }

        std::vector<NodeT> path;
        std::optional<NodeT> current = target;

        while (current.has_value()) {
            path.push_back(current.value());
            current = predecessors[current.value()];
        }

        std::reverse(path.begin(), path.end());
        return path;
    }
};

void test_main() {
    Dijkstra<std::string, double> d(std::numeric_limits<double>::infinity(), 0.0);
    d.add_edge("A", "B", 4.0);
    d.add_edge("A", "C", 2.0);
    d.add_edge("B", "C", 1.0);
    d.add_edge("B", "D", 5.0);
    d.add_edge("C", "D", 8.0);

    auto [distances, _] = d.shortest_paths("A");
    assert(distances["D"] == 9.0);

    auto path = d.shortest_path("A", "D");
    assert(path.has_value());
    assert(path.value() == std::vector<std::string>({"A", "B", "D"}));
}

// Don't write tests below during competition.

void test_single_node() {
    Dijkstra<std::string, double> d(std::numeric_limits<double>::infinity(), 0.0);

    auto [distances, predecessors] = d.shortest_paths("A");
    assert(distances.size() == 1);
    assert(distances["A"] == 0.0);
    assert(predecessors["A"] == std::nullopt);

    auto path = d.shortest_path("A", "A");
    assert(path.has_value());
    assert(path.value() == std::vector<std::string>({"A"}));
}

void test_unreachable_nodes() {
    Dijkstra<int, int> d(999999, 0);
    d.add_edge(1, 2, 5);
    d.add_edge(3, 4, 3);

    auto [distances, _] = d.shortest_paths(1);
    assert(distances[2] == 5);
    assert(distances.find(3) == distances.end());
    assert(distances.find(4) == distances.end());
}

void test_multiple_paths() {
    Dijkstra<std::string, int> d(999999, 0);
    d.add_edge("S", "A", 2);
    d.add_edge("S", "B", 2);
    d.add_edge("A", "T", 3);
    d.add_edge("B", "T", 3);

    auto [distances, _] = d.shortest_paths("S");
    assert(distances["T"] == 5);

    auto path = d.shortest_path("S", "T");
    assert(path.has_value());
    assert(path.value().size() == 3);
    assert(path.value()[0] == "S");
    assert(path.value()[2] == "T");
}

void test_self_loops() {
    Dijkstra<int, int> d(999999, 0);
    d.add_edge(1, 1, 5);
    d.add_edge(1, 2, 3);

    auto [distances, _] = d.shortest_paths(1);
    assert(distances[1] == 0);
    assert(distances[2] == 3);
}

int main() {
    test_single_node();
    test_unreachable_nodes();
    test_multiple_paths();
    test_self_loops();
    test_main();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}
