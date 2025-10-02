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

import java.util.function.BinaryOperator;

class fenwick_tree {
    interface Summable<T> {
        T add(T other);
        T subtract(T other);
    }

    static class FenwickTree<T> {
        private Object[] tree;
        private int size;
        private T zero;
        private BinaryOperator<T> addOp;
        private BinaryOperator<T> subtractOp;

        FenwickTree(int n, T zero, BinaryOperator<T> addOp, BinaryOperator<T> subtractOp) {
            this.size = n;
            this.zero = zero;
            this.addOp = addOp;
            this.subtractOp = subtractOp;
            this.tree = new Object[n + 1];
            for (int i = 0; i <= n; i++) {
                tree[i] = zero;
            }
        }

        // O(n log n) constructor from array
        FenwickTree(T[] values, T zero, BinaryOperator<T> addOp, BinaryOperator<T> subtractOp) {
            this(values.length, zero, addOp, subtractOp);
            for (int i = 0; i < values.length; i++) {
                update(i, values[i]);
            }
        }

        // O(n) constructor from array using prefix sums
        static <T> FenwickTree<T> fromArray(T[] arr, T zero, BinaryOperator<T> addOp, BinaryOperator<T> subtractOp) {
            int n = arr.length;
            FenwickTree<T> ft = new FenwickTree<>(n, zero, addOp, subtractOp);

            // Compute prefix sums
            Object[] prefix = new Object[n + 1];
            prefix[0] = zero;
            for (int i = 0; i < n; i++) {
                prefix[i + 1] = addOp.apply((T)prefix[i], arr[i]);
            }

            // Build tree in O(n): each tree[i] contains sum of range [i - (i & -i) + 1, i]
            for (int i = 1; i <= n; i++) {
                int rangeStart = i - (i & (-i)) + 1;
                ft.tree[i] = subtractOp.apply((T)prefix[i], (T)prefix[rangeStart - 1]);
            }

            return ft;
        }

        @SuppressWarnings("unchecked")
        void update(int i, T delta) {
            if (i < 0 || i >= size) {
                throw new IndexOutOfBoundsException("Index " + i + " out of bounds for size " + size);
            }
            i++; // Convert to 1-based indexing
            while (i <= size) {
                tree[i] = addOp.apply((T)tree[i], delta);
                i += i & (-i);
            }
        }

        @SuppressWarnings("unchecked")
        T query(int i) {
            if (i < 0 || i >= size) {
                throw new IndexOutOfBoundsException("Index " + i + " out of bounds for size " + size);
            }
            i++; // Convert to 1-based indexing
            T sum = zero;
            while (i > 0) {
                sum = addOp.apply(sum, (T)tree[i]);
                i -= i & (-i);
            }
            return sum;
        }

        T rangeQuery(int l, int r) {
            if (l > r || l < 0 || r >= size) {
                return zero;
            }
            if (l == 0) {
                return query(r);
            }
            return subtractOp.apply(query(r), query(l - 1));
        }

        // Optional functionality (not always needed during competition)

        T getValue(int i) {
            if (i < 0 || i >= size) {
                throw new IndexOutOfBoundsException("Index " + i + " out of bounds for size " + size);
            }
            if (i == 0) {
                return query(0);
            }
            return subtractOp.apply(query(i), query(i - 1));
        }

        // Find smallest index >= startIndex with value > zero
        // REQUIRES: all updates are non-negative, T must be comparable
        @SuppressWarnings("unchecked")
        Integer firstNonzeroIndex(int startIndex, java.util.Comparator<T> comparator) {
            startIndex = Math.max(startIndex, 0);
            if (startIndex >= size) {
                return null;
            }

            T prefixBefore = startIndex > 0 ? query(startIndex - 1) : zero;
            T total = query(size - 1);
            if (comparator.compare(total, prefixBefore) == 0) {
                return null;
            }

            // Fenwick lower_bound: first idx with prefix_sum(idx) > prefixBefore
            int idx = 0; // 1-based cursor
            T cur = zero; // running prefix at 'idx'
            int bit = Integer.highestOneBit(size);

            while (bit > 0) {
                int nxt = idx + bit;
                if (nxt <= size) {
                    T cand = addOp.apply(cur, (T)tree[nxt]);
                    if (comparator.compare(cand, prefixBefore) <= 0) { // move right while prefix <= target
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
        FenwickTree<Long> f = new FenwickTree<>(5, 0L, (a, b) -> a + b, (a, b) -> a - b);
        f.update(0, 7L);
        f.update(2, 13L);
        f.update(4, 19L);
        assert f.query(4) == 39L;
        assert f.rangeQuery(1, 3) == 13L;

        // Optional functionality (not always needed during competition)

        assert f.getValue(2) == 13L;
        FenwickTree<Long> g = FenwickTree.fromArray(new Long[]{1L, 2L, 3L, 4L, 5L}, 0L, (a, b) -> a + b, (a, b) -> a - b);
        assert g.query(4) == 15L;
    }

    // Don't write tests below during competition.

    static void testEmpty() {
        FenwickTree<Long> ft = new FenwickTree<>(10, 0L, (a, b) -> a + b, (a, b) -> a - b);
        assert ft.query(0) == 0L;
        assert ft.query(9) == 0L;
        assert ft.rangeQuery(0, 9) == 0L;
    }

    static void testSingleUpdate() {
        FenwickTree<Long> ft = new FenwickTree<>(5, 0L, (a, b) -> a + b, (a, b) -> a - b);
        ft.update(2, 7L);
        assert ft.query(1) == 0L;
        assert ft.query(2) == 7L;
        assert ft.query(4) == 7L;
    }

    static void testFromArray() {
        Long[] arr = {1L, 2L, 3L, 4L, 5L};
        FenwickTree<Long> ft = new FenwickTree<>(arr, 0L, (a, b) -> a + b, (a, b) -> a - b);
        assert ft.query(0) == 1L;
        assert ft.query(2) == 6L;
        assert ft.query(4) == 15L;
        assert ft.rangeQuery(1, 3) == 9L;
    }

    static void testNegativeValues() {
        FenwickTree<Long> ft = new FenwickTree<>(4, 0L, (a, b) -> a + b, (a, b) -> a - b);
        ft.update(0, 10L);
        ft.update(1, -5L);
        ft.update(2, 3L);
        ft.update(3, -2L);

        assert ft.query(1) == 5L;
        assert ft.query(3) == 6L;
        assert ft.rangeQuery(1, 2) == -2L;
    }

    static void testLargeUpdates() {
        FenwickTree<Long> ft = new FenwickTree<>(1000, 0L, (a, b) -> a + b, (a, b) -> a - b);
        for (int i = 0; i < 1000; i++) {
            ft.update(i, (long)(i + 1));
        }
        assert ft.query(999) == 500500L;
        assert ft.rangeQuery(0, 99) == 5050L;
    }

    static void testBoundsChecking() {
        FenwickTree<Long> ft = new FenwickTree<>(5, 0L, (a, b) -> a + b, (a, b) -> a - b);

        // Test update bounds
        try {
            ft.update(-1, 10L);
            assert false : "Should throw IndexOutOfBoundsException for negative index";
        } catch (IndexOutOfBoundsException e) {
            // Expected
        }

        try {
            ft.update(5, 10L);
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

        // Test range_query bounds - should return 0 for invalid ranges
        assert ft.rangeQuery(-1, 2) == 0L;
        assert ft.rangeQuery(0, 5) == 0L;
        assert ft.rangeQuery(5, 3) == 0L;
    }

    static void testGetValue() {
        FenwickTree<Long> ft = new FenwickTree<>(5, 0L, (a, b) -> a + b, (a, b) -> a - b);
        ft.update(0, 5L);
        ft.update(2, 3L);
        ft.update(4, 7L);

        assert ft.getValue(0) == 5L;
        assert ft.getValue(2) == 3L;
        assert ft.getValue(4) == 7L;
    }

    static void testFirstNonzeroIndex() {
        FenwickTree<Long> ft = new FenwickTree<>(10, 0L, (a, b) -> a + b, (a, b) -> a - b);
        ft.update(2, 1L);
        ft.update(8, 1L);

        java.util.Comparator<Long> cmp = Long::compare;
        assert ft.firstNonzeroIndex(5, cmp) == 8;
        assert ft.firstNonzeroIndex(8, cmp) == 8;
        assert ft.firstNonzeroIndex(0, cmp) == 2;
        assert ft.firstNonzeroIndex(9, cmp) == null;
    }

    static void testFirstNonzeroBounds() {
        FenwickTree<Long> ft = new FenwickTree<>(10, 0L, (a, b) -> a + b, (a, b) -> a - b);
        ft.update(5, 1L);

        java.util.Comparator<Long> cmp = Long::compare;
        // Negative start_index should be clamped to 0
        assert ft.firstNonzeroIndex(-5, cmp) == 5;

        // Start from exactly where nonzero is
        assert ft.firstNonzeroIndex(5, cmp) == 5;

        // Start past all nonzero elements
        assert ft.firstNonzeroIndex(10, cmp) == null;
        assert ft.firstNonzeroIndex(100, cmp) == null;

        // Empty tree
        FenwickTree<Long> ftEmpty = new FenwickTree<>(10, 0L, (a, b) -> a + b, (a, b) -> a - b);
        assert ftEmpty.firstNonzeroIndex(0, cmp) == null;
    }

    static void testFromArrayMethod() {
        Long[] arr = {1L, 3L, 5L, 7L, 9L, 11L};
        FenwickTree<Long> ft = FenwickTree.fromArray(arr, 0L, (a, b) -> a + b, (a, b) -> a - b);

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
        ft.update(2, 10L);  // arr[2] becomes 15
        assert ft.getValue(2) == 15L;
        assert ft.rangeQuery(1, 3) == 3 + 15 + 7; // 25
    }

    static void testEdgeCases() {
        FenwickTree<Long> ft = new FenwickTree<>(1, 0L, (a, b) -> a + b, (a, b) -> a - b);

        // Single element tree
        ft.update(0, 42L);
        assert ft.query(0) == 42L;
        assert ft.rangeQuery(0, 0) == 42L;
        assert ft.getValue(0) == 42L;

        // Empty range
        FenwickTree<Long> ftLarge = new FenwickTree<>(10, 0L, (a, b) -> a + b, (a, b) -> a - b);
        assert ftLarge.rangeQuery(5, 3) == 0L;  // left > right
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
