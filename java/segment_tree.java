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

class segment_tree {
    static class SegmentTree {
        private long[] tree;
        private int n;

        SegmentTree(long[] arr) {
            this.n = arr.length;
            this.tree = new long[4 * n];
            if (n > 0) {
                build(arr, 0, 0, n - 1);
            }
        }

        private void build(long[] arr, int node, int start, int end) {
            if (start == end) {
                tree[node] = arr[start];
            } else {
                int mid = (start + end) / 2;
                int leftChild = 2 * node + 1;
                int rightChild = 2 * node + 2;

                build(arr, leftChild, start, mid);
                build(arr, rightChild, mid + 1, end);

                tree[node] = tree[leftChild] + tree[rightChild];
            }
        }

        void update(int idx, long value) {
            update(0, 0, n - 1, idx, value);
        }

        private void update(int node, int start, int end, int idx, long value) {
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

                tree[node] = tree[leftChild] + tree[rightChild];
            }
        }

        long query(int l, int r) {
            if (l < 0 || r >= n || l > r) {
                throw new IllegalArgumentException("Invalid range");
            }
            return query(0, 0, n - 1, l, r);
        }

        private long query(int node, int start, int end, int l, int r) {
            if (r < start || l > end) {
                return 0;
            }

            if (l <= start && end <= r) {
                return tree[node];
            }

            int mid = (start + end) / 2;
            int leftChild = 2 * node + 1;
            int rightChild = 2 * node + 2;

            long leftSum = query(leftChild, start, mid, l, r);
            long rightSum = query(rightChild, mid + 1, end, l, r);

            return leftSum + rightSum;
        }
    }

    static void testMain() {
        long[] arr = {1, 3, 5, 7, 9, 11};
        SegmentTree st = new SegmentTree(arr);

        assert st.query(0, 2) == 9;
        assert st.query(1, 4) == 24;

        st.update(2, 6);
        assert st.query(0, 2) == 10;
        assert st.query(1, 4) == 25;
    }

    // Don't write tests below during competition.

    static void testSingleElement() {
        long[] arr = {42};
        SegmentTree st = new SegmentTree(arr);

        assert st.query(0, 0) == 42;

        st.update(0, 100);
        assert st.query(0, 0) == 100;
    }

    static void testAllElements() {
        long[] arr = {1, 2, 3, 4, 5};
        SegmentTree st = new SegmentTree(arr);

        assert st.query(0, 4) == 15;
    }

    static void testNegativeValues() {
        long[] arr = {-5, 3, -2, 8, -1};
        SegmentTree st = new SegmentTree(arr);

        assert st.query(0, 4) == 3;
        assert st.query(1, 3) == 9;

        st.update(2, 5);
        assert st.query(0, 4) == 10;
    }

    static void testMultipleUpdates() {
        long[] arr = {1, 1, 1, 1, 1};
        SegmentTree st = new SegmentTree(arr);

        for (int i = 0; i < 5; i++) {
            st.update(i, i + 1);
        }

        assert st.query(0, 4) == 15;
        assert st.query(2, 4) == 12;
    }

    static void testLargeArray() {
        long[] arr = new long[1000];
        for (int i = 0; i < 1000; i++) {
            arr[i] = i + 1;
        }

        SegmentTree st = new SegmentTree(arr);

        assert st.query(0, 999) == 500500;
        assert st.query(0, 99) == 5050;

        st.update(500, 1000);
        assert st.query(500, 500) == 1000;
    }

    static void testEmpty() {
        long[] arr = {};
        SegmentTree st = new SegmentTree(arr);
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
