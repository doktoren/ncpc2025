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

        // O(n log n) constructor from array
        FenwickTree(long[] values) {
            this.size = values.length;
            this.tree = new long[size + 1];
            for (int i = 0; i < values.length; i++) {
                update(i, values[i]);
            }
        }

        // O(n) constructor from array using prefix sums
        static FenwickTree fromArray(long[] arr) {
            int n = arr.length;
            FenwickTree ft = new FenwickTree(n);

            // Compute prefix sums
            long[] prefix = new long[n + 1];
            for (int i = 0; i < n; i++) {
                prefix[i + 1] = prefix[i] + arr[i];
            }

            // Build tree in O(n): each tree[i] contains sum of range [i - (i & -i) + 1, i]
            for (int i = 1; i <= n; i++) {
                int rangeStart = i - (i & (-i)) + 1;
                ft.tree[i] = prefix[i] - prefix[rangeStart - 1];
            }

            return ft;
        }

        void update(int i, long delta) {
            if (i < 0 || i >= size) {
                throw new IndexOutOfBoundsException("Index " + i + " out of bounds for size " + size);
            }
            i++; // Convert to 1-based indexing
            while (i <= size) {
                tree[i] += delta;
                i += i & (-i);
            }
        }

        long query(int i) {
            if (i < 0 || i >= size) {
                throw new IndexOutOfBoundsException("Index " + i + " out of bounds for size " + size);
            }
            i++; // Convert to 1-based indexing
            long sum = 0;
            while (i > 0) {
                sum += tree[i];
                i -= i & (-i);
            }
            return sum;
        }

        long rangeQuery(int l, int r) {
            if (l > r) {
                return 0; // Returns 0 if left > right
            }
            if (l < 0 || r >= size) {
                throw new IndexOutOfBoundsException("Range [" + l + ", " + r + "] out of bounds for size " + size);
            }
            if (l == 0) {
                return query(r);
            }
            return query(r) - query(l - 1);
        }

        long getValue(int i) {
            if (i < 0 || i >= size) {
                throw new IndexOutOfBoundsException("Index " + i + " out of bounds for size " + size);
            }
            if (i == 0) {
                return query(0);
            }
            return query(i) - query(i - 1);
        }

        // Find smallest index >= startIndex with value > 0
        // REQUIRES: all updates are non-negative
        Integer firstNonzeroIndex(int startIndex) {
            startIndex = Math.max(startIndex, 0);
            if (startIndex >= size) {
                return null;
            }

            long prefixBefore = startIndex > 0 ? query(startIndex - 1) : 0;
            long total = query(size - 1);
            if (total == prefixBefore) {
                return null;
            }

            // Fenwick lower_bound: first idx with prefix_sum(idx) > prefixBefore
            int idx = 0; // 1-based cursor
            long cur = 0; // running prefix at 'idx'
            int bit = Integer.highestOneBit(size);

            while (bit > 0) {
                int nxt = idx + bit;
                if (nxt <= size) {
                    long cand = cur + tree[nxt];
                    if (cand <= prefixBefore) { // move right while prefix <= target
                        cur = cand;
                        idx = nxt;
                    }
                }
                bit >>= 1;
            }

            // idx is the largest position with prefix <= prefixBefore (1-based).
            // The answer is idx (converted to 0-based).
            return idx;
        }
    }

    static void testMain() {
        FenwickTree f = new FenwickTree(5);
        f.update(0, 7);
        f.update(2, 13);
        f.update(4, 19);
        assert f.query(4) == 39;
        assert f.rangeQuery(1, 3) == 13;
        assert f.getValue(2) == 13;
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

    static void testBoundsChecking() {
        FenwickTree ft = new FenwickTree(5);

        // Test update bounds
        try {
            ft.update(-1, 10);
            assert false : "Should throw IndexOutOfBoundsException for negative index";
        } catch (IndexOutOfBoundsException e) {
            // Expected
        }

        try {
            ft.update(5, 10);
            assert false : "Should throw IndexOutOfBoundsException for index >= size";
        } catch (IndexOutOfBoundsException e) {
            // Expected
        }

        // Test query bounds
        try {
            ft.query(-1);
            assert false : "Should throw IndexOutOfBoundsException for negative index";
        } catch (IndexOutOfBoundsException e) {
            // Expected
        }

        try {
            ft.query(5);
            assert false : "Should throw IndexOutOfBoundsException for index >= size";
        } catch (IndexOutOfBoundsException e) {
            // Expected
        }

        // Test range_query bounds
        try {
            ft.rangeQuery(-1, 2);
            assert false : "Should throw IndexOutOfBoundsException for negative left";
        } catch (IndexOutOfBoundsException e) {
            // Expected
        }

        try {
            ft.rangeQuery(0, 5);
            assert false : "Should throw IndexOutOfBoundsException for right >= size";
        } catch (IndexOutOfBoundsException e) {
            // Expected
        }

        // Empty range should return 0
        assert ft.rangeQuery(5, 3) == 0;
    }

    static void testGetValue() {
        FenwickTree ft = new FenwickTree(5);
        ft.update(0, 5);
        ft.update(2, 3);
        ft.update(4, 7);

        assert ft.getValue(0) == 5;
        assert ft.getValue(2) == 3;
        assert ft.getValue(4) == 7;
    }

    static void testFirstNonzeroIndex() {
        FenwickTree ft = new FenwickTree(10);
        ft.update(2, 1);
        ft.update(8, 1);

        assert ft.firstNonzeroIndex(5) == 8;
        assert ft.firstNonzeroIndex(8) == 8;
        assert ft.firstNonzeroIndex(0) == 2;
        assert ft.firstNonzeroIndex(9) == null;
    }

    static void testFirstNonzeroBounds() {
        FenwickTree ft = new FenwickTree(10);
        ft.update(5, 1);

        // Negative start_index should be clamped to 0
        assert ft.firstNonzeroIndex(-5) == 5;

        // Start from exactly where nonzero is
        assert ft.firstNonzeroIndex(5) == 5;

        // Start past all nonzero elements
        assert ft.firstNonzeroIndex(10) == null;
        assert ft.firstNonzeroIndex(100) == null;

        // Empty tree
        FenwickTree ftEmpty = new FenwickTree(10);
        assert ftEmpty.firstNonzeroIndex(0) == null;
    }

    static void testFromArrayMethod() {
        long[] arr = {1, 3, 5, 7, 9, 11};
        FenwickTree ft = FenwickTree.fromArray(arr);

        // Test that prefix sums match
        long expectedSum = 0;
        for (int i = 0; i < arr.length; i++) {
            expectedSum += arr[i];
            assert ft.query(i) == expectedSum;
        }

        // Test range queries
        assert ft.rangeQuery(1, 3) == 3 + 5 + 7; // 15
        assert ft.rangeQuery(2, 4) == 5 + 7 + 9; // 21

        // Test updates
        ft.update(2, 10);  // arr[2] becomes 15
        assert ft.getValue(2) == 15;
        assert ft.rangeQuery(1, 3) == 3 + 15 + 7; // 25
    }

    static void testEdgeCases() {
        FenwickTree ft = new FenwickTree(1);

        // Single element tree
        ft.update(0, 42);
        assert ft.query(0) == 42;
        assert ft.rangeQuery(0, 0) == 42;
        assert ft.getValue(0) == 42;

        // Empty range
        FenwickTree ftLarge = new FenwickTree(10);
        assert ftLarge.rangeQuery(5, 3) == 0;  // left > right
    }

    public static void main(String[] args) {
        testEmpty();
        testSingleUpdate();
        testFromArray();
        testNegativeValues();
        testLargeUpdates();
        testBoundsChecking();
        testGetValue();
        testFirstNonzeroIndex();
        testFirstNonzeroBounds();
        testFromArrayMethod();
        testEdgeCases();
        testMain();
        System.out.println("All tests passed!");
    }
}
