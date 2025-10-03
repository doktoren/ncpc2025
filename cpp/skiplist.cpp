#include <cassert>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <string>
#include <vector>

template <typename T>
class SkipListNode {
  public:
    T value;
    std::vector<SkipListNode*> forward;

    SkipListNode(T val, int level) : value(val), forward(level + 1, nullptr) {}
};

template <typename T>
class SkipList {
  private:
    int max_level;
    float p;
    int level;
    SkipListNode<T>* header;

    int random_level() {
        int lvl = 0;
        while ((float)rand() / RAND_MAX < p && lvl < max_level) { lvl++; }
        return lvl;
    }

  public:
    SkipList(int max_lvl = 16, float prob = 0.5) : max_level(max_lvl), p(prob), level(0) {
        header = new SkipListNode<T>(T(), max_level);
    }

    ~SkipList() {
        SkipListNode<T>* current = header;
        while (current != nullptr) {
            SkipListNode<T>* next = current->forward[0];
            delete current;
            current = next;
        }
    }

    // Delete copy and move operations (not needed for competition)
    SkipList(const SkipList&) = delete;
    SkipList& operator=(const SkipList&) = delete;
    SkipList(SkipList&&) = delete;
    SkipList& operator=(SkipList&&) = delete;

    SkipList& insert(const T& value) {
        std::vector<SkipListNode<T>*> update(max_level + 1);
        SkipListNode<T>* current = header;

        for (int i = level; i >= 0; i--) {
            while (current->forward[i] != nullptr && current->forward[i]->value < value) {
                current = current->forward[i];
            }
            update[i] = current;
        }

        int lvl = random_level();
        if (lvl > level) {
            for (int i = level + 1; i <= lvl; i++) { update[i] = header; }
            level = lvl;
        }

        SkipListNode<T>* new_node = new SkipListNode<T>(value, lvl);
        for (int i = 0; i <= lvl; i++) {
            new_node->forward[i] = update[i]->forward[i];
            update[i]->forward[i] = new_node;
        }

        return *this;
    }

    bool search(const T& value) {
        SkipListNode<T>* current = header;
        for (int i = level; i >= 0; i--) {
            while (current->forward[i] != nullptr && current->forward[i]->value < value) {
                current = current->forward[i];
            }
        }
        current = current->forward[0];
        return current != nullptr && current->value == value;
    }

    bool remove(const T& value) {
        std::vector<SkipListNode<T>*> update(max_level + 1);
        SkipListNode<T>* current = header;

        for (int i = level; i >= 0; i--) {
            while (current->forward[i] != nullptr && current->forward[i]->value < value) {
                current = current->forward[i];
            }
            update[i] = current;
        }

        current = current->forward[0];
        if (current == nullptr || current->value != value) { return false; }

        for (int i = 0; i <= level; i++) {
            if (update[i]->forward[i] != current) { break; }
            update[i]->forward[i] = current->forward[i];
        }

        delete current;

        while (level > 0 && header->forward[level] == nullptr) { level--; }

        return true;
    }

    // Optional functionality (not always needed during competition)

    int size() const {
        int count = 0;
        SkipListNode<T>* current = header->forward[0];
        while (current != nullptr) {
            count++;
            current = current->forward[0];
        }
        return count;
    }

    std::vector<T> to_vector() const {
        std::vector<T> result;
        SkipListNode<T>* current = header->forward[0];
        while (current != nullptr) {
            result.push_back(current->value);
            current = current->forward[0];
        }
        return result;
    }

    bool contains(const T& value) {
        return search(value);
    }
};

void test_main() {
    srand(42);
    SkipList<int> sl;
    sl.insert(10).insert(20).insert(5).insert(15);
    assert(sl.search(10));
    assert(sl.search(20));
    assert(!sl.search(25));
    assert(sl.remove(10));
    assert(!sl.search(10));
    assert(!sl.remove(30));

    // Optional functionality (not always needed during competition)
    srand(42);
    SkipList<int> sl2;
    sl2.insert(3).insert(1).insert(4).insert(1).insert(5);
    assert(sl2.size() == 5);
    std::vector<int> expected = {1, 1, 3, 4, 5};
    assert(sl2.to_vector() == expected);
    assert(sl2.contains(3));
    assert(!sl2.contains(7));
}

// Don't write tests below during competition.

void test_basic_operations() {
    srand(123);
    SkipList<int> sl;
    assert(!sl.search(1));
    sl.insert(5);
    assert(sl.search(5));
    assert(!sl.search(4));
}

void test_multiple_inserts() {
    srand(456);
    SkipList<int> sl;
    std::vector<int> values = {10, 5, 15, 3, 7, 12, 20};
    for (int v : values) { sl.insert(v); }
    for (int v : values) { assert(sl.search(v)); }
    assert(!sl.search(1));
    assert(!sl.search(100));
}

void test_delete_operations() {
    srand(789);
    SkipList<int> sl;
    sl.insert(10).insert(20).insert(30);
    assert(sl.remove(20));
    assert(!sl.search(20));
    assert(sl.search(10));
    assert(sl.search(30));
    assert(!sl.remove(20));
    assert(!sl.remove(40));
}

void test_duplicate_values() {
    srand(101);
    SkipList<int> sl;
    sl.insert(5).insert(5).insert(5);
    assert(sl.size() == 3);
    std::vector<int> expected = {5, 5, 5};
    assert(sl.to_vector() == expected);
}

void test_ordered_insertion() {
    srand(202);
    SkipList<int> sl;
    for (int i = 1; i <= 10; i++) { sl.insert(i); }
    std::vector<int> expected;
    for (int i = 1; i <= 10; i++) { expected.push_back(i); }
    assert(sl.to_vector() == expected);
}

void test_reverse_insertion() {
    srand(303);
    SkipList<int> sl;
    for (int i = 10; i >= 1; i--) { sl.insert(i); }
    std::vector<int> expected;
    for (int i = 1; i <= 10; i++) { expected.push_back(i); }
    assert(sl.to_vector() == expected);
}

void test_empty_skiplist() {
    srand(404);
    SkipList<int> sl;
    assert(sl.size() == 0);
    assert(sl.to_vector().empty());
    assert(!sl.remove(5));
}

void test_strings() {
    srand(505);
    SkipList<std::string> sl;
    sl.insert("dog").insert("cat").insert("bird").insert("ant");
    assert(sl.search("cat"));
    std::vector<std::string> expected = {"ant", "bird", "cat", "dog"};
    assert(sl.to_vector() == expected);
}

int main() {
    test_basic_operations();
    test_multiple_inserts();
    test_delete_operations();
    test_duplicate_values();
    test_ordered_insertion();
    test_reverse_insertion();
    test_empty_skiplist();
    test_strings();
    test_main();
    return 0;
}
