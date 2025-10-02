/*
Edmonds-Karp is a specialization of the Ford-Fulkerson method for computing the maximum flow in a
directed graph.

* It repeatedly searches for an augmenting path from source to sink.
* The search is done with BFS, guaranteeing the path found is the shortest (fewest edges).
* Each augmentation increases the total flow, and each edge's residual capacity is updated.
* The algorithm terminates when no augmenting path exists.

Time complexity: O(V · E²), where V is the number of vertices and E the number of edges.
*/

#include <algorithm>
#include <cassert>
#include <iostream>
#include <limits>
#include <queue>
#include <vector>

template <typename T>
class EdmondsKarp {
  private:
    int n;
    std::vector<std::vector<T>> capacity;
    std::vector<std::vector<T>> flow;
    T total_flow;

  public:
    EdmondsKarp(int vertices) : n(vertices), total_flow(0) {
        capacity.assign(n, std::vector<T>(n, 0));
        flow.assign(n, std::vector<T>(n, 0));
    }

    void add_edge(int from, int to, T cap) {
        capacity[from][to] += cap;
    }

    bool bfs(int source, int sink, std::vector<int>& parent) {
        std::vector<bool> visited(n, false);
        std::queue<int> q;
        q.push(source);
        visited[source] = true;
        parent[source] = -1;

        while (!q.empty()) {
            int u = q.front();
            q.pop();

            for (int v = 0; v < n; v++) {
                // Check residual capacity: forward capacity minus forward flow, plus backward flow
                T residual = capacity[u][v] - flow[u][v];
                if (!visited[v] && residual > 0) {
                    q.push(v);
                    parent[v] = u;
                    visited[v] = true;
                    if (v == sink) { return true; }
                }
            }
        }
        return false;
    }

    T max_flow(int source, int sink) {
        total_flow = 0;
        std::vector<int> parent(n);

        while (bfs(source, sink, parent)) {
            T path_flow = std::numeric_limits<T>::max();

            // Find minimum residual capacity along the path
            for (int v = sink; v != source; v = parent[v]) {
                int u = parent[v];
                path_flow = std::min(path_flow, capacity[u][v] - flow[u][v]);
            }

            // Add path flow to overall flow
            for (int v = sink; v != source; v = parent[v]) {
                int u = parent[v];
                flow[u][v] += path_flow;
                flow[v][u] -= path_flow;
            }

            total_flow += path_flow;
        }

        return total_flow;
    }

    T get_total_flow() const {
        return total_flow;
    }
};

void test_main() {
    EdmondsKarp<int> e(4);
    e.add_edge(0, 1, 10);
    e.add_edge(0, 2, 8);
    e.add_edge(1, 2, 2);
    e.add_edge(1, 3, 5);
    e.add_edge(2, 3, 7);
    assert(e.max_flow(0, 3) == 12);
}

// Don't write tests below during competition.

void test_basic() {
    // Simple flow network
    // Paths: 0->1->3 (10), 0->2->3 (10), 0->1->2->3 (10) = 30 total
    EdmondsKarp<int> ek(4);
    ek.add_edge(0, 1, 20);
    ek.add_edge(0, 2, 10);
    ek.add_edge(1, 2, 30);
    ek.add_edge(1, 3, 10);
    ek.add_edge(2, 3, 20);

    int max_flow = ek.max_flow(0, 3);
    assert(max_flow == 30);
}

void test_no_flow() {
    // No path from source to sink
    EdmondsKarp<int> ek(4);
    ek.add_edge(0, 1, 10);
    ek.add_edge(2, 3, 10);

    int max_flow = ek.max_flow(0, 3);
    assert(max_flow == 0);
}

void test_single_edge() {
    // Single edge network
    EdmondsKarp<int> ek(2);
    ek.add_edge(0, 1, 5);

    int max_flow = ek.max_flow(0, 1);
    assert(max_flow == 5);
}

void test_bottleneck() {
    // Path with bottleneck
    EdmondsKarp<int> ek(4);
    ek.add_edge(0, 1, 100);
    ek.add_edge(1, 2, 1);
    ek.add_edge(2, 3, 100);

    int max_flow = ek.max_flow(0, 3);
    assert(max_flow == 1);
}

void test_parallel_edges() {
    // Multiple parallel paths
    EdmondsKarp<int> ek(4);
    ek.add_edge(0, 1, 5);
    ek.add_edge(0, 2, 5);
    ek.add_edge(1, 3, 5);
    ek.add_edge(2, 3, 5);

    int max_flow = ek.max_flow(0, 3);
    assert(max_flow == 10);
}

void test_empty_graph() {
    // Empty graph (no edges)
    EdmondsKarp<int> ek(2);
    int max_flow = ek.max_flow(0, 1);
    assert(max_flow == 0);
}

void test_complex_network() {
    // More complex network with multiple paths
    EdmondsKarp<int> ek(6);
    ek.add_edge(0, 1, 10);
    ek.add_edge(0, 2, 10);
    ek.add_edge(1, 2, 2);
    ek.add_edge(1, 3, 4);
    ek.add_edge(1, 4, 8);
    ek.add_edge(2, 4, 9);
    ek.add_edge(3, 5, 10);
    ek.add_edge(4, 3, 6);
    ek.add_edge(4, 5, 10);

    int max_flow = ek.max_flow(0, 5);
    assert(max_flow == 19);
}

int main() {
    test_basic();
    test_no_flow();
    test_single_edge();
    test_bottleneck();
    test_parallel_edges();
    test_empty_graph();
    test_complex_network();
    test_main();
    std::cout << "All Edmonds-Karp tests passed!" << std::endl;
    return 0;
}