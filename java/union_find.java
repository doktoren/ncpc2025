/*
Union-Find (Disjoint Set Union) data structure with path compression and union by rank.

Supports:
- find(x): Find the representative of the set containing x - O(α(n)) amortized
- union(x, y): Merge the sets containing x and y - O(α(n)) amortized
- connected(x, y): Check if x and y are in the same set - O(α(n)) amortized

Space complexity: O(n)

α(n) is the inverse Ackermann function, which is effectively constant for all practical values of n.
*/

class union_find {
    static class UnionFind {
        private int[] parent;
        private int[] rank;
        private int[] size;

        UnionFind(int n) {
            parent = new int[n];
            rank = new int[n];
            size = new int[n];
            for (int i = 0; i < n; i++) {
                parent[i] = i;
                rank[i] = 0;
                size[i] = 1;
            }
        }

        int find(int x) {
            if (parent[x] != x) {
                parent[x] = find(parent[x]); // Path compression
            }
            return parent[x];
        }

        int union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);

            if (rootX == rootY) {
                return rootX;
            }

            // Union by rank
            if (rank[rootX] < rank[rootY]) {
                parent[rootX] = rootY;
                size[rootY] += size[rootX];
                return rootY;
            } else if (rank[rootX] > rank[rootY]) {
                parent[rootY] = rootX;
                size[rootX] += size[rootY];
                return rootX;
            } else {
                parent[rootY] = rootX;
                size[rootX] += size[rootY];
                rank[rootX]++;
                return rootX;
            }
        }

        boolean connected(int x, int y) {
            return find(x) == find(y);
        }

        int getSize(int x) {
            return size[find(x)];
        }
    }

    static void testMain() {
        UnionFind a = new UnionFind(3);
        int d = a.union(0, 1);
        int e = a.union(d, 2);
        assert a.getSize(e) == 3;
        assert a.getSize(a.find(0)) == 3;
    }

    // Don't write tests below during competition.

    static void testSingleElement() {
        UnionFind uf = new UnionFind(1);
        assert uf.find(0) == 0;
        assert uf.getSize(0) == 1;
    }

    static void testUnionSameSet() {
        UnionFind uf = new UnionFind(2);
        uf.union(0, 1);
        // Unioning again should be safe
        int root = uf.union(0, 1);
        assert uf.find(0) == uf.find(1);
        assert uf.getSize(root) == 2;
    }

    static void testMultipleUnions() {
        UnionFind uf = new UnionFind(10);
        // Chain union: 0-1-2-3-4-5-6-7-8-9
        for (int i = 0; i < 9; i++) {
            uf.union(i, i + 1);
        }

        // All should have same root
        int root = uf.find(0);
        for (int i = 0; i < 10; i++) {
            assert uf.find(i) == root;
        }

        assert uf.getSize(root) == 10;
    }

    static void testUnionOrderIndependence() {
        // Test that union order doesn't affect final result
        UnionFind uf1 = new UnionFind(3);
        uf1.union(0, 1);
        uf1.union(1, 2);
        int root1 = uf1.find(0);

        UnionFind uf2 = new UnionFind(3);
        uf2.union(2, 1);
        uf2.union(1, 0);
        int root2 = uf2.find(0);

        assert uf1.getSize(root1) == uf2.getSize(root2);
        assert uf1.getSize(root1) == 3;
    }

    static void testDisconnectedSets() {
        UnionFind uf = new UnionFind(4);

        uf.union(0, 1);
        uf.union(2, 3);

        assert uf.connected(0, 1);
        assert uf.connected(2, 3);
        assert !uf.connected(0, 2);

        assert uf.getSize(uf.find(0)) == 2;
        assert uf.getSize(uf.find(2)) == 2;
    }

    static void testLargeSet() {
        UnionFind uf = new UnionFind(100);

        // Union in pairs
        for (int i = 0; i < 100; i += 2) {
            uf.union(i, i + 1);
        }

        // Now we have 50 sets of size 2
        int uniqueRoots = 0;
        boolean[] seenRoots = new boolean[100];
        for (int i = 0; i < 100; i++) {
            int root = uf.find(i);
            if (!seenRoots[root]) {
                seenRoots[root] = true;
                uniqueRoots++;
            }
        }
        assert uniqueRoots == 50;

        // Union all pairs together
        for (int i = 0; i < 100; i += 4) {
            if (i + 2 < 100) {
                uf.union(i, i + 2);
            }
        }

        // Now we have 25 sets of size 4
        uniqueRoots = 0;
        seenRoots = new boolean[100];
        for (int i = 0; i < 100; i++) {
            int root = uf.find(i);
            if (!seenRoots[root]) {
                seenRoots[root] = true;
                uniqueRoots++;
            }
        }
        assert uniqueRoots == 25;
    }

    public static void main(String[] args) {
        testSingleElement();
        testUnionSameSet();
        testMultipleUnions();
        testUnionOrderIndependence();
        testDisconnectedSets();
        testLargeSet();
        testMain();
        System.out.println("All tests passed!");
    }
}
