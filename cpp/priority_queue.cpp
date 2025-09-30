/*
Priority queue implementation using a binary heap.

This module provides a generic priority queue that supports adding items with priorities,
updating priorities, removing items, and popping the item with the lowest priority.
The implementation uses C++ std::priority_queue for efficient heap operations.

Time complexity: O(log n) for add/update and pop operations, O(log n) for remove.
Space complexity: O(n) where n is the number of items in the queue.
*/

#include <queue>
#include <unordered_map>
#include <functional>
#include <cassert>
#include <iostream>
#include <stdexcept>
#include <utility>

template<typename KeyT, typename PriorityT>
class PriorityQueue {
private:
    struct Entry {
        PriorityT priority;
        KeyT key;
        size_t version;

        Entry(PriorityT p, KeyT k, size_t v) : priority(p), key(k), version(v) {}

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
            size_count--; // We'll increment it back below
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
    auto result1 = p.pop();
    assert(result1.first == "z" && result1.second == 8);
    auto result2 = p.pop();
    assert(result2.first == "x" && result2.second == 15);
}

// Don't write tests below during competition.

void test_basic() {
    PriorityQueue<std::string, int> pq;

    // Test empty queue
    assert(pq.empty());
    assert(pq.size() == 0);

    // Add some items
    pq.set("task1", 10);
    pq.set("task2", 5);
    pq.set("task3", 15);

    assert(pq.size() == 3);
    assert(!pq.empty());

    // Pop in priority order
    auto item1 = pq.pop();
    assert(item1.first == "task2" && item1.second == 5);

    auto item2 = pq.pop();
    assert(item2.first == "task1" && item2.second == 10);

    auto item3 = pq.pop();
    assert(item3.first == "task3" && item3.second == 15);

    assert(pq.empty());
}

void test_update_priority() {
    PriorityQueue<std::string, int> pq;

    pq.set("task1", 10);
    pq.set("task2", 20);

    // Update priority of task1 to be higher than task2
    pq.set("task1", 25);

    assert(pq.size() == 2);

    // task2 should come first now
    auto item1 = pq.pop();
    assert(item1.first == "task2" && item1.second == 20);

    auto item2 = pq.pop();
    assert(item2.first == "task1" && item2.second == 25);
}

void test_remove() {
    PriorityQueue<std::string, int> pq;

    pq.set("task1", 10);
    pq.set("task2", 5);
    pq.set("task3", 15);

    assert(pq.size() == 3);

    // Remove middle priority item
    pq.remove("task1");
    assert(pq.size() == 2);

    // Should get task2 first, then task3
    auto item1 = pq.pop();
    assert(item1.first == "task2" && item1.second == 5);

    auto item2 = pq.pop();
    assert(item2.first == "task3" && item2.second == 15);

    assert(pq.empty());
}

void test_edge_cases() {
    PriorityQueue<int, double> pq;

    // Test with numeric keys and floating point priorities
    pq.set(1, 3.14);
    pq.set(2, 2.71);
    pq.set(3, 1.41);

    auto item1 = pq.pop();
    assert(item1.first == 3 && item1.second == 1.41);

    auto item2 = pq.pop();
    assert(item2.first == 2 && item2.second == 2.71);

    auto item3 = pq.pop();
    assert(item3.first == 1 && item3.second == 3.14);
}

int main() {
    test_basic();
    test_update_priority();
    test_remove();
    test_edge_cases();
    test_main();
    std::cout << "All Priority Queue tests passed!" << std::endl;
    return 0;
}