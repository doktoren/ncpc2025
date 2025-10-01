/*
Maximum bipartite matching using augmenting path algorithm.

Given a bipartite graph with left and right vertex sets, finds the maximum
number of edges such that no two edges share a vertex.

Key operations:
- addEdge(u, v): Add edge from left vertex u to right vertex v
- maxMatching(): Compute maximum matching size

Time complexity: O(V * E)
Space complexity: O(V + E)
*/

import java.util.*;

class bipartite_match {
    static class BipartiteMatch {
        private int leftSize;
        private int rightSize;
        private Map<Integer, List<Integer>> graph;
        private Map<Integer, Integer> match;
        private Set<Integer> visited;

        BipartiteMatch(int leftSize, int rightSize) {
            this.leftSize = leftSize;
            this.rightSize = rightSize;
            this.graph = new HashMap<>();
            for (int i = 0; i < leftSize; i++) {
                graph.put(i, new ArrayList<>());
            }
        }

        void addEdge(int u, int v) {
            graph.get(u).add(v);
        }

        int maxMatching() {
            match = new HashMap<>();
            int matchingSize = 0;

            for (int u = 0; u < leftSize; u++) {
                visited = new HashSet<>();
                if (dfs(u)) {
                    matchingSize++;
                }
            }

            return matchingSize;
        }

        private boolean dfs(int u) {
            for (int v : graph.get(u)) {
                if (visited.contains(v)) {
                    continue;
                }
                visited.add(v);

                // If v is not matched or we can find augmenting path from match[v]
                if (!match.containsKey(v) || dfs(match.get(v))) {
                    match.put(v, u);
                    return true;
                }
            }
            return false;
        }

        Map<Integer, Integer> getMatching() {
            Map<Integer, Integer> result = new HashMap<>();
            for (Map.Entry<Integer, Integer> entry : match.entrySet()) {
                result.put(entry.getValue(), entry.getKey());
            }
            return result;
        }
    }

    static void testMain() {
        BipartiteMatch b = new BipartiteMatch(3, 3);
        b.addEdge(0, 0); // 1 -> X
        b.addEdge(1, 1); // 2 -> Y
        b.addEdge(2, 0); // 3 -> X
        b.addEdge(0, 2); // 1 -> Z
        b.addEdge(1, 2); // 2 -> Z
        b.addEdge(2, 1); // 3 -> Y

        int matching = b.maxMatching();
        if (matching != 3) throw new AssertionError("Expected 3, got " + matching);
        Map<Integer, Integer> matches = b.getMatching();
        if (matches.size() != 3) throw new AssertionError("Expected size 3, got " + matches.size());
    }

    // Don't write tests below during competition.

    static void testSimpleMatching() {
        BipartiteMatch bm = new BipartiteMatch(3, 3);
        bm.addEdge(0, 0);
        bm.addEdge(1, 1);
        bm.addEdge(2, 2);

        assert bm.maxMatching() == 3;
    }

    static void testNoMatching() {
        BipartiteMatch bm = new BipartiteMatch(2, 2);
        assert bm.maxMatching() == 0;
    }

    static void testPartialMatching() {
        BipartiteMatch bm = new BipartiteMatch(3, 2);
        bm.addEdge(0, 0);
        bm.addEdge(1, 0);
        bm.addEdge(2, 1);

        assert bm.maxMatching() == 2;
    }

    static void testComplexMatching() {
        BipartiteMatch bm = new BipartiteMatch(5, 5);
        bm.addEdge(0, 2);
        bm.addEdge(1, 1);
        bm.addEdge(1, 3);
        bm.addEdge(2, 0);
        bm.addEdge(2, 3);
        bm.addEdge(3, 2);
        bm.addEdge(3, 4);
        bm.addEdge(4, 4);

        int matching = bm.maxMatching();
        assert matching >= 4; // Should be at least 4
    }

    static void testSingleVertex() {
        BipartiteMatch bm = new BipartiteMatch(1, 1);
        bm.addEdge(0, 0);

        assert bm.maxMatching() == 1;
    }

    static void testMultipleEdges() {
        BipartiteMatch bm = new BipartiteMatch(2, 3);
        bm.addEdge(0, 0);
        bm.addEdge(0, 1);
        bm.addEdge(0, 2);
        bm.addEdge(1, 1);
        bm.addEdge(1, 2);

        assert bm.maxMatching() == 2;
    }

    static void testAugmentingPath() {
        BipartiteMatch bm = new BipartiteMatch(3, 3);
        bm.addEdge(0, 0);
        bm.addEdge(0, 1);
        bm.addEdge(1, 1);
        bm.addEdge(2, 2);

        int matching = bm.maxMatching();
        assert matching == 3;

        Map<Integer, Integer> matches = bm.getMatching();
        assert matches.size() == 3;
    }

    public static void main(String[] args) {
        testMain();
        testSimpleMatching();
        testNoMatching();
        testPartialMatching();
        testSingleVertex();
        testMultipleEdges();
        testAugmentingPath();
        System.out.println("All tests passed!");
    }
}
