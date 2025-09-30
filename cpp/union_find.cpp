/*
Union-find (disjoint-set union, DSU) maintains a collection of disjoint sets under two operations:

* find(x): return the representative (root) of the set containing x.
* union(x, y): merge the sets containing x and y.

Time complexity: O(alpha(n)) per operation with path compression and union by rank,
where alpha is the inverse Ackermann function (effectively constant for practical purposes).
*/

#include <cassert>
#include <iostream>

class UnionFind {
public:
    UnionFind* parent;
    int rank;

    UnionFind() : parent(this), rank(0) {}

    virtual void merge(UnionFind* other) {
        // Override with desired functionality
    }

    UnionFind* find() {
        if (parent == this) {
            return this;
        }
        parent = parent->find();
        return parent;
    }

    UnionFind* union_with(UnionFind* other) {
        UnionFind* x = this->find();
        UnionFind* y = other->find();
        if (x == y) {
            return x;
        }
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

void test_basic() {
    Test* nodes[5];
    for (int i = 0; i < 5; i++) {
        nodes[i] = new Test();
    }

    // Initially all separate
    for (int i = 0; i < 5; i++) {
        assert(static_cast<Test*>(nodes[i]->find())->size == 1);
    }

    // Union 0 and 1
    Test* root01 = static_cast<Test*>(nodes[0]->union_with(nodes[1]));
    assert(static_cast<Test*>(nodes[0]->find())->size == 2);
    assert(static_cast<Test*>(nodes[1]->find())->size == 2);
    assert(nodes[0]->find() == nodes[1]->find());

    // Union 2 and 3
    Test* root23 = static_cast<Test*>(nodes[2]->union_with(nodes[3]));
    assert(static_cast<Test*>(nodes[2]->find())->size == 2);
    assert(static_cast<Test*>(nodes[3]->find())->size == 2);
    assert(nodes[2]->find() == nodes[3]->find());

    // Union the two groups
    Test* final_root = static_cast<Test*>(root01->union_with(root23));
    assert(static_cast<Test*>(final_root->find())->size == 4);

    // All should point to same root
    UnionFind* common_root = nodes[0]->find();
    for (int i = 1; i < 4; i++) {
        assert(nodes[i]->find() == common_root);
    }

    // Node 4 still separate
    assert(static_cast<Test*>(nodes[4]->find())->size == 1);
    assert(nodes[4]->find() != common_root);

    for (int i = 0; i < 5; i++) {
        delete nodes[i];
    }
}

int main() {
    test_basic();
    test_main();
    std::cout << "All Union-Find tests passed!" << std::endl;
    return 0;
}