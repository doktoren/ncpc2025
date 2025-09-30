/*
Edmonds-Karp algorithm for computing maximum flow in a flow network.

Implementation of the Ford-Fulkerson method using BFS to find augmenting paths.
Guarantees O(V * E^2) time complexity.

Key operations:
- addEdge(u, v, capacity): Add a directed edge with given capacity
- maxFlow(source, sink): Compute maximum flow from source to sink

Space complexity: O(V^2) for adjacency matrix representation
*/

import java.util.*;

class edmonds_karp {
    static class EdmondsKarp {
        private int n;
        private int[][] capacity;
        private int[][] flow;

        EdmondsKarp(int n) {
            this.n = n;
            this.capacity = new int[n][n];
            this.flow = new int[n][n];
        }

        void addEdge(int u, int v, int cap) {
            capacity[u][v] += cap;
        }

        int maxFlow(int source, int sink) {
            // Reset flow
            for (int i = 0; i < n; i++) {
                Arrays.fill(flow[i], 0);
            }

            int totalFlow = 0;

            while (true) {
                // BFS to find augmenting path
                int[] parent = new int[n];
                Arrays.fill(parent, -1);
                parent[source] = source;

                Queue<Integer> queue = new LinkedList<>();
                queue.offer(source);

                while (!queue.isEmpty() && parent[sink] == -1) {
                    int u = queue.poll();

                    for (int v = 0; v < n; v++) {
                        if (parent[v] == -1 && capacity[u][v] - flow[u][v] > 0) {
                            parent[v] = u;
                            queue.offer(v);
                        }
                    }
                }

                // No augmenting path found
                if (parent[sink] == -1) {
                    break;
                }

                // Find minimum residual capacity along the path
                int pathFlow = Integer.MAX_VALUE;
                int v = sink;
                while (v != source) {
                    int u = parent[v];
                    pathFlow = Math.min(pathFlow, capacity[u][v] - flow[u][v]);
                    v = u;
                }

                // Update flow along the path
                v = sink;
                while (v != source) {
                    int u = parent[v];
                    flow[u][v] += pathFlow;
                    flow[v][u] -= pathFlow;
                    v = u;
                }

                totalFlow += pathFlow;
            }

            return totalFlow;
        }

        int getFlow(int u, int v) {
            return flow[u][v];
        }
    }

    static void testMain() {
        EdmondsKarp ek = new EdmondsKarp(4);
        ek.addEdge(0, 1, 10);
        ek.addEdge(0, 2, 10);
        ek.addEdge(1, 2, 2);
        ek.addEdge(1, 3, 10);
        ek.addEdge(2, 3, 10);

        int maxFlow = ek.maxFlow(0, 3);
        assert maxFlow == 20;
    }

    // Don't write tests below during competition.

    static void testSimpleFlow() {
        EdmondsKarp ek = new EdmondsKarp(3);
        ek.addEdge(0, 1, 5);
        ek.addEdge(1, 2, 3);

        assert ek.maxFlow(0, 2) == 3;
    }

    static void testMultiplePaths() {
        EdmondsKarp ek = new EdmondsKarp(4);
        ek.addEdge(0, 1, 10);
        ek.addEdge(0, 2, 10);
        ek.addEdge(1, 3, 10);
        ek.addEdge(2, 3, 10);

        assert ek.maxFlow(0, 3) == 20;
    }

    static void testBottleneck() {
        EdmondsKarp ek = new EdmondsKarp(4);
        ek.addEdge(0, 1, 100);
        ek.addEdge(1, 2, 1);
        ek.addEdge(2, 3, 100);

        assert ek.maxFlow(0, 3) == 1;
    }

    static void testComplexNetwork() {
        EdmondsKarp ek = new EdmondsKarp(6);
        ek.addEdge(0, 1, 16);
        ek.addEdge(0, 2, 13);
        ek.addEdge(1, 2, 10);
        ek.addEdge(1, 3, 12);
        ek.addEdge(2, 1, 4);
        ek.addEdge(2, 4, 14);
        ek.addEdge(3, 2, 9);
        ek.addEdge(3, 5, 20);
        ek.addEdge(4, 3, 7);
        ek.addEdge(4, 5, 4);

        assert ek.maxFlow(0, 5) == 23;
    }

    static void testNoPath() {
        EdmondsKarp ek = new EdmondsKarp(4);
        ek.addEdge(0, 1, 10);
        ek.addEdge(2, 3, 10);

        assert ek.maxFlow(0, 3) == 0;
    }

    static void testSingleEdge() {
        EdmondsKarp ek = new EdmondsKarp(2);
        ek.addEdge(0, 1, 42);

        assert ek.maxFlow(0, 1) == 42;
    }

    static void testZeroCapacity() {
        EdmondsKarp ek = new EdmondsKarp(3);
        ek.addEdge(0, 1, 0);
        ek.addEdge(1, 2, 10);

        assert ek.maxFlow(0, 2) == 0;
    }

    static void testMultipleEdges() {
        EdmondsKarp ek = new EdmondsKarp(3);
        ek.addEdge(0, 1, 5);
        ek.addEdge(0, 1, 5);
        ek.addEdge(1, 2, 10);

        assert ek.maxFlow(0, 2) == 10;
    }

    public static void main(String[] args) {
        testSimpleFlow();
        testMultiplePaths();
        testBottleneck();
        testComplexNetwork();
        testNoPath();
        testSingleEdge();
        testZeroCapacity();
        testMultipleEdges();
        testMain();
        System.out.println("All tests passed!");
    }
}
