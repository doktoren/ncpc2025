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

        UnionFind(int n) {
            parent = new int[n];
            rank = new int[n];
            for (int i = 0; i < n; i++) {
                parent[i] = i;
                rank[i] = 0;
            }
        }

        int find(int x) {
            if (parent[x] != x) {
                parent[x] = find(parent[x]); // Path compression
            }
            return parent[x];
        }

        void union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);

            if (rootX != rootY) {
                // Union by rank
                if (rank[rootX] < rank[rootY]) {
                    parent[rootX] = rootY;
                } else if (rank[rootX] > rank[rootY]) {
                    parent[rootY] = rootX;
                } else {
                    parent[rootY] = rootX;
                    rank[rootX]++;
                }
            }
        }

        boolean connected(int x, int y) {
            return find(x) == find(y);
        }
    }

    static void testMain() {
        UnionFind uf = new UnionFind(10);
        uf.union(1, 2);
        uf.union(3, 4);
        uf.union(2, 4);

        assert uf.connected(1, 3);
        assert uf.connected(1, 4);
        assert !uf.connected(1, 5);
    }

    // Don't write tests below during competition.

    static void testSingleElement() {
        UnionFind uf = new UnionFind(5);
        assert uf.connected(2, 2);
        assert !uf.connected(2, 3);
    }

    static void testChain() {
        UnionFind uf = new UnionFind(5);
        uf.union(0, 1);
        uf.union(1, 2);
        uf.union(2, 3);
        uf.union(3, 4);

        assert uf.connected(0, 4);
        assert uf.connected(1, 3);
    }

    public static void main(String[] args) {
        testSingleElement();
        testChain();
        testMain();
        System.out.println("All tests passed!");
    }
}
