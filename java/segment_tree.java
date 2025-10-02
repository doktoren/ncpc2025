/*
Segment Tree for range queries and point updates.

Supports efficient range queries (sum, min, max, etc.) and point updates on an array.

Key operations:
- update(i, value): Update element at index i - O(log n)
- query(l, r): Query range [l, r] - O(log n)

Space complexity: O(4n) = O(n)

This implementation supports sum queries but can be modified for min/max/gcd/etc.
*/

import java.util.*;
import java.util.function.BinaryOperator;

class segment_tree {
    static class SegmentTree<T> {
        private Object[] tree;
        private int n;
        private T zero;
        private BinaryOperator<T> combineOp;

        SegmentTree(T[] arr, T zero, BinaryOperator<T> combineOp) {
            this.n = arr.length;
            this.zero = zero;
            this.combineOp = combineOp;
            this.tree = new Object[4 * n];
            if (n > 0) {
                build(arr, 0, 0, n - 1);
            }
        }

        private void build(T[] arr, int node, int start, int end) {
            if (start == end) {
                tree[node] = arr[start];
            } else {
                int mid = (start + end) / 2;
                int leftChild = 2 * node + 1;
                int rightChild = 2 * node + 2;

                build(arr, leftChild, start, mid);
                build(arr, rightChild, mid + 1, end);

                tree[node] = combineOp.apply((T) tree[leftChild], (T) tree[rightChild]);
            }
        }

        void update(int idx, T value) {
            update(0, 0, n - 1, idx, value);
        }

        @SuppressWarnings("unchecked")
        private void update(int node, int start, int end, int idx, T value) {
            if (start == end) {
                tree[node] = value;
            } else {
                int mid = (start + end) / 2;
                int leftChild = 2 * node + 1;
                int rightChild = 2 * node + 2;

                if (idx <= mid) {
                    update(leftChild, start, mid, idx, value);
                } else {
                    update(rightChild, mid + 1, end, idx, value);
                }

                tree[node] = combineOp.apply((T) tree[leftChild], (T) tree[rightChild]);
            }
        }

        T query(int l, int r) {
            if (l < 0 || r >= n || l > r) {
                throw new IllegalArgumentException("Invalid range");
            }
            return query(0, 0, n - 1, l, r);
        }

        @SuppressWarnings("unchecked")
        private T query(int node, int start, int end, int l, int r) {
            if (r < start || l > end) {
                return zero;
            }

            if (l <= start && end <= r) {
                return (T) tree[node];
            }

            int mid = (start + end) / 2;
            int leftChild = 2 * node + 1;
            int rightChild = 2 * node + 2;

            T leftSum = query(leftChild, start, mid, l, r);
            T rightSum = query(rightChild, mid + 1, end, l, r);

            return combineOp.apply(leftSum, rightSum);
        }
    }

    static void testMain() {
        Long[] arr = {1L, 3L, 5L, 7L, 9L};
        SegmentTree<Long> st = new SegmentTree<>(arr, 0L, (a, b) -> a + b);
        assert st.query(1, 3) == 15L;
        st.update(2, 10L);
        assert st.query(1, 3) == 20L;
        assert st.query(0, 4) == 30L;
    }

    // Don't write tests below during competition.

    static void testSingleElement() {
        Long[] arr = {42L};
        SegmentTree<Long> st = new SegmentTree<>(arr, 0L, (a, b) -> a + b);

        assert st.query(0, 0) == 42L;

        st.update(0, 100L);
        assert st.query(0, 0) == 100L;
    }

    static void testAllElements() {
        Long[] arr = {1L, 2L, 3L, 4L, 5L};
        SegmentTree<Long> st = new SegmentTree<>(arr, 0L, (a, b) -> a + b);

        assert st.query(0, 4) == 15L;
    }

    static void testNegativeValues() {
        Long[] arr = {-5L, 3L, -2L, 8L, -1L};
        SegmentTree<Long> st = new SegmentTree<>(arr, 0L, (a, b) -> a + b);

        assert st.query(0, 4) == 3L;
        assert st.query(1, 3) == 9L;

        st.update(2, 5L);
        assert st.query(0, 4) == 10L;
    }

    static void testMultipleUpdates() {
        Long[] arr = {1L, 1L, 1L, 1L, 1L};
        SegmentTree<Long> st = new SegmentTree<>(arr, 0L, (a, b) -> a + b);

        for (int i = 0; i < 5; i++) {
            st.update(i, (long) (i + 1));
        }

        assert st.query(0, 4) == 15L;
        assert st.query(2, 4) == 12L;
    }

    static void testLargeArray() {
        Long[] arr = new Long[1000];
        for (int i = 0; i < 1000; i++) {
            arr[i] = (long) (i + 1);
        }

        SegmentTree<Long> st = new SegmentTree<>(arr, 0L, (a, b) -> a + b);

        assert st.query(0, 999) == 500500L;
        assert st.query(0, 99) == 5050L;

        st.update(500, 1000L);
        assert st.query(500, 500) == 1000L;
    }

    static void testEmpty() {
        Long[] arr = {};
        SegmentTree<Long> st = new SegmentTree<>(arr, 0L, (a, b) -> a + b);
        // Empty tree should not crash
    }

    public static void main(String[] args) {
        testSingleElement();
        testAllElements();
        testNegativeValues();
        testMultipleUpdates();
        testLargeArray();
        testEmpty();
        testMain();
        System.out.println("All tests passed!");
    }
}
