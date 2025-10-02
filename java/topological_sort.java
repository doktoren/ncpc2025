/*
Topological sorting algorithms for Directed Acyclic Graphs (DAG).

Provides two implementations:
1. Kahn's algorithm (BFS-based) - detects cycles
2. DFS-based algorithm - also detects cycles

Both return a topological ordering of vertices if the graph is a DAG,
or null if a cycle is detected.

Time complexity: O(V + E)
Space complexity: O(V + E)
*/

import java.util.*;

class topological_sort {
    static class TopologicalSort {
        private int n;
        private Map<Integer, List<Integer>> graph;

        TopologicalSort(int n) {
            this.n = n;
            this.graph = new HashMap<>();
            for (int i = 0; i < n; i++) {
                graph.put(i, new ArrayList<>());
            }
        }

        void addEdge(int u, int v) {
            graph.get(u).add(v);
        }

        List<Integer> kahnSort() {
            int[] inDegree = new int[n];

            for (int u = 0; u < n; u++) {
                for (int v : graph.get(u)) {
                    inDegree[v]++;
                }
            }

            Queue<Integer> queue = new LinkedList<>();
            for (int i = 0; i < n; i++) {
                if (inDegree[i] == 0) {
                    queue.offer(i);
                }
            }

            List<Integer> result = new ArrayList<>();

            while (!queue.isEmpty()) {
                int u = queue.poll();
                result.add(u);

                for (int v : graph.get(u)) {
                    inDegree[v]--;
                    if (inDegree[v] == 0) {
                        queue.offer(v);
                    }
                }
            }

            if (result.size() != n) {
                return null; // Cycle detected
            }

            return result;
        }

        List<Integer> dfsSort() {
            Set<Integer> visited = new HashSet<>();
            Set<Integer> recStack = new HashSet<>();
            Stack<Integer> stack = new Stack<>();

            for (int i = 0; i < n; i++) {
                if (!visited.contains(i)) {
                    if (!dfsVisit(i, visited, recStack, stack)) {
                        return null; // Cycle detected
                    }
                }
            }

            List<Integer> result = new ArrayList<>();
            while (!stack.isEmpty()) {
                result.add(stack.pop());
            }

            return result;
        }

        private boolean dfsVisit(
                int u, Set<Integer> visited, Set<Integer> recStack, Stack<Integer> stack) {
            visited.add(u);
            recStack.add(u);

            for (int v : graph.get(u)) {
                if (!visited.contains(v)) {
                    if (!dfsVisit(v, visited, recStack, stack)) {
                        return false;
                    }
                } else if (recStack.contains(v)) {
                    return false; // Cycle detected
                }
            }

            recStack.remove(u);
            stack.push(u);
            return true;
        }

        boolean hasCycle() {
            return kahnSort() == null;
        }

        List<Integer> longestPath(int source) {
            List<Integer> topoOrder = kahnSort();
            if (topoOrder == null) {
                return null; // Has cycle
            }

            Map<Integer, Integer> dist = new HashMap<>();
            Map<Integer, Integer> parent = new HashMap<>();

            for (int i = 0; i < n; i++) {
                dist.put(i, Integer.MIN_VALUE);
            }
            dist.put(source, 0);

            for (int u : topoOrder) {
                if (dist.get(u) != Integer.MIN_VALUE) {
                    for (int v : graph.get(u)) {
                        if (dist.get(u) + 1 > dist.get(v)) {
                            dist.put(v, dist.get(u) + 1);
                            parent.put(v, u);
                        }
                    }
                }
            }

            // Find vertex with maximum distance
            int maxDist = Integer.MIN_VALUE;
            int endVertex = -1;
            for (int i = 0; i < n; i++) {
                if (dist.get(i) > maxDist) {
                    maxDist = dist.get(i);
                    endVertex = i;
                }
            }

            if (endVertex == -1 || maxDist == Integer.MIN_VALUE) {
                return Arrays.asList(source);
            }

            // Reconstruct path
            List<Integer> path = new ArrayList<>();
            int current = endVertex;
            while (current != source) {
                path.add(current);
                current = parent.get(current);
            }
            path.add(source);
            Collections.reverse(path);

            return path;
        }
    }

    static void testMain() {
        TopologicalSort ts = new TopologicalSort(6);
        int[][] edges = {{5, 2}, {5, 0}, {4, 0}, {4, 1}, {2, 3}, {3, 1}};
        for (int[] edge : edges) {
            ts.addEdge(edge[0], edge[1]);
        }

        List<Integer> kahnResult = ts.kahnSort();
        List<Integer> dfsResult = ts.dfsSort();

        assert kahnResult != null;
        assert dfsResult != null;
        assert !ts.hasCycle();

        // Test with cycle
        TopologicalSort tsCycle = new TopologicalSort(3);
        tsCycle.addEdge(0, 1);
        tsCycle.addEdge(1, 2);
        tsCycle.addEdge(2, 0);
        assert tsCycle.hasCycle();
    }

    // Don't write tests below during competition.

    static void testSimpleDAG() {
        TopologicalSort ts = new TopologicalSort(4);
        ts.addEdge(0, 1);
        ts.addEdge(0, 2);
        ts.addEdge(1, 3);
        ts.addEdge(2, 3);

        List<Integer> result = ts.kahnSort();
        assert result != null;
        assert result.get(0) == 0;
        assert result.get(3) == 3;
    }

    static void testCycle() {
        TopologicalSort ts = new TopologicalSort(3);
        ts.addEdge(0, 1);
        ts.addEdge(1, 2);
        ts.addEdge(2, 0);

        assert ts.kahnSort() == null;
        assert ts.dfsSort() == null;
        assert ts.hasCycle();
    }

    static void testSingleVertex() {
        TopologicalSort ts = new TopologicalSort(1);
        List<Integer> result = ts.kahnSort();
        assert result != null;
        assert result.equals(Arrays.asList(0));
    }

    static void testDisconnected() {
        TopologicalSort ts = new TopologicalSort(4);
        ts.addEdge(0, 1);
        ts.addEdge(2, 3);

        List<Integer> result = ts.kahnSort();
        assert result != null;
        assert result.size() == 4;
    }

    static void testLongestPath() {
        TopologicalSort ts = new TopologicalSort(6);
        ts.addEdge(0, 1);
        ts.addEdge(0, 2);
        ts.addEdge(1, 3);
        ts.addEdge(2, 3);
        ts.addEdge(3, 4);
        ts.addEdge(3, 5);

        List<Integer> path = ts.longestPath(0);
        assert path != null;
        assert path.get(0) == 0;
        assert path.size() >= 3;
    }

    static void testSelfLoop() {
        TopologicalSort ts = new TopologicalSort(2);
        ts.addEdge(0, 0);

        assert ts.kahnSort() == null;
        assert ts.hasCycle();
    }

    public static void main(String[] args) {
        testSimpleDAG();
        testCycle();
        testSingleVertex();
        testDisconnected();
        testLongestPath();
        testSelfLoop();
        testMain();
        System.out.println("All tests passed!");
    }
}
