/*
Kosaraju's algorithm for finding strongly connected components (SCCs) in directed graphs.

A strongly connected component is a maximal set of vertices where every vertex is
reachable from every other vertex in the set. Uses two DFS passes.

Key operations:
- addEdge(u, v): Add directed edge from u to v
- findSCCs(): Find all strongly connected components

Time complexity: O(V + E)
Space complexity: O(V + E)
*/

import java.util.*;

class kosaraju_scc {
    static class KosarajuSCC {
        private Map<Integer, List<Integer>> graph;
        private Map<Integer, List<Integer>> transpose;

        KosarajuSCC() {
            this.graph = new HashMap<>();
            this.transpose = new HashMap<>();
        }

        void addEdge(int u, int v) {
            graph.putIfAbsent(u, new ArrayList<>());
            graph.putIfAbsent(v, new ArrayList<>());
            transpose.putIfAbsent(u, new ArrayList<>());
            transpose.putIfAbsent(v, new ArrayList<>());

            graph.get(u).add(v);
            transpose.get(v).add(u);
        }

        List<List<Integer>> findSCCs() {
            // First DFS pass: compute finish order
            Set<Integer> visited = new HashSet<>();
            List<Integer> finishOrder = new ArrayList<>();

            for (int node : graph.keySet()) {
                if (!visited.contains(node)) {
                    dfs1(node, visited, finishOrder);
                }
            }

            // Second DFS pass: find SCCs on transpose graph
            visited.clear();
            List<List<Integer>> sccs = new ArrayList<>();

            for (int i = finishOrder.size() - 1; i >= 0; i--) {
                int node = finishOrder.get(i);
                if (!visited.contains(node)) {
                    List<Integer> scc = new ArrayList<>();
                    dfs2(node, visited, scc);
                    sccs.add(scc);
                }
            }

            return sccs;
        }

        private void dfs1(int node, Set<Integer> visited, List<Integer> finishOrder) {
            visited.add(node);
            if (graph.containsKey(node)) {
                for (int neighbor : graph.get(node)) {
                    if (!visited.contains(neighbor)) {
                        dfs1(neighbor, visited, finishOrder);
                    }
                }
            }
            finishOrder.add(node);
        }

        private void dfs2(int node, Set<Integer> visited, List<Integer> scc) {
            visited.add(node);
            scc.add(node);
            if (transpose.containsKey(node)) {
                for (int neighbor : transpose.get(node)) {
                    if (!visited.contains(neighbor)) {
                        dfs2(neighbor, visited, scc);
                    }
                }
            }
        }
    }

    static void testMain() {
        KosarajuSCC g = new KosarajuSCC();
        g.addEdge(0, 1);
        g.addEdge(1, 2);
        g.addEdge(2, 0);
        g.addEdge(1, 3);
        g.addEdge(3, 4);
        g.addEdge(4, 5);
        g.addEdge(5, 3);

        List<List<Integer>> sccs = g.findSCCs();
        assert sccs.size() == 2;

        // Sort SCCs for comparison
        List<List<Integer>> sorted = new ArrayList<>();
        for (List<Integer> scc : sccs) {
            List<Integer> s = new ArrayList<>(scc);
            Collections.sort(s);
            sorted.add(s);
        }
        Collections.sort(sorted, (a, b) -> Integer.compare(a.get(0), b.get(0)));

        assert sorted.get(0).equals(Arrays.asList(0, 1, 2));
        assert sorted.get(1).equals(Arrays.asList(3, 4, 5));
    }

    // Don't write tests below during competition.

    static void testSingleNode() {
        KosarajuSCC g = new KosarajuSCC();
        g.addEdge(1, 1);

        List<List<Integer>> sccs = g.findSCCs();
        assert sccs.size() == 1;
        assert sccs.get(0).contains(1);
    }

    static void testNoEdges() {
        KosarajuSCC g = new KosarajuSCC();
        g.addEdge(1, 2);
        g.addEdge(3, 4);

        List<List<Integer>> sccs = g.findSCCs();
        assert sccs.size() == 4;
    }

    static void testFullyConnected() {
        KosarajuSCC g = new KosarajuSCC();
        for (int i = 0; i < 4; i++) {
            g.addEdge(i, (i + 1) % 4);
        }

        List<List<Integer>> sccs = g.findSCCs();
        assert sccs.size() == 1;
        assert sccs.get(0).size() == 4;
    }

    static void testLinearChain() {
        KosarajuSCC g = new KosarajuSCC();
        for (int i = 0; i < 4; i++) {
            g.addEdge(i, i + 1);
        }

        List<List<Integer>> sccs = g.findSCCs();
        assert sccs.size() == 5;
    }

    static void testMultipleComponents() {
        KosarajuSCC g = new KosarajuSCC();
        g.addEdge(0, 1);
        g.addEdge(1, 2);
        g.addEdge(2, 0);
        g.addEdge(3, 4);
        g.addEdge(4, 3);
        g.addEdge(2, 3);

        List<List<Integer>> sccs = g.findSCCs();
        assert sccs.size() == 2;
    }

    static void testComplexGraph() {
        KosarajuSCC g = new KosarajuSCC();
        g.addEdge(0, 1);
        g.addEdge(1, 2);
        g.addEdge(2, 0);
        g.addEdge(3, 4);
        g.addEdge(4, 3);
        g.addEdge(5, 6);
        g.addEdge(6, 7);
        g.addEdge(7, 5);
        g.addEdge(2, 3);
        g.addEdge(4, 5);

        List<List<Integer>> sccs = g.findSCCs();
        assert sccs.size() == 3;
    }

    static void testBidirectionalEdges() {
        KosarajuSCC g = new KosarajuSCC();
        g.addEdge(1, 2);
        g.addEdge(2, 1);
        g.addEdge(2, 3);
        g.addEdge(3, 2);

        List<List<Integer>> sccs = g.findSCCs();
        assert sccs.size() == 1;
        assert sccs.get(0).size() == 3;
    }

    static void testLargeGraph() {
        KosarajuSCC g = new KosarajuSCC();
        for (int sccId = 0; sccId < 10; sccId++) {
            int base = sccId * 5;
            for (int i = 0; i < 5; i++) {
                g.addEdge(base + i, base + (i + 1) % 5);
            }
            if (sccId < 9) {
                g.addEdge(base + 4, (sccId + 1) * 5);
            }
        }

        List<List<Integer>> sccs = g.findSCCs();
        assert sccs.size() == 10;
        for (List<Integer> scc : sccs) {
            assert scc.size() == 5;
        }
    }

    public static void main(String[] args) {
        testMain();
        testSingleNode();
        testNoEdges();
        testFullyConnected();
        testLinearChain();
        testMultipleComponents();
        testComplexGraph();
        testBidirectionalEdges();
        testLargeGraph();
        System.out.println("All tests passed!");
    }
}
