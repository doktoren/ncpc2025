/*
Priority queue implementation using a binary heap.

This module provides a generic priority queue that supports adding items with priorities,
updating priorities, removing items, and popping the item with the lowest priority.
The implementation uses C++ std::priority_queue for efficient heap operations.

Standard library alternatives:
- C++: std::priority_queue (basic operations only, no key-based updates/removal)
- Python: heapq module (min-heap only, no key-based updates/removal)
- Java: PriorityQueue class (basic operations only, no key-based updates/removal)

Time complexity: O(log n) for add/update and pop operations, O(log n) for remove.
Space complexity: O(n) where n is the number of items in the queue.
*/

#include <cassert>
#include <functional>
#include <iostream>
#include <queue>
#include <stdexcept>
#include <unordered_map>
#include <utility>

template <typename KeyT, typename PriorityT>
class PriorityQueue {
  private:
    struct Entry {
        PriorityT priority;
        KeyT key;
        size_t version;

        Entry(PriorityT p, const KeyT& k, size_t v) : priority(p), key(k), version(v) {}

        // For min-heap behavior (lowest priority first)
        bool operator>(const Entry& other) const {
            return priority > other.priority;
        }
    };

    std::priority_queue<Entry, std::vector<Entry>, std::greater<Entry>> pq;
    std::unordered_map<KeyT, size_t> key_versions;  // Maps keys to their current version
    size_t next_version;
    int size_count;

  public:
    PriorityQueue() : next_version(0), size_count(0) {}

    void set(const KeyT& key, const PriorityT& priority) {
        // Add a new task or update the priority of an existing task
        if (key_versions.find(key) != key_versions.end()) {
            // Key exists, this will invalidate the old entry
            size_count--;  // We'll increment it back below
        }

        size_count++;
        size_t version = next_version++;
        key_versions[key] = version;
        pq.push(Entry(priority, key, version));
    }

    void remove(const KeyT& key) {
        // Mark an existing task as removed by updating its version
        auto it = key_versions.find(key);
        if (it == key_versions.end()) {
            throw std::runtime_error("Key not found in priority queue");
        }
        key_versions.erase(it);
        size_count--;
    }

    std::pair<KeyT, PriorityT> pop() {
        // Remove and return the lowest priority task. Throw exception if empty.
        while (!pq.empty()) {
            Entry top = pq.top();
            pq.pop();

            // Check if this entry is still valid (not removed/updated)
            auto it = key_versions.find(top.key);
            if (it != key_versions.end() && it->second == top.version) {
                key_versions.erase(it);
                size_count--;
                return std::make_pair(top.key, top.priority);
            }
        }
        throw std::runtime_error("pop from an empty priority queue");
    }

    std::pair<KeyT, PriorityT> peek() {
        // Return the lowest priority task without removing. Returns empty result throws if empty.
        while (!pq.empty()) {
            Entry top = pq.top();

            // Check if this entry is still valid (not removed/updated)
            auto it = key_versions.find(top.key);
            if (it != key_versions.end() && it->second == top.version) {
                return std::make_pair(top.key, top.priority);
            }
            // Remove the invalid entry from the top
            pq.pop();
        }
        throw std::runtime_error("peek from an empty priority queue");
    }

    bool contains(const KeyT& key) const {
        return key_versions.find(key) != key_versions.end();
    }

    int size() const {
        return size_count;
    }

    bool empty() const {
        return size_count == 0;
    }
};

void test_main() {
    PriorityQueue<std::string, int> p;
    p.set("x", 15);
    p.set("y", 23);
    p.set("z", 8);
    auto peek_result = p.peek();
    assert(peek_result.first == "z" && peek_result.second == 8);
    auto result1 = p.pop();
    assert(result1.first == "z" && result1.second == 8);
    auto result2 = p.pop();
    assert(result2.first == "x" && result2.second == 15);
}

// Don't write tests below during competition.

void test_basic_operations() {
    PriorityQueue<std::string, int> pq;

    // Test empty queue
    assert(pq.empty());
    assert(pq.size() == 0);

    // Add items
    pq.set("task1", 10);
    pq.set("task2", 5);
    pq.set("task3", 15);

    assert(pq.size() == 3);
    auto peek_result = pq.peek();
    assert(peek_result.first == "task2" && peek_result.second == 5);

    // Pop in priority order
    auto item1 = pq.pop();
    assert(item1.first == "task2" && item1.second == 5);
    assert(pq.size() == 2);

    auto item2 = pq.pop();
    assert(item2.first == "task1" && item2.second == 10);

    auto item3 = pq.pop();
    assert(item3.first == "task3" && item3.second == 15);

    assert(pq.size() == 0);
}

void test_update_priority() {
    PriorityQueue<std::string, int> pq;

    pq.set("task1", 10);
    pq.set("task2", 5);

    // Update task1 to have higher priority
    pq.set("task1", 3);
    assert(pq.peek().first == "task1");
    assert(pq.peek().second == 3);
    assert(pq.size() == 2);

    // Pop should now give task1 first
    auto item1 = pq.pop();
    assert(item1.first == "task1" && item1.second == 3);

    auto item2 = pq.pop();
    assert(item2.first == "task2" && item2.second == 5);
}

void test_remove() {
    PriorityQueue<std::string, int> pq;

    pq.set("task1", 10);
    pq.set("task2", 5);
    pq.set("task3", 15);

    // Remove middle priority task
    pq.remove("task1");
    assert(pq.size() == 2);
    assert(!pq.contains("task1"));

    // Verify correct items remain
    auto item1 = pq.pop();
    assert(item1.first == "task2" && item1.second == 5);

    auto item2 = pq.pop();
    assert(item2.first == "task3" && item2.second == 15);
}

void test_contains() {
    PriorityQueue<std::string, int> pq;

    pq.set("task1", 10);
    pq.set("task2", 5);

    assert(pq.contains("task1"));
    assert(pq.contains("task2"));
    assert(!pq.contains("task3"));

    pq.remove("task1");
    assert(!pq.contains("task1"));
}

void test_empty_operations() {
    PriorityQueue<std::string, int> pq;

    // Test pop on empty queue
    bool caught = false;
    try {
        pq.pop();
    } catch (const std::runtime_error&) { caught = true; }
    assert(caught);

    // Test peek on empty queue
    caught = false;
    try {
        pq.peek();
    } catch (const std::runtime_error&) { caught = true; }
    assert(caught);
}

void test_remove_nonexistent() {
    PriorityQueue<std::string, int> pq;

    pq.set("task1", 10);

    bool caught = false;
    try {
        pq.remove("nonexistent");
    } catch (const std::runtime_error&) { caught = true; }
    assert(caught);
}

void test_single_element() {
    PriorityQueue<std::string, int> pq;

    pq.set("only", 42);
    assert(pq.size() == 1);
    assert(pq.peek().first == "only" && pq.peek().second == 42);
    assert(pq.pop().first == "only");
    assert(pq.size() == 0);
}

void test_duplicate_priorities() {
    PriorityQueue<std::string, int> pq;

    pq.set("task1", 10);
    pq.set("task2", 10);
    pq.set("task3", 10);

    assert(pq.size() == 3);

    // All should pop eventually
    std::vector<std::pair<std::string, int>> results;
    results.push_back(pq.pop());
    results.push_back(pq.pop());
    results.push_back(pq.pop());

    assert(results.size() == 3);
    for (const auto& [key, priority] : results) { assert(priority == 10); }
}

void test_with_floats() {
    PriorityQueue<std::string, double> pq;

    pq.set("a", 1.5);
    pq.set("b", 0.5);
    pq.set("c", 2.3);

    auto item1 = pq.pop();
    assert(item1.first == "b" && item1.second == 0.5);

    auto item2 = pq.pop();
    assert(item2.first == "a" && item2.second == 1.5);

    auto item3 = pq.pop();
    assert(item3.first == "c" && item3.second == 2.3);
}

int main() {
    test_basic_operations();
    test_update_priority();
    test_remove();
    test_contains();
    test_empty_operations();
    test_remove_nonexistent();
    test_single_element();
    test_duplicate_priorities();
    test_with_floats();
    test_main();
    std::cout << "All Priority Queue tests passed!" << std::endl;
    return 0;
}