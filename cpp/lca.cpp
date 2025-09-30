/*
Lowest Common Ancestor (LCA) using binary lifting preprocessing.

Finds the lowest common ancestor of two nodes in a tree efficiently after O(n log n)
preprocessing. Binary lifting allows answering LCA queries in O(log n) time by
maintaining ancestors at powers-of-2 distances.

Time complexity: O(n log n) preprocessing, O(log n) per LCA query.
Space complexity: O(n log n) for the binary lifting table.
*/

#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <algorithm>
#include <stdexcept>
#include <cassert>

template<typename NodeT>
class LCA {
private:
    NodeT root;
    std::map<NodeT, std::vector<NodeT>> graph;
    std::map<NodeT, int> depth;
    std::map<NodeT, std::map<int, NodeT>> up;  // up[node][i] = 2^i-th ancestor
    std::set<NodeT> has_parent;  // nodes that have a parent
    int max_log;

    void dfs_depth(NodeT node, bool has_par, NodeT par, int d) {
        depth[node] = d;
        for (const auto& neighbor : graph[node]) {
            if (!has_par || neighbor != par) {
                dfs_depth(neighbor, true, node, d + 1);
            }
        }
    }

    void dfs_parents(NodeT node, bool has_par, NodeT par) {
        if (has_par) {
            up[node][0] = par;
            has_parent.insert(node);
        }
        for (const auto& neighbor : graph[node]) {
            if (!has_par || neighbor != par) {
                dfs_parents(neighbor, true, node);
            }
        }
    }

public:
    LCA(NodeT root) : root(root), max_log(0) {}

    void add_edge(NodeT u, NodeT v) {
        graph[u].push_back(v);
        graph[v].push_back(u);
    }

    void preprocess() {
        // Find max depth to determine log table size
        dfs_depth(root, false, root, 0);

        int n = depth.size();
        max_log = 0;
        while ((1 << max_log) <= n) {
            max_log++;
        }

        // Fill first column (direct parents)
        dfs_parents(root, false, root);

        // Fill binary lifting table
        for (int j = 1; j < max_log; j++) {
            for (const auto& [node, _] : depth) {
                if (up[node].count(j - 1)) {
                    NodeT parent_j_minus_1 = up[node][j - 1];
                    if (up[parent_j_minus_1].count(j - 1)) {
                        up[node][j] = up[parent_j_minus_1][j - 1];
                    }
                }
            }
        }
    }

    NodeT lca(NodeT u, NodeT v) {
        if (depth[u] < depth[v]) {
            std::swap(u, v);
        }

        // Bring u to same level as v
        int diff = depth[u] - depth[v];
        for (int i = 0; i < max_log; i++) {
            if ((diff >> i) & 1) {
                if (up[u].count(i)) {
                    u = up[u][i];
                }
            }
        }

        if (u == v) {
            return u;
        }

        // Binary search for LCA
        for (int i = max_log - 1; i >= 0; i--) {
            bool u_has = up[u].count(i);
            bool v_has = up[v].count(i);
            if (u_has && v_has && up[u][i] != up[v][i]) {
                u = up[u][i];
                v = up[v][i];
            }
        }

        if (!up[u].count(0)) {
            throw std::runtime_error("LCA computation failed - invalid tree structure");
        }
        return up[u][0];
    }

    int distance(NodeT u, NodeT v) {
        NodeT lca_node = lca(u, v);
        return depth[u] + depth[v] - 2 * depth[lca_node];
    }
};

void test_main() {
    LCA<int> lca(1);
    std::vector<std::pair<int, int>> edges = {{1, 2}, {1, 3}, {2, 4}, {2, 5}, {3, 6}};
    for (const auto& [u, v] : edges) {
        lca.add_edge(u, v);
    }

    lca.preprocess();

    assert(lca.lca(4, 5) == 2);
    assert(lca.lca(4, 6) == 1);
    assert(lca.distance(4, 6) == 4);
}

// Don't write tests below during competition.

void test_linear_chain() {
    // Test on a simple linear chain: 1-2-3-4-5
    LCA<int> lca(1);
    std::vector<std::pair<int, int>> edges = {{1, 2}, {2, 3}, {3, 4}, {4, 5}};
    for (const auto& [u, v] : edges) {
        lca.add_edge(u, v);
    }

    lca.preprocess();

    // LCA of nodes at different depths
    assert(lca.lca(1, 5) == 1);
    assert(lca.lca(2, 5) == 2);
    assert(lca.lca(3, 5) == 3);
    assert(lca.lca(4, 5) == 4);
    assert(lca.lca(5, 5) == 5);

    // Distance tests
    assert(lca.distance(1, 5) == 4);
    assert(lca.distance(2, 4) == 2);
    assert(lca.distance(3, 3) == 0);
}

void test_single_node() {
    // Test with single node tree
    LCA<int> lca(1);
    lca.preprocess();

    assert(lca.lca(1, 1) == 1);
    assert(lca.distance(1, 1) == 0);
}

void test_binary_tree() {
    // Perfect binary tree
    LCA<int> lca(1);
    std::vector<std::pair<int, int>> edges = {{1, 2}, {1, 3}, {2, 4}, {2, 5}, {3, 6}, {3, 7}};
    for (const auto& [u, v] : edges) {
        lca.add_edge(u, v);
    }

    lca.preprocess();

    // Same parent
    assert(lca.lca(4, 5) == 2);
    assert(lca.lca(6, 7) == 3);

    // Different parents
    assert(lca.lca(4, 6) == 1);
    assert(lca.lca(5, 7) == 1);

    // One is ancestor of other
    assert(lca.lca(1, 4) == 1);
    assert(lca.lca(2, 5) == 2);

    // Distance tests
    assert(lca.distance(4, 5) == 2);
    assert(lca.distance(4, 7) == 4);
    assert(lca.distance(2, 3) == 2);
}

void test_star_tree() {
    // Star tree with center at 1
    LCA<int> lca(1);
    for (int i = 2; i <= 10; i++) {
        lca.add_edge(1, i);
    }

    lca.preprocess();

    // All pairs should have LCA = 1 (center)
    for (int i = 2; i <= 10; i++) {
        for (int j = i + 1; j <= 10; j++) {
            assert(lca.lca(i, j) == 1);
            assert(lca.distance(i, j) == 2);
        }
    }

    // Center to leaf
    for (int i = 2; i <= 10; i++) {
        assert(lca.lca(1, i) == 1);
        assert(lca.distance(1, i) == 1);
    }
}

void test_deep_tree() {
    // Deep tree (linear chain of depth 100)
    LCA<int> lca(1);
    for (int i = 1; i < 100; i++) {
        lca.add_edge(i, i + 1);
    }

    lca.preprocess();

    // Test some LCA queries
    assert(lca.lca(1, 100) == 1);
    assert(lca.lca(50, 100) == 50);
    assert(lca.lca(25, 75) == 25);

    // Distance tests
    assert(lca.distance(1, 100) == 99);
    assert(lca.distance(50, 60) == 10);
    assert(lca.distance(25, 75) == 50);
}

void test_string_nodes() {
    // Test with string node identifiers
    LCA<std::string> lca("root");
    lca.add_edge("root", "left");
    lca.add_edge("root", "right");
    lca.add_edge("left", "left_child");
    lca.add_edge("right", "right_child");

    lca.preprocess();

    assert(lca.lca("left_child", "right_child") == "root");
    assert(lca.lca("left", "left_child") == "left");
    assert(lca.distance("left_child", "right_child") == 4);
}

int main() {
    test_linear_chain();
    test_single_node();
    test_binary_tree();
    test_star_tree();
    test_deep_tree();
    test_string_nodes();
    test_main();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}
