/*
Fenwick Tree (Binary Indexed Tree) implementation.

A data structure for efficient prefix sum queries and point updates on an array.

Key operations:
- update(i, delta): Add delta to element at index i - O(log n)
- query(i): Get sum of elements from index 0 to i (inclusive) - O(log n)
- range_query(l, r): Get sum from index l to r (inclusive) - O(log n)

Space complexity: O(n)

Note: Uses 1-based indexing internally for simpler bit manipulation.
*/

class fenwick_tree {
    static class FenwickTree {
        private long[] tree;
        private int size;

        FenwickTree(int n) {
            this.size = n;
            this.tree = new long[n + 1];
        }

        FenwickTree(long[] values) {
            this.size = values.length;
            this.tree = new long[size + 1];
            for (int i = 0; i < values.length; i++) {
                update(i, values[i]);
            }
        }

        void update(int i, long delta) {
            i++; // Convert to 1-based indexing
            while (i <= size) {
                tree[i] += delta;
                i += i & (-i);
            }
        }

        long query(int i) {
            i++; // Convert to 1-based indexing
            long sum = 0;
            while (i > 0) {
                sum += tree[i];
                i -= i & (-i);
            }
            return sum;
        }

        long rangeQuery(int l, int r) {
            if (l > 0) {
                return query(r) - query(l - 1);
            }
            return query(r);
        }
    }

    static void testMain() {
        FenwickTree ft = new FenwickTree(5);
        ft.update(0, 3);
        ft.update(1, 2);
        ft.update(2, 5);
        ft.update(3, 1);
        ft.update(4, 4);

        assert ft.query(2) == 10;
        assert ft.rangeQuery(1, 3) == 8;

        ft.update(2, 3);
        assert ft.query(2) == 13;
    }

    // Don't write tests below during competition.

    static void testEmpty() {
        FenwickTree ft = new FenwickTree(10);
        assert ft.query(0) == 0;
        assert ft.query(9) == 0;
        assert ft.rangeQuery(0, 9) == 0;
    }

    static void testSingleUpdate() {
        FenwickTree ft = new FenwickTree(5);
        ft.update(2, 7);
        assert ft.query(1) == 0;
        assert ft.query(2) == 7;
        assert ft.query(4) == 7;
    }

    static void testFromArray() {
        long[] arr = {1, 2, 3, 4, 5};
        FenwickTree ft = new FenwickTree(arr);
        assert ft.query(0) == 1;
        assert ft.query(2) == 6;
        assert ft.query(4) == 15;
        assert ft.rangeQuery(1, 3) == 9;
    }

    static void testNegativeValues() {
        FenwickTree ft = new FenwickTree(4);
        ft.update(0, 10);
        ft.update(1, -5);
        ft.update(2, 3);
        ft.update(3, -2);

        assert ft.query(1) == 5;
        assert ft.query(3) == 6;
        assert ft.rangeQuery(1, 2) == -2;
    }

    static void testLargeUpdates() {
        FenwickTree ft = new FenwickTree(1000);
        for (int i = 0; i < 1000; i++) {
            ft.update(i, i + 1);
        }
        assert ft.query(999) == 500500;
        assert ft.rangeQuery(0, 99) == 5050;
    }

    public static void main(String[] args) {
        testEmpty();
        testSingleUpdate();
        testFromArray();
        testNegativeValues();
        testLargeUpdates();
        testMain();
        System.out.println("All tests passed!");
    }
}
