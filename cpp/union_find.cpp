/*
Union-find (disjoint-set union, DSU) maintains a collection of disjoint sets under two operations:

* find(x): return the representative (root) of the set containing x.
* union(x, y): merge the sets containing x and y.

Time complexity: O(alpha(n)) per operation with path compression and union by rank,
where alpha is the inverse Ackermann function (effectively constant for practical purposes).
*/

#include <cassert>
#include <iostream>
#include <set>

class UnionFind {
  public:
    UnionFind* parent;
    int rank;

    UnionFind() : parent(this), rank(0) {}

    virtual void merge(UnionFind* other) {
        // Override with desired functionality
    }

    UnionFind* find() {
        if (parent == this) { return this; }
        parent = parent->find();
        return parent;
    }

    UnionFind* union_with(UnionFind* other) {
        UnionFind* x = this->find();
        UnionFind* y = other->find();
        if (x == y) { return x; }
        if (x->rank < y->rank) {
            x->parent = y;
            y->merge(x);
            return y;
        }
        if (x->rank > y->rank) {
            y->parent = x;
            x->merge(y);
            return x;
        }
        x->parent = y;
        y->merge(x);
        y->rank++;
        return y;
    }
};

class Test : public UnionFind {
  public:
    int size;

    Test() : UnionFind(), size(1) {}

    void merge(UnionFind* other) override {
        Test* other_test = static_cast<Test*>(other);
        this->size += other_test->size;
    }
};

void test_main() {
    Test* a = new Test();
    Test* b = new Test();
    Test* c = new Test();
    Test* d = static_cast<Test*>(a->union_with(b));
    Test* e = static_cast<Test*>(d->union_with(c));
    assert(static_cast<Test*>(e->find())->size == 3);
    assert(static_cast<Test*>(a->find())->size == 3);

    delete a;
    delete b;
    delete c;
}

// Don't write tests below during competition.

void test_single_element() {
    Test* a = new Test();
    assert(a->find() == a);
    assert(a->size == 1);
    delete a;
}

void test_union_same_set() {
    Test* a = new Test();
    Test* b = new Test();
    a->union_with(b);
    // Unioning again should be safe
    Test* root = static_cast<Test*>(a->union_with(b));
    assert(a->find() == b->find());
    assert(root->size == 2);
    delete a;
    delete b;
}

void test_multiple_unions() {
    Test* nodes[10];
    for (int i = 0; i < 10; i++) { nodes[i] = new Test(); }

    // Chain union: 0-1-2-3-4-5-6-7-8-9
    for (int i = 0; i < 9; i++) { nodes[i]->union_with(nodes[i + 1]); }

    // All should have same root
    UnionFind* root = nodes[0]->find();
    for (int i = 0; i < 10; i++) { assert(nodes[i]->find() == root); }

    assert(static_cast<Test*>(root)->size == 10);

    for (int i = 0; i < 10; i++) { delete nodes[i]; }
}

void test_union_order_independence() {
    // Test that union order doesn't affect final result
    Test* a1 = new Test();
    Test* b1 = new Test();
    Test* c1 = new Test();
    a1->union_with(b1)->union_with(c1);
    Test* root1 = static_cast<Test*>(a1->find());

    Test* a2 = new Test();
    Test* b2 = new Test();
    Test* c2 = new Test();
    c2->union_with(b2)->union_with(a2);
    Test* root2 = static_cast<Test*>(a2->find());

    assert(root1->size == 3);
    assert(root2->size == 3);

    delete a1;
    delete b1;
    delete c1;
    delete a2;
    delete b2;
    delete c2;
}

void test_disconnected_sets() {
    // Create two separate sets
    Test* a = new Test();
    Test* b = new Test();
    Test* c = new Test();
    Test* d = new Test();

    a->union_with(b);
    c->union_with(d);

    assert(a->find() == b->find());
    assert(c->find() == d->find());
    assert(a->find() != c->find());

    assert(static_cast<Test*>(a->find())->size == 2);
    assert(static_cast<Test*>(c->find())->size == 2);

    delete a;
    delete b;
    delete c;
    delete d;
}

void test_large_set() {
    // Create a large union-find structure
    Test* nodes[100];
    for (int i = 0; i < 100; i++) { nodes[i] = new Test(); }

    // Union in pairs
    for (int i = 0; i < 100; i += 2) { nodes[i]->union_with(nodes[i + 1]); }

    // Now we have 50 sets of size 2
    std::set<UnionFind*> roots;
    for (int i = 0; i < 100; i++) { roots.insert(nodes[i]->find()); }
    assert(roots.size() == 50);

    // Union all pairs together
    for (int i = 0; i < 100; i += 4) {
        if (i + 2 < 100) { nodes[i]->union_with(nodes[i + 2]); }
    }

    // Now we have 25 sets of size 4
    roots.clear();
    for (int i = 0; i < 100; i++) { roots.insert(nodes[i]->find()); }
    assert(roots.size() == 25);

    for (int i = 0; i < 100; i++) { delete nodes[i]; }
}

int main() {
    test_single_element();
    test_union_same_set();
    test_multiple_unions();
    test_union_order_independence();
    test_disconnected_sets();
    test_large_set();
    test_main();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}