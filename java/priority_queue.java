/*
Generic priority queue (min-heap) with update and remove operations.

Supports:
- push(item): Add item to heap - O(log n)
- pop(): Remove and return minimum item - O(log n)
- peek(): View minimum item without removing - O(1)
- update(old_item, new_item): Update item in heap - O(n)
- remove(item): Remove specific item - O(n)

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
                throw new IllegalStateException("Heap is empty");
            }
            return heap.get(0);
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
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        pq.push(5);
        pq.push(2);
        pq.push(8);
        pq.push(1);

        assert pq.peek() == 1;
        assert pq.pop() == 1;
        assert pq.pop() == 2;

        pq.update(8, 3);
        assert pq.pop() == 3;
    }

    // Don't write tests below during competition.

    static void testEmpty() {
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        assert pq.isEmpty();
        assert pq.size() == 0;
    }

    static void testRemove() {
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        pq.push(5);
        pq.push(2);
        pq.push(8);
        pq.remove(2);
        assert pq.pop() == 5;
        assert pq.pop() == 8;
    }

    public static void main(String[] args) {
        testEmpty();
        testRemove();
        testMain();
        System.out.println("All tests passed!");
    }
}
