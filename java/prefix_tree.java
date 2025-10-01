/*
Prefix Tree (Trie) implementation for efficient string prefix operations.

Supports:
- insert(word): Add a word to the trie - O(m) where m is word length
- search(word): Check if exact word exists - O(m)
- startsWith(prefix): Check if any word starts with prefix - O(m)
- delete(word): Remove a word from the trie - O(m)

Space complexity: O(ALPHABET_SIZE * N * M) where N is number of words and M is average length
*/

import java.util.*;

class prefix_tree {
    static class TrieNode {
        Map<Character, TrieNode> children;
        boolean isEndOfWord;

        TrieNode() {
            children = new HashMap<>();
            isEndOfWord = false;
        }
    }

    static class PrefixTree {
        private TrieNode root;

        PrefixTree() {
            root = new TrieNode();
        }

        void insert(String word) {
            TrieNode node = root;
            for (char c : word.toCharArray()) {
                node.children.putIfAbsent(c, new TrieNode());
                node = node.children.get(c);
            }
            node.isEndOfWord = true;
        }

        boolean search(String word) {
            TrieNode node = root;
            for (char c : word.toCharArray()) {
                if (!node.children.containsKey(c)) {
                    return false;
                }
                node = node.children.get(c);
            }
            return node.isEndOfWord;
        }

        boolean startsWith(String prefix) {
            TrieNode node = root;
            for (char c : prefix.toCharArray()) {
                if (!node.children.containsKey(c)) {
                    return false;
                }
                node = node.children.get(c);
            }
            return true;
        }

        boolean delete(String word) {
            return deleteHelper(root, word, 0);
        }

        private boolean deleteHelper(TrieNode node, String word, int depth) {
            if (node == null) {
                return false;
            }

            if (depth == word.length()) {
                if (!node.isEndOfWord) {
                    return false;
                }
                node.isEndOfWord = false;
                return node.children.isEmpty();
            }

            char c = word.charAt(depth);
            if (!node.children.containsKey(c)) {
                return false;
            }

            TrieNode child = node.children.get(c);
            boolean shouldDeleteChild = deleteHelper(child, word, depth + 1);

            if (shouldDeleteChild) {
                node.children.remove(c);
                return !node.isEndOfWord && node.children.isEmpty();
            }

            return false;
        }
    }

    static void testMain() {
        PrefixTree trie = new PrefixTree();
        trie.insert("cat");
        trie.insert("car");
        trie.insert("card");

        assert trie.search("car");
        assert !trie.search("ca");
        assert trie.startsWith("car");
    }

    // Don't write tests below during competition.

    static void testEmpty() {
        PrefixTree trie = new PrefixTree();
        assert !trie.search("test");
        assert !trie.startsWith("test");
    }

    static void testOverlappingWords() {
        PrefixTree trie = new PrefixTree();
        trie.insert("car");
        trie.insert("card");
        trie.insert("care");
        trie.insert("careful");

        assert trie.search("car");
        assert trie.search("card");
        assert trie.search("careful");
        assert !trie.search("ca");
        assert trie.startsWith("car");
        assert trie.startsWith("care");
    }

    static void testDeleteNonexistent() {
        PrefixTree trie = new PrefixTree();
        trie.insert("test");
        assert !trie.delete("testing");
        assert trie.search("test");
    }

    public static void main(String[] args) {
        testEmpty();
        testOverlappingWords();
        testDeleteNonexistent();
        testMain();
        System.out.println("All tests passed!");
    }
}
