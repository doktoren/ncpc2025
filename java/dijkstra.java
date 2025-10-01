/*
Dijkstra's algorithm for single-source shortest paths in weighted graphs.

Finds shortest paths from a source vertex to all other vertices in a graph
with non-negative edge weights.

Key operations:
- addEdge(u, v, weight): Add weighted directed edge
- shortestPaths(source): Compute shortest paths from source to all vertices
- shortestPath(source, target): Get shortest path between two vertices

Time complexity: O((V + E) log V) with binary heap
Space complexity: O(V + E)
*/

import java.util.*;

class dijkstra {
    static class Edge {
        int to;
        int weight;

        Edge(int to, int weight) {
            this.to = to;
            this.weight = weight;
        }
    }

    static class Node implements Comparable<Node> {
        int vertex;
        int distance;

        Node(int vertex, int distance) {
            this.vertex = vertex;
            this.distance = distance;
        }

        @Override
        public int compareTo(Node other) {
            return Integer.compare(this.distance, other.distance);
        }
    }

    static class Dijkstra {
        private int n;
        private Map<Integer, List<Edge>> graph;

        Dijkstra(int n) {
            this.n = n;
            this.graph = new HashMap<>();
            for (int i = 0; i < n; i++) {
                graph.put(i, new ArrayList<>());
            }
        }

        void addEdge(int u, int v, int weight) {
            graph.get(u).add(new Edge(v, weight));
        }

        Map<Integer, Integer> shortestPaths(int source) {
            Map<Integer, Integer> distances = new HashMap<>();
            for (int i = 0; i < n; i++) {
                distances.put(i, Integer.MAX_VALUE);
            }
            distances.put(source, 0);

            PriorityQueue<Node> pq = new PriorityQueue<>();
            pq.offer(new Node(source, 0));

            while (!pq.isEmpty()) {
                Node current = pq.poll();
                int u = current.vertex;
                int dist = current.distance;

                if (dist > distances.get(u)) {
                    continue;
                }

                for (Edge edge : graph.get(u)) {
                    int v = edge.to;
                    int newDist = dist + edge.weight;

                    if (newDist < distances.get(v)) {
                        distances.put(v, newDist);
                        pq.offer(new Node(v, newDist));
                    }
                }
            }

            return distances;
        }

        List<Integer> shortestPath(int source, int target) {
            Map<Integer, Integer> distances = new HashMap<>();
            Map<Integer, Integer> previous = new HashMap<>();

            for (int i = 0; i < n; i++) {
                distances.put(i, Integer.MAX_VALUE);
            }
            distances.put(source, 0);

            PriorityQueue<Node> pq = new PriorityQueue<>();
            pq.offer(new Node(source, 0));

            while (!pq.isEmpty()) {
                Node current = pq.poll();
                int u = current.vertex;
                int dist = current.distance;

                if (u == target) {
                    break;
                }

                if (dist > distances.get(u)) {
                    continue;
                }

                for (Edge edge : graph.get(u)) {
                    int v = edge.to;
                    int newDist = dist + edge.weight;

                    if (newDist < distances.get(v)) {
                        distances.put(v, newDist);
                        previous.put(v, u);
                        pq.offer(new Node(v, newDist));
                    }
                }
            }

            if (!previous.containsKey(target) && target != source) {
                return null;
            }

            List<Integer> path = new ArrayList<>();
            int current = target;
            while (current != source) {
                path.add(current);
                current = previous.get(current);
            }
            path.add(source);
            Collections.reverse(path);

            return path;
        }
    }

    static void testMain() {
        Dijkstra d = new Dijkstra(4);
        d.addEdge(0, 1, 4);
        d.addEdge(0, 2, 2);
        d.addEdge(1, 2, 1);
        d.addEdge(1, 3, 5);
        d.addEdge(2, 3, 8);

        Map<Integer, Integer> distances = d.shortestPaths(0);
        assert distances.get(3) == 9;

        List<Integer> path = d.shortestPath(0, 3);
        assert path.equals(Arrays.asList(0, 1, 3));
    }

    // Don't write tests below during competition.

    static void testSimplePath() {
        Dijkstra d = new Dijkstra(3);
        d.addEdge(0, 1, 5);
        d.addEdge(1, 2, 3);

        Map<Integer, Integer> distances = d.shortestPaths(0);
        assert distances.get(2) == 8;
    }

    static void testNoPath() {
        Dijkstra d = new Dijkstra(3);
        d.addEdge(0, 1, 1);

        Map<Integer, Integer> distances = d.shortestPaths(0);
        assert distances.get(2) == Integer.MAX_VALUE;

        List<Integer> path = d.shortestPath(0, 2);
        assert path == null;
    }

    static void testSelfLoop() {
        Dijkstra d = new Dijkstra(2);
        d.addEdge(0, 0, 5);
        d.addEdge(0, 1, 3);

        Map<Integer, Integer> distances = d.shortestPaths(0);
        assert distances.get(0) == 0;
        assert distances.get(1) == 3;
    }

    public static void main(String[] args) {
        testSimplePath();
        testNoPath();
        testSelfLoop();
        testMain();
        System.out.println("All tests passed!");
    }
}
