/*
Generic priority queue (min-heap) with update and remove operations.

Supports:
- push(item): Add item to heap - O(log n)
- pop(): Remove and return minimum item - O(log n)
- peek(): View minimum item without removing - O(1)
- update(old_item, new_item): Update item in heap - O(n)
- remove(item): Remove specific item - O(n)

Standard library alternatives:
- C++: std::priority_queue (basic operations only, no key-based updates/removal)
- Python: heapq module (min-heap only, no key-based updates/removal)
- Java: PriorityQueue class (basic operations only, no key-based updates/removal)

Space complexity: O(n)
*/

import java.util.*;

class priority_queue {
    static class PriorityQueue<T extends Comparable<T>> {
        private List<T> heap;

        PriorityQueue() {
            this.heap = new ArrayList<>();
        }

        void push(T item) {
            heap.add(item);
            siftUp(heap.size() - 1);
        }

        T pop() {
            if (heap.isEmpty()) {
                throw new IllegalStateException("Heap is empty");
            }
            T item = heap.get(0);
            T last = heap.remove(heap.size() - 1);
            if (!heap.isEmpty()) {
                heap.set(0, last);
                siftDown(0);
            }
            return item;
        }

        T peek() {
            if (heap.isEmpty()) {
                return null;
            }
            return heap.get(0);
        }

        boolean contains(T item) {
            return heap.contains(item);
        }

        void update(T oldItem, T newItem) {
            int idx = heap.indexOf(oldItem);
            if (idx == -1) {
                throw new IllegalArgumentException("Item not in heap");
            }
            heap.set(idx, newItem);
            if (newItem.compareTo(oldItem) < 0) {
                siftUp(idx);
            } else {
                siftDown(idx);
            }
        }

        void remove(T item) {
            int idx = heap.indexOf(item);
            if (idx == -1) {
                throw new IllegalArgumentException("Item not in heap");
            }
            T last = heap.remove(heap.size() - 1);
            if (idx < heap.size()) {
                T oldItem = heap.get(idx);
                heap.set(idx, last);
                if (last.compareTo(oldItem) < 0) {
                    siftUp(idx);
                } else {
                    siftDown(idx);
                }
            }
        }

        int size() {
            return heap.size();
        }

        boolean isEmpty() {
            return heap.isEmpty();
        }

        private void siftUp(int idx) {
            while (idx > 0) {
                int parent = (idx - 1) / 2;
                if (heap.get(idx).compareTo(heap.get(parent)) >= 0) {
                    break;
                }
                Collections.swap(heap, idx, parent);
                idx = parent;
            }
        }

        private void siftDown(int idx) {
            while (true) {
                int smallest = idx;
                int left = 2 * idx + 1;
                int right = 2 * idx + 2;

                if (left < heap.size() && heap.get(left).compareTo(heap.get(smallest)) < 0) {
                    smallest = left;
                }
                if (right < heap.size() && heap.get(right).compareTo(heap.get(smallest)) < 0) {
                    smallest = right;
                }
                if (smallest == idx) {
                    break;
                }
                Collections.swap(heap, idx, smallest);
                idx = smallest;
            }
        }
    }

    static void testMain() {
        PriorityQueue<Integer> p = new PriorityQueue<>();
        p.push(15);
        p.push(23);
        p.push(8);
        assert p.peek() == 8;
        assert p.pop() == 8;
        assert p.pop() == 15;
    }

    // Don't write tests below during competition.

    static void testBasicOperations() {
        PriorityQueue<Integer> pq = new PriorityQueue<>();

        // Test empty queue
        assert pq.size() == 0;
        assert pq.peek() == null;

        // Add items
        pq.push(10);
        pq.push(5);
        pq.push(15);

        assert pq.size() == 3;
        assert pq.peek() == 5;

        // Pop in priority order
        assert pq.pop() == 5;
        assert pq.size() == 2;
        assert pq.pop() == 10;
        assert pq.pop() == 15;

        assert pq.size() == 0;
    }

    static void testUpdatePriority() {
        PriorityQueue<Integer> pq = new PriorityQueue<>();

        pq.push(10);
        pq.push(5);

        // Update to have higher priority
        pq.update(10, 3);
        assert pq.peek() == 3;
        assert pq.size() == 2;

        // Pop should now give updated value first
        assert pq.pop() == 3;
        assert pq.pop() == 5;
    }

    static void testRemove() {
        PriorityQueue<Integer> pq = new PriorityQueue<>();

        pq.push(10);
        pq.push(5);
        pq.push(15);

        // Remove middle priority task
        pq.remove(10);
        assert pq.size() == 2;
        assert !pq.contains(10);

        // Verify correct items remain
        assert pq.pop() == 5;
        assert pq.pop() == 15;
    }

    static void testContains() {
        PriorityQueue<Integer> pq = new PriorityQueue<>();

        pq.push(10);
        pq.push(5);

        assert pq.contains(10);
        assert pq.contains(5);
        assert !pq.contains(3);

        pq.remove(10);
        assert !pq.contains(10);
    }

    static void testEmptyOperations() {
        PriorityQueue<Integer> pq = new PriorityQueue<>();

        // Test peek on empty queue
        assert pq.peek() == null;

        // Test pop on empty queue
        try {
            pq.pop();
            assert false : "Should throw IllegalStateException";
        } catch (IllegalStateException e) {
            // Expected
        }
    }

    static void testRemoveNonexistent() {
        PriorityQueue<Integer> pq = new PriorityQueue<>();

        pq.push(10);

        try {
            pq.remove(999);
            assert false : "Should throw IllegalArgumentException";
        } catch (IllegalArgumentException e) {
            // Expected
        }
    }

    static void testSingleElement() {
        PriorityQueue<Integer> pq = new PriorityQueue<>();

        pq.push(42);
        assert pq.size() == 1;
        assert pq.peek() == 42;
        assert pq.pop() == 42;
        assert pq.size() == 0;
    }

    static void testDuplicatePriorities() {
        PriorityQueue<Integer> pq = new PriorityQueue<>();

        pq.push(10);
        pq.push(10);
        pq.push(10);

        assert pq.size() == 3;

        // All should pop eventually
        assert pq.pop() == 10;
        assert pq.pop() == 10;
        assert pq.pop() == 10;
    }

    static void testWithDoubles() {
        PriorityQueue<Double> pq = new PriorityQueue<>();

        pq.push(1.5);
        pq.push(0.5);
        pq.push(2.3);

        assert pq.pop() == 0.5;
        assert pq.pop() == 1.5;
        assert pq.pop() == 2.3;
    }

    public static void main(String[] args) {
        testBasicOperations();
        testUpdatePriority();
        testRemove();
        testContains();
        testEmptyOperations();
        testRemoveNonexistent();
        testSingleElement();
        testDuplicatePriorities();
        testWithDoubles();
        testMain();
        System.out.println("All tests passed!");
    }
}
