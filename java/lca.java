/*
Lowest Common Ancestor (LCA) using Binary Lifting.

Preprocesses a tree to answer LCA queries efficiently.

Key operations:
- addEdge(u, v): Add undirected edge to tree
- build(root): Preprocess tree with given root - O(n log n)
- query(u, v): Find LCA of nodes u and v - O(log n)
- distance(u, v): Find distance between two nodes - O(log n)

Space complexity: O(n log n)

Binary lifting allows us to "jump" up the tree in powers of 2, enabling
efficient LCA queries.
*/

import java.util.*;

class lca {
    static class LCA {
        private int n;
        private int maxLog;
        private Map<Integer, List<Integer>> graph;
        private int[] depth;
        private Map<Integer, Map<Integer, Integer>> up;

        LCA(int n) {
            this.n = n;
            this.maxLog = (int) Math.ceil(Math.log(n) / Math.log(2)) + 1;
            this.graph = new HashMap<>();
            this.depth = new int[n];
            this.up = new HashMap<>();

            for (int i = 0; i < n; i++) {
                graph.put(i, new ArrayList<>());
                up.put(i, new HashMap<>());
            }
        }

        void addEdge(int u, int v) {
            graph.get(u).add(v);
            graph.get(v).add(u);
        }

        void build(int root) {
            Arrays.fill(depth, 0);
            dfs(root, -1, 0);
        }

        private void dfs(int node, int parent, int d) {
            depth[node] = d;

            if (parent != -1) {
                up.get(node).put(0, parent);
            }

            for (int i = 1; i < maxLog; i++) {
                if (up.get(node).containsKey(i - 1)) {
                    int ancestor = up.get(node).get(i - 1);
                    if (up.get(ancestor).containsKey(i - 1)) {
                        up.get(node).put(i, up.get(ancestor).get(i - 1));
                    }
                }
            }

            for (int child : graph.get(node)) {
                if (child != parent) {
                    dfs(child, node, d + 1);
                }
            }
        }

        int query(int u, int v) {
            if (depth[u] < depth[v]) {
                int temp = u;
                u = v;
                v = temp;
            }

            // Bring u to the same level as v
            int diff = depth[u] - depth[v];
            for (int i = 0; i < maxLog; i++) {
                if (((diff >> i) & 1) == 1) {
                    if (up.get(u).containsKey(i)) {
                        u = up.get(u).get(i);
                    }
                }
            }

            if (u == v) {
                return u;
            }

            // Binary search for LCA
            for (int i = maxLog - 1; i >= 0; i--) {
                if (up.get(u).containsKey(i) && up.get(v).containsKey(i)) {
                    int uAncestor = up.get(u).get(i);
                    int vAncestor = up.get(v).get(i);
                    if (uAncestor != vAncestor) {
                        u = uAncestor;
                        v = vAncestor;
                    }
                }
            }

            return up.get(u).getOrDefault(0, u);
        }

        int distance(int u, int v) {
            int lcaNode = query(u, v);
            return depth[u] + depth[v] - 2 * depth[lcaNode];
        }
    }

    static void testMain() {
        LCA lca = new LCA(7);
        lca.addEdge(0, 1);
        lca.addEdge(0, 2);
        lca.addEdge(1, 3);
        lca.addEdge(1, 4);
        lca.addEdge(2, 5);
        lca.addEdge(2, 6);

        lca.build(0);

        assert lca.query(3, 4) == 1;
        assert lca.query(3, 5) == 0;
        assert lca.query(5, 6) == 2;

        assert lca.distance(3, 4) == 2;
        assert lca.distance(3, 5) == 4;
    }

    // Don't write tests below during competition.

    static void testLinearTree() {
        LCA lca = new LCA(5);
        lca.addEdge(0, 1);
        lca.addEdge(1, 2);
        lca.addEdge(2, 3);
        lca.addEdge(3, 4);

        lca.build(0);

        assert lca.query(0, 4) == 0;
        assert lca.query(2, 4) == 2;
        assert lca.distance(0, 4) == 4;
    }

    static void testSameNode() {
        LCA lca = new LCA(3);
        lca.addEdge(0, 1);
        lca.addEdge(0, 2);

        lca.build(0);

        assert lca.query(1, 1) == 1;
        assert lca.distance(1, 1) == 0;
    }

    static void testDeepTree() {
        int n = 100;
        LCA lca = new LCA(n);
        for (int i = 0; i < n - 1; i++) {
            lca.addEdge(i, i + 1);
        }

        lca.build(0);

        assert lca.query(50, 99) == 50;
        assert lca.distance(0, 99) == 99;
    }

    static void testComplexTree() {
        LCA lca = new LCA(10);
        lca.addEdge(0, 1);
        lca.addEdge(0, 2);
        lca.addEdge(1, 3);
        lca.addEdge(1, 4);
        lca.addEdge(2, 5);
        lca.addEdge(3, 6);
        lca.addEdge(3, 7);
        lca.addEdge(4, 8);
        lca.addEdge(5, 9);

        lca.build(0);

        assert lca.query(6, 7) == 3;
        assert lca.query(6, 8) == 1;
        assert lca.query(7, 9) == 0;
        assert lca.distance(6, 7) == 2;
        assert lca.distance(6, 9) == 6;
    }

    static void testBinaryTree() {
        LCA lca = new LCA(7);
        lca.addEdge(0, 1);
        lca.addEdge(0, 2);
        lca.addEdge(1, 3);
        lca.addEdge(1, 4);
        lca.addEdge(2, 5);
        lca.addEdge(2, 6);

        lca.build(0);

        assert lca.query(3, 6) == 0;
        assert lca.query(4, 5) == 0;
        assert lca.distance(3, 6) == 4;
    }

    public static void main(String[] args) {
        testLinearTree();
        testSameNode();
        testDeepTree();
        testComplexTree();
        testBinaryTree();
        testMain();
        System.out.println("All tests passed!");
    }
}
