/*
2-SAT solver using Kosaraju's SCC algorithm on implication graph.

2-SAT (Boolean Satisfiability with 2 literals per clause) determines if a Boolean formula
in CNF with at most 2 literals per clause is satisfiable. Uses implication graph where
each variable x has nodes x and not-x, and clause (a OR b) creates edges not-a -> b
and not-b -> a.

Key operations:
- addClause(a, aNeg, b, bNeg): Add clause (a OR b)
- solve(): Returns assignment array if satisfiable, null otherwise

Time complexity: O(n + m) where n is variables and m is clauses
Space complexity: O(n + m)
*/

import java.util.*;

class two_sat {
    static class TwoSAT {
        private int n;
        private List<List<Integer>> graph;
        private List<List<Integer>> transpose;

        TwoSAT(int n) {
            this.n = n;
            this.graph = new ArrayList<>();
            this.transpose = new ArrayList<>();
            for (int i = 0; i < 2 * n; i++) {
                graph.add(new ArrayList<>());
                transpose.add(new ArrayList<>());
            }
        }

        void addClause(int a, boolean aNeg, int b, boolean bNeg) {
            int aNode = 2 * a + (aNeg ? 1 : 0);
            int bNode = 2 * b + (bNeg ? 1 : 0);
            int naNode = 2 * a + (aNeg ? 0 : 1);
            int nbNode = 2 * b + (bNeg ? 0 : 1);

            graph.get(naNode).add(bNode);
            graph.get(nbNode).add(aNode);
            transpose.get(bNode).add(naNode);
            transpose.get(aNode).add(nbNode);
        }

        boolean[] solve() {
            // Kosaraju's algorithm
            boolean[] visited = new boolean[2 * n];
            List<Integer> finishOrder = new ArrayList<>();

            for (int node = 0; node < 2 * n; node++) {
                if (!visited[node]) {
                    dfs1(node, visited, finishOrder);
                }
            }

            Arrays.fill(visited, false);
            int[] sccId = new int[2 * n];
            int currentScc = 0;

            for (int i = finishOrder.size() - 1; i >= 0; i--) {
                int node = finishOrder.get(i);
                if (!visited[node]) {
                    dfs2(node, visited, sccId, currentScc);
                    currentScc++;
                }
            }

            // Check satisfiability
            for (int i = 0; i < n; i++) {
                if (sccId[2 * i] == sccId[2 * i + 1]) {
                    return null;
                }
            }

            // Construct assignment
            boolean[] assignment = new boolean[n];
            for (int i = 0; i < n; i++) {
                assignment[i] = sccId[2 * i] > sccId[2 * i + 1];
            }

            return assignment;
        }

        private void dfs1(int node, boolean[] visited, List<Integer> finishOrder) {
            visited[node] = true;
            for (int neighbor : graph.get(node)) {
                if (!visited[neighbor]) {
                    dfs1(neighbor, visited, finishOrder);
                }
            }
            finishOrder.add(node);
        }

        private void dfs2(int node, boolean[] visited, int[] sccId, int scc) {
            visited[node] = true;
            sccId[node] = scc;
            for (int neighbor : transpose.get(node)) {
                if (!visited[neighbor]) {
                    dfs2(neighbor, visited, sccId, scc);
                }
            }
        }
    }

    static void testMain() {
        TwoSAT sat = new TwoSAT(2);
        sat.addClause(0, false, 1, false);
        sat.addClause(0, true, 1, false);
        sat.addClause(0, false, 1, true);

        boolean[] result = sat.solve();
        assert result != null;
        assert result[0] || result[1];
        assert !result[0] || result[1];
        assert result[0] || !result[1];
    }

    // Don't write tests below during competition.

    static void testUnsatisfiable() {
        TwoSAT sat = new TwoSAT(2);
        sat.addClause(0, false, 1, false);
        sat.addClause(0, false, 1, true);
        sat.addClause(0, true, 1, false);
        sat.addClause(0, true, 1, true);

        boolean[] result = sat.solve();
        assert result == null;
    }

    static void testSingleVariable() {
        TwoSAT sat = new TwoSAT(1);
        sat.addClause(0, false, 0, false);

        boolean[] result = sat.solve();
        assert result != null;
        assert result[0];
    }

    static void testImplicationChain() {
        TwoSAT sat = new TwoSAT(4);
        sat.addClause(0, true, 1, false);
        sat.addClause(1, true, 2, false);
        sat.addClause(2, true, 3, false);

        boolean[] result = sat.solve();
        assert result != null;
        if (result[0]) assert result[1];
        if (result[1]) assert result[2];
        if (result[2]) assert result[3];
    }

    static void testMutualImplication() {
        TwoSAT sat = new TwoSAT(2);
        sat.addClause(0, true, 1, false);
        sat.addClause(1, true, 0, false);

        boolean[] result = sat.solve();
        assert result != null;
        assert result[0] == result[1];
    }

    static void testLargeSatisfiable() {
        TwoSAT sat = new TwoSAT(10);
        for (int i = 0; i < 9; i++) {
            sat.addClause(i, false, i + 1, false);
        }

        boolean[] result = sat.solve();
        assert result != null;
        for (int i = 0; i < 9; i++) {
            assert result[i] || result[i + 1];
        }
    }

    static void testContradictoryImplications() {
        TwoSAT sat = new TwoSAT(2);
        sat.addClause(0, true, 1, false);
        sat.addClause(0, true, 1, true);

        boolean[] result = sat.solve();
        assert result != null;
        assert !result[0];
    }

    static void testComplexSystem() {
        TwoSAT sat = new TwoSAT(5);
        sat.addClause(0, false, 1, false);
        sat.addClause(1, true, 2, false);
        sat.addClause(2, true, 3, true);
        sat.addClause(3, false, 4, false);
        sat.addClause(4, true, 0, true);

        boolean[] result = sat.solve();
        assert result != null;
        assert result[0] || result[1];
        assert !result[1] || result[2];
        assert !result[2] || !result[3];
        assert result[3] || result[4];
        assert !result[4] || !result[0];
    }

    static void testXorConstraint() {
        TwoSAT sat = new TwoSAT(2);
        sat.addClause(0, false, 1, false);
        sat.addClause(0, true, 1, true);

        boolean[] result = sat.solve();
        assert result != null;
        assert (result[0] && !result[1]) || (!result[0] && result[1]);
    }

    public static void main(String[] args) {
        testMain();
        testUnsatisfiable();
        testSingleVariable();
        testImplicationChain();
        testMutualImplication();
        testLargeSatisfiable();
        testContradictoryImplications();
        testComplexSystem();
        testXorConstraint();
        System.out.println("All tests passed!");
    }
}
