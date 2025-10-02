/*
Bellman-Ford algorithm for single-source shortest paths with negative edge weights.

Finds shortest paths from a source vertex to all other vertices, even with negative
edge weights. Can detect negative cycles.

Key operations:
- addEdge(u, v, weight): Add directed edge
- shortestPaths(source): Compute shortest paths, returns null if negative cycle detected
- shortestPath(source, target): Get shortest path between two vertices

Time complexity: O(VE)
Space complexity: O(V + E)
*/

import java.util.*;

class bellman_ford {
    static class Edge {
        int from, to, weight;

        Edge(int from, int to, int weight) {
            this.from = from;
            this.to = to;
            this.weight = weight;
        }
    }

    static class BellmanFord {
        private List<Edge> edges;
        private Set<Integer> nodes;
        private static final int INF = 999999;

        BellmanFord() {
            this.edges = new ArrayList<>();
            this.nodes = new HashSet<>();
        }

        void addEdge(int u, int v, int weight) {
            edges.add(new Edge(u, v, weight));
            nodes.add(u);
            nodes.add(v);
        }

        Map<Integer, Integer> shortestPaths(int source) {
            Map<Integer, Integer> distances = new HashMap<>();
            for (int node : nodes) {
                distances.put(node, INF);
            }
            distances.put(source, 0);

            // Relax edges V-1 times
            for (int i = 0; i < nodes.size() - 1; i++) {
                for (Edge e : edges) {
                    if (distances.get(e.from) != INF
                            && distances.get(e.from) + e.weight < distances.get(e.to)) {
                        distances.put(e.to, distances.get(e.from) + e.weight);
                    }
                }
            }

            // Check for negative cycles
            for (Edge e : edges) {
                if (distances.get(e.from) != INF
                        && distances.get(e.from) + e.weight < distances.get(e.to)) {
                    return null;
                }
            }

            return distances;
        }

        List<Integer> shortestPath(int source, int target) {
            Map<Integer, Integer> distances = new HashMap<>();
            Map<Integer, Integer> predecessors = new HashMap<>();

            for (int node : nodes) {
                distances.put(node, INF);
            }
            distances.put(source, 0);
            predecessors.put(source, null);

            for (int i = 0; i < nodes.size() - 1; i++) {
                for (Edge e : edges) {
                    if (distances.get(e.from) != INF
                            && distances.get(e.from) + e.weight < distances.get(e.to)) {
                        distances.put(e.to, distances.get(e.from) + e.weight);
                        predecessors.put(e.to, e.from);
                    }
                }
            }

            for (Edge e : edges) {
                if (distances.get(e.from) != INF
                        && distances.get(e.from) + e.weight < distances.get(e.to)) {
                    return null;
                }
            }

            if (!predecessors.containsKey(target)) {
                return null;
            }

            List<Integer> path = new ArrayList<>();
            Integer current = target;
            while (current != null) {
                path.add(current);
                current = predecessors.get(current);
            }
            Collections.reverse(path);
            return path;
        }
    }

    static void testMain() {
        BellmanFord bf = new BellmanFord();
        bf.addEdge(0, 1, 4);
        bf.addEdge(0, 2, 2);
        bf.addEdge(1, 2, -3);
        bf.addEdge(2, 3, 2);
        bf.addEdge(3, 1, 1);

        Map<Integer, Integer> result = bf.shortestPaths(0);
        assert result != null;
        assert result.get(2) == 1;
        assert result.get(3) == 3;

        List<Integer> path = bf.shortestPath(0, 3);
        assert path != null;
        assert path.get(0) == 0;
        assert path.get(path.size() - 1) == 3;
    }

    // Don't write tests below during competition.

    static void testNegativeCycle() {
        BellmanFord bf = new BellmanFord();
        bf.addEdge(0, 1, 1);
        bf.addEdge(1, 2, -3);
        bf.addEdge(2, 0, 1);

        Map<Integer, Integer> result = bf.shortestPaths(0);
        assert result == null;
    }

    static void testUnreachableNodes() {
        BellmanFord bf = new BellmanFord();
        bf.addEdge(1, 2, 5);
        bf.addEdge(3, 4, 3);

        Map<Integer, Integer> result = bf.shortestPaths(1);
        assert result != null;
        assert result.get(2) == 5;
        assert result.get(3) == 999999;
    }

    static void testAllNegativeEdges() {
        BellmanFord bf = new BellmanFord();
        bf.addEdge(0, 1, -1);
        bf.addEdge(1, 2, -2);
        bf.addEdge(2, 3, -3);

        Map<Integer, Integer> result = bf.shortestPaths(0);
        assert result != null;
        assert result.get(3) == -6;
    }

    static void testPathReconstruction() {
        BellmanFord bf = new BellmanFord();
        bf.addEdge(0, 1, 5);
        bf.addEdge(1, 2, 3);
        bf.addEdge(0, 2, 10);

        List<Integer> path = bf.shortestPath(0, 2);
        assert path != null;
        assert path.equals(Arrays.asList(0, 1, 2));
    }

    static void testNegativeEdgeRelaxation() {
        BellmanFord bf = new BellmanFord();
        bf.addEdge(0, 1, 10);
        bf.addEdge(0, 2, 5);
        bf.addEdge(2, 1, -8);

        Map<Integer, Integer> result = bf.shortestPaths(0);
        assert result != null;
        assert result.get(1) == -3;
    }

    static void testDisconnectedGraph() {
        BellmanFord bf = new BellmanFord();
        bf.addEdge(0, 1, 1);
        bf.addEdge(2, 3, 1);

        Map<Integer, Integer> result = bf.shortestPaths(0);
        assert result != null;
        assert result.get(1) == 1;
        assert result.get(2) == 999999;
    }

    static void testSelfLoopNegative() {
        BellmanFord bf = new BellmanFord();
        bf.addEdge(0, 0, -1);

        Map<Integer, Integer> result = bf.shortestPaths(0);
        assert result == null;
    }

    static void testComplexGraph() {
        BellmanFord bf = new BellmanFord();
        bf.addEdge(0, 1, 10);
        bf.addEdge(0, 4, 8);
        bf.addEdge(1, 2, 2);
        bf.addEdge(2, 3, 5);
        bf.addEdge(3, 4, 3);
        bf.addEdge(4, 3, 1);

        Map<Integer, Integer> result = bf.shortestPaths(0);
        assert result != null;
        assert result.get(3) == 9;
        assert result.get(4) == 8;
    }

    public static void main(String[] args) {
        testMain();
        testNegativeCycle();
        testUnreachableNodes();
        testAllNegativeEdges();
        testPathReconstruction();
        testNegativeEdgeRelaxation();
        testDisconnectedGraph();
        testSelfLoopNegative();
        testComplexGraph();
        System.out.println("All tests passed!");
    }
}
