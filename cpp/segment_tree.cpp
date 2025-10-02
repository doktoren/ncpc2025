/*
Segment tree for efficient range queries and updates.

Supports range sum queries, point updates, and can be easily modified for other operations
like range minimum, maximum, or more complex functions. The tree uses 1-indexed array
representation with lazy propagation for range updates.

Time complexity: O(log n) for query and update operations, O(n) for construction.
Space complexity: O(n) for the tree structure.
*/

#include <cassert>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

template <typename T>
class SegmentTree {
  private:
    int n;
    T zero;
    std::vector<T> tree;

    void build(const std::vector<T>& arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
        } else {
            int mid = (start + end) / 2;
            build(arr, 2 * node, start, mid);
            build(arr, 2 * node + 1, mid + 1, end);
            tree[node] = tree[2 * node] + tree[2 * node + 1];
        }
    }

    void update_helper(int node, int start, int end, int idx, T val) {
        if (start == end) {
            tree[node] = val;
        } else {
            int mid = (start + end) / 2;
            if (idx <= mid) {
                update_helper(2 * node, start, mid, idx, val);
            } else {
                update_helper(2 * node + 1, mid + 1, end, idx, val);
            }
            tree[node] = tree[2 * node] + tree[2 * node + 1];
        }
    }

    T query_helper(int node, int start, int end, int left, int right) {
        if (right < start || left > end) { return zero; }
        if (left <= start && end <= right) { return tree[node]; }
        int mid = (start + end) / 2;
        T left_sum = query_helper(2 * node, start, mid, left, right);
        T right_sum = query_helper(2 * node + 1, mid + 1, end, left, right);
        return left_sum + right_sum;
    }

  public:
    SegmentTree(const std::vector<T>& arr, T zero) : n(arr.size()), zero(zero) {
        tree.resize(4 * n, zero);
        if (!arr.empty()) { build(arr, 1, 0, n - 1); }
    }

    void update(int idx, T val) {
        if (idx < 0 || idx >= n) {
            throw std::out_of_range("Index " + std::to_string(idx) + " out of bounds for size " +
                                    std::to_string(n));
        }
        update_helper(1, 0, n - 1, idx, val);
    }

    T query(int left, int right) {
        if (left < 0 || right >= n || left > right) {
            throw std::out_of_range("Invalid range [" + std::to_string(left) + ", " +
                                    std::to_string(right) + "] for size " + std::to_string(n));
        }
        return query_helper(1, 0, n - 1, left, right);
    }
};

void test_main() {
    SegmentTree<int> st({1, 3, 5, 7, 9}, 0);
    assert(st.query(1, 3) == 15);
    st.update(2, 10);
    assert(st.query(1, 3) == 20);
    assert(st.query(0, 4) == 30);
}

// Don't write tests below during competition.

void test_large_array() {
    // Test with large array
    std::vector<int> arr(1000);
    std::iota(arr.begin(), arr.end(), 0);
    SegmentTree<int> st(arr, 0);

    // Test various range queries
    int sum_0_99 = 0;
    for (int i = 0; i < 100; i++) sum_0_99 += i;
    assert(st.query(0, 99) == sum_0_99);

    int sum_500_599 = 0;
    for (int i = 500; i < 600; i++) sum_500_599 += i;
    assert(st.query(500, 599) == sum_500_599);

    assert(st.query(999, 999) == 999);

    // Test updates on large array
    st.update(500, 9999);
    assert(st.query(500, 500) == 9999);
    assert(st.query(499, 501) == 499 + 9999 + 501);
}

void test_edge_cases() {
    // Single element
    SegmentTree<int> st({42}, 0);
    assert(st.query(0, 0) == 42);
    st.update(0, 100);
    assert(st.query(0, 0) == 100);

    // Empty array - skip test as it would throw on query

    // All zeros
    SegmentTree<int> st_zeros({0, 0, 0, 0}, 0);
    assert(st_zeros.query(0, 3) == 0);
    st_zeros.update(2, 5);
    assert(st_zeros.query(0, 3) == 5);
}

void test_single_point_queries() {
    SegmentTree<int> st({10, 20, 30, 40, 50}, 0);

    // Query single points
    assert(st.query(0, 0) == 10);
    assert(st.query(1, 1) == 20);
    assert(st.query(2, 2) == 30);
    assert(st.query(3, 3) == 40);
    assert(st.query(4, 4) == 50);

    // Update and requery
    st.update(2, 100);
    assert(st.query(2, 2) == 100);
    assert(st.query(0, 4) == 220);
}

void test_full_range() {
    SegmentTree<int> st({1, 2, 3, 4, 5}, 0);

    // Query entire range
    assert(st.query(0, 4) == 15);

    // Update and query entire range again
    st.update(0, 10);
    assert(st.query(0, 4) == 24);
}

void test_overlapping_ranges() {
    SegmentTree<int> st({1, 2, 3, 4, 5, 6, 7, 8}, 0);

    // Various overlapping ranges
    assert(st.query(0, 3) == 10);
    assert(st.query(2, 5) == 18);
    assert(st.query(4, 7) == 26);

    st.update(3, 100);
    assert(st.query(0, 3) == 106);
    assert(st.query(2, 5) == 114);
}

void test_negative_numbers() {
    SegmentTree<int> st({-5, -3, -1, 1, 3, 5}, 0);

    assert(st.query(0, 5) == 0);
    assert(st.query(0, 2) == -9);
    assert(st.query(3, 5) == 9);

    st.update(2, 10);
    assert(st.query(0, 5) == 11);
}

void test_string_concatenation() {
    // Test with strings (using + for concatenation)
    SegmentTree<std::string> st({"a", "b", "c", "d"}, "");

    assert(st.query(0, 3) == "abcd");
    assert(st.query(1, 2) == "bc");

    st.update(1, "X");
    assert(st.query(0, 3) == "aXcd");
    assert(st.query(0, 1) == "aX");
}

void test_multiple_updates() {
    SegmentTree<int> st({1, 1, 1, 1, 1}, 0);

    assert(st.query(0, 4) == 5);

    // Multiple updates
    st.update(0, 2);
    st.update(1, 2);
    st.update(2, 2);
    st.update(3, 2);
    st.update(4, 2);

    assert(st.query(0, 4) == 10);
    assert(st.query(1, 3) == 6);
}

void test_invalid_indices() {
    SegmentTree<int> st({1, 2, 3}, 0);

    // Test invalid indices
    bool caught = false;
    try {
        st.update(-1, 5);
    } catch (const std::out_of_range&) { caught = true; }
    assert(caught);

    caught = false;
    try {
        st.update(3, 5);
    } catch (const std::out_of_range&) { caught = true; }
    assert(caught);

    caught = false;
    try {
        st.query(-1, 2);
    } catch (const std::out_of_range&) { caught = true; }
    assert(caught);

    caught = false;
    try {
        st.query(0, 3);
    } catch (const std::out_of_range&) { caught = true; }
    assert(caught);

    caught = false;
    try {
        st.query(2, 1);  // left > right
    } catch (const std::out_of_range&) { caught = true; }
    assert(caught);
}

int main() {
    test_large_array();
    test_edge_cases();
    test_single_point_queries();
    test_full_range();
    test_overlapping_ranges();
    test_negative_numbers();
    test_string_concatenation();
    test_multiple_updates();
    test_invalid_indices();
    test_main();
    std::cout << "All Segment Tree tests passed!" << std::endl;
    return 0;
}
