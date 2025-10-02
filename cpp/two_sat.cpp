/*
2-SAT solver using Kosaraju's SCC algorithm on implication graph.

2-SAT determines if a Boolean formula in CNF with at most 2 literals per clause is satisfiable.

Time complexity: O(n + m) where n is variables and m is clauses.
Space complexity: O(n + m) for the implication graph.
*/

#include <algorithm>
#include <cassert>
#include <iostream>
#include <vector>

class TwoSAT {
  private:
    int n;
    std::vector<std::vector<int>> graph;
    std::vector<std::vector<int>> transpose;

    void dfs1(int node, std::vector<bool>& visited, std::vector<int>& finish_order) {
        visited[node] = true;
        for (int neighbor : graph[node]) {
            if (!visited[neighbor]) { dfs1(neighbor, visited, finish_order); }
        }
        finish_order.push_back(node);
    }

    void dfs2(int node, std::vector<bool>& visited, std::vector<int>& scc_id, int scc) {
        visited[node] = true;
        scc_id[node] = scc;
        for (int neighbor : transpose[node]) {
            if (!visited[neighbor]) { dfs2(neighbor, visited, scc_id, scc); }
        }
    }

  public:
    TwoSAT(int n) : n(n), graph(2 * n), transpose(2 * n) {}

    void add_clause(int a, bool a_neg, int b, bool b_neg) {
        int a_node = 2 * a + (a_neg ? 1 : 0);
        int b_node = 2 * b + (b_neg ? 1 : 0);
        int na_node = 2 * a + (a_neg ? 0 : 1);
        int nb_node = 2 * b + (b_neg ? 0 : 1);

        graph[na_node].push_back(b_node);
        graph[nb_node].push_back(a_node);
        transpose[b_node].push_back(na_node);
        transpose[a_node].push_back(nb_node);
    }

    std::vector<bool> solve() {
        std::vector<bool> visited(2 * n, false);
        std::vector<int> finish_order;

        for (int node = 0; node < 2 * n; node++) {
            if (!visited[node]) { dfs1(node, visited, finish_order); }
        }

        std::fill(visited.begin(), visited.end(), false);
        std::vector<int> scc_id(2 * n);
        int current_scc = 0;

        for (int i = finish_order.size() - 1; i >= 0; i--) {
            int node = finish_order[i];
            if (!visited[node]) {
                dfs2(node, visited, scc_id, current_scc);
                current_scc++;
            }
        }

        for (int i = 0; i < n; i++) {
            if (scc_id[2 * i] == scc_id[2 * i + 1]) { return {}; }
        }

        std::vector<bool> assignment(n);
        for (int i = 0; i < n; i++) { assignment[i] = scc_id[2 * i] > scc_id[2 * i + 1]; }

        return assignment;
    }
};

void test_main() {
    TwoSAT sat(2);
    sat.add_clause(0, false, 1, false);
    sat.add_clause(0, true, 1, false);
    sat.add_clause(0, false, 1, true);

    auto result = sat.solve();
    assert(!result.empty());
    assert(result[0] || result[1]);
    assert(!result[0] || result[1]);
    assert(result[0] || !result[1]);
}

// Don't write tests below during competition.

void test_unsatisfiable() {
    TwoSAT sat(2);
    sat.add_clause(0, false, 1, false);
    sat.add_clause(0, false, 1, true);
    sat.add_clause(0, true, 1, false);
    sat.add_clause(0, true, 1, true);
    assert(sat.solve().empty());
}

void test_single_variable() {
    TwoSAT sat(1);
    sat.add_clause(0, false, 0, false);
    auto result = sat.solve();
    assert(!result.empty());
    assert(result[0]);
}

void test_implication_chain() {
    TwoSAT sat(4);
    sat.add_clause(0, true, 1, false);
    sat.add_clause(1, true, 2, false);
    sat.add_clause(2, true, 3, false);
    auto result = sat.solve();
    assert(!result.empty());
}

void test_xor_constraint() {
    TwoSAT sat(2);
    sat.add_clause(0, false, 1, false);
    sat.add_clause(0, true, 1, true);
    auto result = sat.solve();
    assert(!result.empty());
    assert((result[0] && !result[1]) || (!result[0] && result[1]));
}

int main() {
    test_main();
    test_unsatisfiable();
    test_single_variable();
    test_implication_chain();
    test_xor_constraint();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}
