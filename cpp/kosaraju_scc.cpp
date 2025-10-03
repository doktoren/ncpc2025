/*
Kosaraju's algorithm for finding strongly connected components (SCCs) in directed graphs.

A strongly connected component is a maximal set of vertices where every vertex is
reachable from every other vertex in the set. Uses two DFS passes.

Time complexity: O(V + E) where V is vertices and E is edges.
Space complexity: O(V + E) for graph representation and auxiliary structures.
*/

#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
#include <set>
#include <vector>

template <typename NodeT>
class KosarajuSCC {
  private:
    std::map<NodeT, std::vector<NodeT>> graph;
    std::map<NodeT, std::vector<NodeT>> transpose;

    void dfs1(NodeT node, std::set<NodeT>& visited, std::vector<NodeT>& finish_order) {
        visited.insert(node);
        if (graph.find(node) != graph.end()) {
            for (const auto& neighbor : graph[node]) {
                if (visited.find(neighbor) == visited.end()) {
                    dfs1(neighbor, visited, finish_order);
                }
            }
        }
        finish_order.push_back(node);
    }

    void dfs2(NodeT node, std::set<NodeT>& visited, std::vector<NodeT>& scc) {
        visited.insert(node);
        scc.push_back(node);
        if (transpose.find(node) != transpose.end()) {
            for (const auto& neighbor : transpose[node]) {
                if (visited.find(neighbor) == visited.end()) { dfs2(neighbor, visited, scc); }
            }
        }
    }

  public:
    void add_edge(NodeT u, NodeT v) {
        graph[u].push_back(v);
        transpose[v].push_back(u);
        graph.try_emplace(v, std::vector<NodeT>{});
        transpose.try_emplace(u, std::vector<NodeT>{});
    }

    std::vector<std::vector<NodeT>> find_sccs() {
        std::set<NodeT> visited;
        std::vector<NodeT> finish_order;

        for (const auto& [node, _] : graph) {
            if (visited.find(node) == visited.end()) { dfs1(node, visited, finish_order); }
        }

        visited.clear();
        std::vector<std::vector<NodeT>> sccs;

        for (auto it = finish_order.rbegin(); it != finish_order.rend(); ++it) {
            if (visited.find(*it) == visited.end()) {
                std::vector<NodeT> scc;
                dfs2(*it, visited, scc);
                sccs.push_back(scc);
            }
        }

        return sccs;
    }
};

void test_main() {
    KosarajuSCC<int> g;
    g.add_edge(0, 1);
    g.add_edge(1, 2);
    g.add_edge(2, 0);
    g.add_edge(1, 3);
    g.add_edge(3, 4);
    g.add_edge(4, 5);
    g.add_edge(5, 3);

    auto sccs = g.find_sccs();
    assert(sccs.size() == 2);

    std::vector<std::vector<int>> sorted;
    for (auto& scc : sccs) {
        std::sort(scc.begin(), scc.end());
        sorted.push_back(scc);
    }
    std::sort(sorted.begin(), sorted.end());

    assert(sorted[0] == std::vector<int>({0, 1, 2}));
    assert(sorted[1] == std::vector<int>({3, 4, 5}));
}

// Don't write tests below during competition.

void test_single_node() {
    KosarajuSCC<int> g;
    g.add_edge(1, 1);
    auto sccs = g.find_sccs();
    assert(sccs.size() == 1);
}

void test_no_edges() {
    KosarajuSCC<int> g;
    g.add_edge(1, 2);
    g.add_edge(3, 4);
    auto sccs = g.find_sccs();
    assert(sccs.size() == 4);
}

void test_fully_connected() {
    KosarajuSCC<int> g;
    for (int i = 0; i < 4; i++) { g.add_edge(i, (i + 1) % 4); }
    auto sccs = g.find_sccs();
    assert(sccs.size() == 1);
}

void test_linear_chain() {
    KosarajuSCC<int> g;
    for (int i = 0; i < 4; i++) { g.add_edge(i, i + 1); }
    auto sccs = g.find_sccs();
    assert(sccs.size() == 5);
}

void test_multiple_components() {
    KosarajuSCC<int> g;
    g.add_edge(0, 1);
    g.add_edge(1, 2);
    g.add_edge(2, 0);
    g.add_edge(3, 4);
    g.add_edge(4, 3);
    g.add_edge(2, 3);
    auto sccs = g.find_sccs();
    assert(sccs.size() == 2);
}

void test_complex_graph() {
    KosarajuSCC<int> g;
    g.add_edge(0, 1);
    g.add_edge(1, 2);
    g.add_edge(2, 0);
    g.add_edge(3, 4);
    g.add_edge(4, 3);
    g.add_edge(5, 6);
    g.add_edge(6, 7);
    g.add_edge(7, 5);
    g.add_edge(2, 3);
    g.add_edge(4, 5);
    auto sccs = g.find_sccs();
    assert(sccs.size() == 3);
}

void test_large_graph() {
    KosarajuSCC<int> g;
    for (int scc_id = 0; scc_id < 10; scc_id++) {
        int base = scc_id * 5;
        for (int i = 0; i < 5; i++) { g.add_edge(base + i, base + (i + 1) % 5); }
        if (scc_id < 9) { g.add_edge(base + 4, (scc_id + 1) * 5); }
    }
    auto sccs = g.find_sccs();
    assert(sccs.size() == 10);
}

int main() {
    test_main();
    test_single_node();
    test_no_edges();
    test_fully_connected();
    test_linear_chain();
    test_multiple_components();
    test_complex_graph();
    test_large_graph();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}
