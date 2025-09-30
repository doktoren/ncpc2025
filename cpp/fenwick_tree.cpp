/*
Fenwick tree (Binary Indexed Tree) for efficient range sum queries and point updates.

A Fenwick tree maintains cumulative frequency information and supports two main operations:
* update(i, delta): add delta to the element at index i
* query(i): return the sum of elements from index 0 to i (inclusive)
* range_query(left, right): return the sum of elements from left to right (inclusive)

The tree uses a clever indexing scheme based on the binary representation of indices
to achieve logarithmic time complexity for both operations.

Time complexity: O(log n) for update and query operations.
Space complexity: O(n) where n is the size of the array.
*/

#include <vector>
#include <stdexcept>
#include <cassert>
#include <iostream>

template<typename T>
class FenwickTree {
private:
    int size;
    T zero;
    std::vector<T> tree; // 1-indexed tree for easier bit manipulation

public:
    FenwickTree(int size, T zero) : size(size), zero(zero), tree(size + 1, zero) {}

    static FenwickTree from_array(const std::vector<T>& arr, T zero) {
        int n = arr.size();
        FenwickTree ft(n, zero);

        // Compute prefix sums
        std::vector<T> prefix(n + 1, zero);
        for (int i = 0; i < n; i++) {
            prefix[i + 1] = prefix[i] + arr[i];
        }

        // Build tree in O(n): each tree[i] contains sum of range [i - (i & -i) + 1, i]
        for (int i = 1; i <= n; i++) {
            int range_start = i - (i & (-i)) + 1;
            ft.tree[i] = prefix[i] - prefix[range_start - 1];
        }

        return ft;
    }

    void update(int index, T delta) {
        if (index < 0 || index >= size) {
            throw std::out_of_range("Index out of bounds");
        }

        // Convert to 1-indexed
        index++;
        while (index <= size) {
            tree[index] = tree[index] + delta;
            // Move to next index by adding the lowest set bit
            index += index & (-index);
        }
    }

    T query(int index) {
        if (index < 0 || index >= size) {
            throw std::out_of_range("Index out of bounds");
        }

        // Convert to 1-indexed
        index++;
        T result = zero;
        while (index > 0) {
            result = result + tree[index];
            // Move to parent by removing the lowest set bit
            index -= index & (-index);
        }
        return result;
    }

    T range_query(int left, int right) {
        if (left > right) {
            return zero;
        }
        if (left == 0) {
            return query(right);
        }
        return query(right) - query(left - 1);
    }

    T get_value(int index) {
        if (index == 0) {
            return query(0);
        }
        return query(index) - query(index - 1);
    }

    int length() const {
        return size;
    }
};

void test_main() {
    FenwickTree<int> f(5, 0);
    f.update(0, 7);
    f.update(2, 13);
    f.update(4, 19);
    assert(f.query(4) == 39);
    assert(f.range_query(1, 3) == 13);
    assert(f.get_value(2) == 13);
}

// Don't write tests below during competition.

void test_basic() {
    // Test with integers
    FenwickTree<int> ft(5, 0);

    // Initial array: [0, 0, 0, 0, 0]
    assert(ft.query(0) == 0);
    assert(ft.query(4) == 0);
    assert(ft.range_query(1, 3) == 0);

    // Update operations
    ft.update(0, 5);  // [5, 0, 0, 0, 0]
    ft.update(2, 3);  // [5, 0, 3, 0, 0]
    ft.update(4, 7);  // [5, 0, 3, 0, 7]

    // Query operations
    assert(ft.query(0) == 5);
    assert(ft.query(2) == 8);  // 5 + 0 + 3
    assert(ft.query(4) == 15); // 5 + 0 + 3 + 0 + 7

    // Range queries
    assert(ft.range_query(0, 2) == 8);
    assert(ft.range_query(2, 4) == 10);
    assert(ft.range_query(1, 3) == 3);

    // Get individual values
    assert(ft.get_value(0) == 5);
    assert(ft.get_value(2) == 3);
    assert(ft.get_value(4) == 7);
}

void test_from_array() {
    std::vector<int> arr = {1, 3, 5, 7, 9, 11};
    auto ft = FenwickTree<int>::from_array(arr, 0);

    // Test that prefix sums match
    int expected_sum = 0;
    for (int i = 0; i < arr.size(); i++) {
        expected_sum += arr[i];
        assert(ft.query(i) == expected_sum);
    }

    // Test range queries
    assert(ft.range_query(1, 3) == 3 + 5 + 7); // 15
    assert(ft.range_query(2, 4) == 5 + 7 + 9); // 21

    // Test updates
    ft.update(2, 10); // arr[2] becomes 15
    assert(ft.get_value(2) == 15);
    assert(ft.range_query(1, 3) == 3 + 15 + 7); // 25
}

void test_edge_cases() {
    FenwickTree<int> ft(1, 0);

    // Single element tree
    ft.update(0, 42);
    assert(ft.query(0) == 42);
    assert(ft.range_query(0, 0) == 42);
    assert(ft.get_value(0) == 42);

    // Empty range
    FenwickTree<int> ft_large(10, 0);
    assert(ft_large.range_query(5, 3) == 0); // left > right
}

void test_negative_values() {
    FenwickTree<int> ft(4, 0);

    // Mix of positive and negative updates
    ft.update(0, 10);
    ft.update(1, -5);
    ft.update(2, 8);
    ft.update(3, -3);

    assert(ft.query(3) == 10); // 10 + (-5) + 8 + (-3)
    assert(ft.range_query(1, 2) == 3); // (-5) + 8

    // Update with negative delta
    ft.update(0, -5); // Subtract 5 from position 0
    assert(ft.get_value(0) == 5);
    assert(ft.query(3) == 5); // 5 + (-5) + 8 + (-3)
}

int main() {
    test_basic();
    test_from_array();
    test_edge_cases();
    test_negative_values();
    test_main();
    std::cout << "All Fenwick tree tests passed!" << std::endl;
    return 0;
}