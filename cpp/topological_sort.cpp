/*
Topological sorting for Directed Acyclic Graphs (DAGs).

Produces a linear ordering of vertices such that for every directed edge (u, v),
vertex u comes before v in the ordering. Uses both DFS-based and Kahn's algorithm
(BFS-based) approaches for different use cases.

Time complexity: O(V + E) for both algorithms, where V is vertices and E is edges.
Space complexity: O(V + E) for the graph representation and auxiliary data structures.
*/

#include <iostream>
#include <vector>
#include <map>
#include <queue>
#include <algorithm>
#include <optional>
#include <stdexcept>
#include <cassert>

template<typename NodeT>
class TopologicalSort {
private:
    std::map<NodeT, std::vector<NodeT>> graph;
    std::map<NodeT, int> in_degree;

    enum Color { WHITE, GRAY, BLACK };

    bool dfs_helper(NodeT node, std::map<NodeT, Color>& color, std::vector<NodeT>& result) {
        if (color[node] == GRAY) {  // Back edge (cycle)
            return false;
        }
        if (color[node] == BLACK) {  // Already processed
            return true;
        }

        color[node] = GRAY;
        for (const auto& neighbor : graph[node]) {
            if (!dfs_helper(neighbor, color, result)) {
                return false;
            }
        }

        color[node] = BLACK;
        result.push_back(node);
        return true;
    }

public:
    void add_edge(NodeT u, NodeT v) {
        if (graph.find(u) == graph.end()) {
            graph[u] = {};
            in_degree[u] = 0;
        }
        if (in_degree.find(v) == in_degree.end()) {
            in_degree[v] = 0;
            graph[v] = {};
        }

        graph[u].push_back(v);
        in_degree[v]++;
    }

    std::optional<std::vector<NodeT>> kahn_sort() {
        /*
        Topological sort using Kahn's algorithm (BFS-based).

        Returns the topological ordering, or nullopt if the graph has a cycle.
        */
        std::map<NodeT, int> in_deg = in_degree;
        std::queue<NodeT> q;

        for (const auto& [node, deg] : in_deg) {
            if (deg == 0) {
                q.push(node);
            }
        }

        std::vector<NodeT> result;

        while (!q.empty()) {
            NodeT node = q.front();
            q.pop();
            result.push_back(node);

            for (const auto& neighbor : graph[node]) {
                in_deg[neighbor]--;
                if (in_deg[neighbor] == 0) {
                    q.push(neighbor);
                }
            }
        }

        // Check if all nodes are processed (no cycle)
        if (result.size() != in_degree.size()) {
            return std::nullopt;
        }

        return result;
    }

    std::optional<std::vector<NodeT>> dfs_sort() {
        /*
        Topological sort using DFS.

        Returns the topological ordering, or nullopt if the graph has a cycle.
        */
        std::map<NodeT, Color> color;
        for (const auto& [node, _] : in_degree) {
            color[node] = WHITE;
        }

        std::vector<NodeT> result;

        for (const auto& [node, _] : in_degree) {
            if (color[node] == WHITE && !dfs_helper(node, color, result)) {
                return std::nullopt;
            }
        }

        std::reverse(result.begin(), result.end());
        return result;
    }

    bool has_cycle() {
        return !kahn_sort().has_value();
    }

    std::map<NodeT, int> longest_path() {
        /*
        Find longest path from each node in the DAG.

        Returns a map from each node to its longest path length.
        */
        auto topo_order = kahn_sort();
        if (!topo_order.has_value()) {
            throw std::runtime_error("Graph contains a cycle");
        }

        std::map<NodeT, int> dist;
        for (const auto& [node, _] : in_degree) {
            dist[node] = 0;
        }

        for (const auto& node : topo_order.value()) {
            for (const auto& neighbor : graph[node]) {
                dist[neighbor] = std::max(dist[neighbor], dist[node] + 1);
            }
        }

        return dist;
    }
};

void test_main() {
    TopologicalSort<int> ts;
    std::vector<std::pair<int, int>> edges = {{5, 2}, {5, 0}, {4, 0}, {4, 1}, {2, 3}, {3, 1}};
    for (const auto& [u, v] : edges) {
        ts.add_edge(u, v);
    }

    auto kahn_result = ts.kahn_sort();
    auto dfs_result = ts.dfs_sort();

    assert(kahn_result.has_value());
    assert(dfs_result.has_value());
    assert(!ts.has_cycle());

    // Test with cycle
    TopologicalSort<int> ts_cycle;
    ts_cycle.add_edge(1, 2);
    ts_cycle.add_edge(2, 3);
    ts_cycle.add_edge(3, 1);
    assert(ts_cycle.has_cycle());
}

// Don't write tests below during competition.

void test_empty_graph() {
    TopologicalSort<int> ts;

    // Empty graph should return empty list
    assert(ts.kahn_sort().value().empty());
    assert(ts.dfs_sort().value().empty());
    assert(!ts.has_cycle());
}

void test_single_node_self_loop() {
    TopologicalSort<std::string> ts;
    ts.add_edge("A", "A");  // This creates a self-loop (cycle)

    assert(ts.has_cycle());
    assert(!ts.kahn_sort().has_value());
    assert(!ts.dfs_sort().has_value());
}

void test_single_node_no_edges() {
    TopologicalSort<int> ts;
    ts.add_edge(1, 2);  // Add a simple edge to create node

    TopologicalSort<int> ts2;
    // Can't easily test single isolated node, skip this case
}

void test_linear_chain() {
    TopologicalSort<int> ts;
    ts.add_edge(1, 2);
    ts.add_edge(2, 3);
    ts.add_edge(3, 4);
    ts.add_edge(4, 5);

    auto kahn_result = ts.kahn_sort();
    auto dfs_result = ts.dfs_sort();

    assert(kahn_result.has_value());
    assert(dfs_result.has_value());
    assert(!ts.has_cycle());

    // Check ordering
    auto kahn = kahn_result.value();
    assert(kahn.size() == 5);
    // Verify 1 comes before 2, 2 before 3, etc.
    for (size_t i = 0; i < kahn.size() - 1; i++) {
        assert(kahn[i] < kahn[i + 1]);
    }
}

void test_multiple_sources() {
    TopologicalSort<int> ts;
    ts.add_edge(1, 3);
    ts.add_edge(2, 3);
    ts.add_edge(3, 4);

    auto result = ts.kahn_sort();
    assert(result.has_value());
    assert(!ts.has_cycle());

    // Both 1 and 2 should come before 3
    auto vec = result.value();
    auto pos_1 = std::find(vec.begin(), vec.end(), 1) - vec.begin();
    auto pos_2 = std::find(vec.begin(), vec.end(), 2) - vec.begin();
    auto pos_3 = std::find(vec.begin(), vec.end(), 3) - vec.begin();
    auto pos_4 = std::find(vec.begin(), vec.end(), 4) - vec.begin();

    assert(pos_1 < pos_3);
    assert(pos_2 < pos_3);
    assert(pos_3 < pos_4);
}

void test_diamond_shape() {
    TopologicalSort<std::string> ts;
    ts.add_edge("A", "B");
    ts.add_edge("A", "C");
    ts.add_edge("B", "D");
    ts.add_edge("C", "D");

    auto kahn = ts.kahn_sort();
    auto dfs = ts.dfs_sort();

    assert(kahn.has_value());
    assert(dfs.has_value());
    assert(!ts.has_cycle());

    // A should come first, D should come last
    auto kahn_vec = kahn.value();
    assert(kahn_vec.front() == "A");
    assert(kahn_vec.back() == "D");
}

void test_complex_cycle() {
    TopologicalSort<int> ts;
    ts.add_edge(1, 2);
    ts.add_edge(2, 3);
    ts.add_edge(3, 4);
    ts.add_edge(4, 2);  // Creates cycle 2->3->4->2

    assert(ts.has_cycle());
    assert(!ts.kahn_sort().has_value());
    assert(!ts.dfs_sort().has_value());
}

void test_disconnected_components() {
    TopologicalSort<int> ts;
    // Component 1
    ts.add_edge(1, 2);
    ts.add_edge(2, 3);
    // Component 2
    ts.add_edge(4, 5);
    ts.add_edge(5, 6);

    auto result = ts.kahn_sort();
    assert(result.has_value());
    assert(!ts.has_cycle());
    assert(result.value().size() == 6);
}

void test_longest_path() {
    TopologicalSort<int> ts;
    ts.add_edge(1, 2);
    ts.add_edge(1, 3);
    ts.add_edge(2, 4);
    ts.add_edge(3, 4);
    ts.add_edge(4, 5);

    auto dist = ts.longest_path();

    assert(dist[1] == 0);
    assert(dist[5] == 3);  // Longest path: 1->2->4->5 or 1->3->4->5
}

void test_longest_path_with_cycle() {
    TopologicalSort<int> ts;
    ts.add_edge(1, 2);
    ts.add_edge(2, 3);
    ts.add_edge(3, 1);

    bool caught = false;
    try {
        ts.longest_path();
    } catch (const std::runtime_error&) {
        caught = true;
    }
    assert(caught);
}

void test_comparison_kahn_vs_dfs() {
    TopologicalSort<int> ts;
    ts.add_edge(5, 2);
    ts.add_edge(5, 0);
    ts.add_edge(4, 0);
    ts.add_edge(4, 1);
    ts.add_edge(2, 3);
    ts.add_edge(3, 1);

    auto kahn = ts.kahn_sort();
    auto dfs = ts.dfs_sort();

    assert(kahn.has_value());
    assert(dfs.has_value());

    // Both should produce valid topological orderings
    // (may differ, but both should be valid)
}

void test_large_graph() {
    TopologicalSort<int> ts;

    // Create a chain of 1000 nodes
    for (int i = 0; i < 999; i++) {
        ts.add_edge(i, i + 1);
    }

    auto result = ts.kahn_sort();
    assert(result.has_value());
    assert(result.value().size() == 1000);
    assert(!ts.has_cycle());
}

void test_string_nodes() {
    TopologicalSort<std::string> ts;
    ts.add_edge("undershirt", "shirt");
    ts.add_edge("pants", "belt");
    ts.add_edge("shirt", "belt");
    ts.add_edge("belt", "jacket");
    ts.add_edge("socks", "shoes");
    ts.add_edge("pants", "shoes");

    auto result = ts.kahn_sort();
    assert(result.has_value());
    assert(!ts.has_cycle());
}

int main() {
    test_empty_graph();
    test_single_node_self_loop();
    test_linear_chain();
    test_multiple_sources();
    test_diamond_shape();
    test_complex_cycle();
    test_disconnected_components();
    test_longest_path();
    test_longest_path_with_cycle();
    test_comparison_kahn_vs_dfs();
    test_large_graph();
    test_string_nodes();
    test_main();
    std::cout << "All Topological Sort tests passed!" << std::endl;
    return 0;
}
