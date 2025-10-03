/*
Skip list is a probabilistic data structure that maintains a sorted collection of elements.

It uses multiple levels of linked lists to achieve O(log n) average time complexity for
search, insertion, and deletion operations. Elements are inserted with randomly determined
heights, creating express lanes for faster traversal.

Standard library alternatives:
- C++: std::set / std::map (red-black tree, O(log n) guaranteed)
- Python: No built-in sorted set (use bisect module for sorted lists)
- Java: TreeSet / TreeMap (red-black tree, O(log n) guaranteed)

Time complexity: O(log n) average for search, insert, and delete operations.
Space complexity: O(n) on average, where n is the number of elements.
*/

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

class SkipListNode<T extends Comparable<T>> {
    T value;
    List<SkipListNode<T>> forward;

    SkipListNode(T value, int level) {
        this.value = value;
        this.forward = new ArrayList<>(level + 1);
        for (int i = 0; i <= level; i++) {
            this.forward.add(null);
        }
    }
}

class SkipList<T extends Comparable<T>> {
    private int maxLevel;
    private double p;
    private int level;
    private SkipListNode<T> header;
    Random random;

    SkipList(int maxLevel, double p) {
        this.maxLevel = maxLevel;
        this.p = p;
        this.level = 0;
        this.header = new SkipListNode<>(null, maxLevel);
        this.random = new Random();
    }

    SkipList() {
        this(16, 0.5);
    }

    private int randomLevel() {
        int lvl = 0;
        while (random.nextDouble() < p && lvl < maxLevel) {
            lvl++;
        }
        return lvl;
    }

    SkipList<T> insert(T value) {
        List<SkipListNode<T>> update = new ArrayList<>(maxLevel + 1);
        for (int i = 0; i <= maxLevel; i++) {
            update.add(null);
        }

        SkipListNode<T> current = header;

        for (int i = level; i >= 0; i--) {
            while (current.forward.get(i) != null
                    && current.forward.get(i).value.compareTo(value) < 0) {
                current = current.forward.get(i);
            }
            update.set(i, current);
        }

        int lvl = randomLevel();
        if (lvl > level) {
            for (int i = level + 1; i <= lvl; i++) {
                update.set(i, header);
            }
            level = lvl;
        }

        SkipListNode<T> newNode = new SkipListNode<>(value, lvl);
        for (int i = 0; i <= lvl; i++) {
            newNode.forward.set(i, update.get(i).forward.get(i));
            update.get(i).forward.set(i, newNode);
        }

        return this;
    }

    boolean search(T value) {
        SkipListNode<T> current = header;
        for (int i = level; i >= 0; i--) {
            while (current.forward.get(i) != null
                    && current.forward.get(i).value.compareTo(value) < 0) {
                current = current.forward.get(i);
            }
        }
        current = current.forward.get(0);
        return current != null && current.value.compareTo(value) == 0;
    }

    boolean delete(T value) {
        List<SkipListNode<T>> update = new ArrayList<>(maxLevel + 1);
        for (int i = 0; i <= maxLevel; i++) {
            update.add(null);
        }

        SkipListNode<T> current = header;

        for (int i = level; i >= 0; i--) {
            while (current.forward.get(i) != null
                    && current.forward.get(i).value.compareTo(value) < 0) {
                current = current.forward.get(i);
            }
            update.set(i, current);
        }

        current = current.forward.get(0);
        if (current == null || current.value.compareTo(value) != 0) {
            return false;
        }

        for (int i = 0; i <= level; i++) {
            if (update.get(i).forward.get(i) != current) {
                break;
            }
            update.get(i).forward.set(i, current.forward.get(i));
        }

        while (level > 0 && header.forward.get(level) == null) {
            level--;
        }

        return true;
    }

    // Optional functionality (not always needed during competition)

    int size() {
        int count = 0;
        SkipListNode<T> current = header.forward.get(0);
        while (current != null) {
            count++;
            current = current.forward.get(0);
        }
        return count;
    }

    List<T> toList() {
        List<T> result = new ArrayList<>();
        SkipListNode<T> current = header.forward.get(0);
        while (current != null) {
            result.add(current.value);
            current = current.forward.get(0);
        }
        return result;
    }

    boolean contains(T value) {
        return search(value);
    }
}

public class skiplist {
    static void testMain() {
        SkipList<Integer> sl = new SkipList<>();
        sl.random = new Random(42);
        sl.insert(10).insert(20).insert(5).insert(15);
        assert sl.search(10);
        assert sl.search(20);
        assert !sl.search(25);
        assert sl.delete(10);
        assert !sl.search(10);
        assert !sl.delete(30);

        // Optional functionality (not always needed during competition)
        SkipList<Integer> sl2 = new SkipList<>();
        sl2.random = new Random(42);
        sl2.insert(3).insert(1).insert(4).insert(1).insert(5);
        assert sl2.size() == 5;
        List<Integer> expected = List.of(1, 1, 3, 4, 5);
        assert sl2.toList().equals(expected);
        assert sl2.contains(3);
        assert !sl2.contains(7);
    }

    // Don't write tests below during competition.

    static void testBasicOperations() {
        SkipList<Integer> sl = new SkipList<>();
        sl.random = new Random(123);
        assert !sl.search(1);
        sl.insert(5);
        assert sl.search(5);
        assert !sl.search(4);
    }

    static void testMultipleInserts() {
        SkipList<Integer> sl = new SkipList<>();
        sl.random = new Random(456);
        int[] values = {10, 5, 15, 3, 7, 12, 20};
        for (int v : values) {
            sl.insert(v);
        }
        for (int v : values) {
            assert sl.search(v);
        }
        assert !sl.search(1);
        assert !sl.search(100);
    }

    static void testDeleteOperations() {
        SkipList<Integer> sl = new SkipList<>();
        sl.random = new Random(789);
        sl.insert(10).insert(20).insert(30);
        assert sl.delete(20);
        assert !sl.search(20);
        assert sl.search(10);
        assert sl.search(30);
        assert !sl.delete(20);
        assert !sl.delete(40);
    }

    static void testDuplicateValues() {
        SkipList<Integer> sl = new SkipList<>();
        sl.random = new Random(101);
        sl.insert(5).insert(5).insert(5);
        assert sl.size() == 3;
        List<Integer> expected = List.of(5, 5, 5);
        assert sl.toList().equals(expected);
    }

    static void testOrderedInsertion() {
        SkipList<Integer> sl = new SkipList<>();
        sl.random = new Random(202);
        for (int i = 1; i <= 10; i++) {
            sl.insert(i);
        }
        List<Integer> expected = new ArrayList<>();
        for (int i = 1; i <= 10; i++) {
            expected.add(i);
        }
        assert sl.toList().equals(expected);
    }

    static void testReverseInsertion() {
        SkipList<Integer> sl = new SkipList<>();
        sl.random = new Random(303);
        for (int i = 10; i >= 1; i--) {
            sl.insert(i);
        }
        List<Integer> expected = new ArrayList<>();
        for (int i = 1; i <= 10; i++) {
            expected.add(i);
        }
        assert sl.toList().equals(expected);
    }

    static void testEmptySkiplist() {
        SkipList<Integer> sl = new SkipList<>();
        sl.random = new Random(404);
        assert sl.size() == 0;
        assert sl.toList().isEmpty();
        assert !sl.delete(5);
    }

    static void testStrings() {
        SkipList<String> sl = new SkipList<>();
        sl.random = new Random(505);
        sl.insert("dog").insert("cat").insert("bird").insert("ant");
        assert sl.search("cat");
        List<String> expected = List.of("ant", "bird", "cat", "dog");
        assert sl.toList().equals(expected);
    }

    public static void main(String[] args) {
        testBasicOperations();
        testMultipleInserts();
        testDeleteOperations();
        testDuplicateValues();
        testOrderedInsertion();
        testReverseInsertion();
        testEmptySkiplist();
        testStrings();
        testMain();
    }
}
