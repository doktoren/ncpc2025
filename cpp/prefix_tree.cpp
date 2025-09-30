/*
Write-only prefix tree (trie) for efficient string storage and retrieval.

Supports adding strings and finding all strings that are prefixes of a given string.
The tree structure allows for efficient storage of strings with common prefixes.

Time complexity: O(m) for add and find operations, where m is the length of the string.
Space complexity: O(ALPHABET_SIZE * N * M) in the worst case, where N is the number
of strings and M is the average length of strings.
*/

#include <string>
#include <unordered_map>
#include <vector>
#include <cassert>
#include <iostream>

class PrefixTree {
private:
    struct TrieNode {
        std::unordered_map<char, TrieNode*> children;
        bool is_end_of_word;

        TrieNode() : is_end_of_word(false) {}

        ~TrieNode() {
            for (auto& pair : children) {
                delete pair.second;
            }
        }
    };

    TrieNode* root;

public:
    PrefixTree() {
        root = new TrieNode();
    }

    ~PrefixTree() {
        delete root;
    }

    void add(const std::string& word) {
        TrieNode* current = root;
        for (char c : word) {
            if (current->children.find(c) == current->children.end()) {
                current->children[c] = new TrieNode();
            }
            current = current->children[c];
        }
        current->is_end_of_word = true;
    }

    bool contains(const std::string& word) {
        TrieNode* current = root;
        for (char c : word) {
            if (current->children.find(c) == current->children.end()) {
                return false;
            }
            current = current->children[c];
        }
        return current->is_end_of_word;
    }

    bool starts_with(const std::string& prefix) {
        TrieNode* current = root;
        for (char c : prefix) {
            if (current->children.find(c) == current->children.end()) {
                return false;
            }
            current = current->children[c];
        }
        return true;
    }

    void find_all_prefixes(const std::string& text, std::vector<int>& end_positions) {
        for (int i = 0; i < text.length(); i++) {
            TrieNode* current = root;
            for (int j = i; j < text.length(); j++) {
                char c = text[j];
                if (current->children.find(c) == current->children.end()) {
                    break;
                }
                current = current->children[c];
                if (current->is_end_of_word) {
                    end_positions.push_back(j + 1);
                }
            }
        }
    }

    int max_depth() {
        return max_depth_helper(root);
    }

private:
    int max_depth_helper(TrieNode* node) {
        if (node->children.empty()) {
            return 0;
        }
        int max_child_depth = 0;
        for (auto& pair : node->children) {
            max_child_depth = std::max(max_child_depth, max_depth_helper(pair.second));
        }
        return 1 + max_child_depth;
    }
};

void test_main() {
    PrefixTree pt;
    pt.add("hello");
    pt.add("help");
    pt.add("her");
    assert(pt.contains("hello"));
    assert(pt.starts_with("he"));
    assert(!pt.contains("he"));
}

// Don't write tests below during competition.

void test_basic() {
    PrefixTree trie;

    // Test adding and searching
    trie.add("cat");
    trie.add("car");
    trie.add("card");
    trie.add("care");
    trie.add("careful");

    assert(trie.contains("cat"));
    assert(trie.contains("car"));
    assert(trie.contains("card"));
    assert(trie.contains("care"));
    assert(trie.contains("careful"));

    assert(!trie.contains("c"));
    assert(!trie.contains("ca"));
    assert(!trie.contains("cards"));
    assert(!trie.contains("dog"));

    // Test prefix checking
    assert(trie.starts_with("c"));
    assert(trie.starts_with("ca"));
    assert(trie.starts_with("car"));
    assert(trie.starts_with("care"));
    assert(!trie.starts_with("dog"));
    assert(!trie.starts_with("careless"));
}

void test_prefix_finding() {
    PrefixTree trie;
    trie.add("a");
    trie.add("to");
    trie.add("tea");
    trie.add("ted");
    trie.add("ten");
    trie.add("i");
    trie.add("in");
    trie.add("inn");

    std::vector<int> positions;
    trie.find_all_prefixes("ateatento", positions);

    // Should find "a" at position 1, "tea" at position 4, "te" at position 6, "ten" at position 8
    assert(positions.size() >= 2); // At least "a" and "tea"
}

void test_empty_and_edge_cases() {
    PrefixTree trie;

    // Empty trie
    assert(!trie.contains(""));
    assert(!trie.contains("test"));

    // Add empty string
    trie.add("");
    assert(trie.contains(""));

    // Single character
    trie.add("a");
    assert(trie.contains("a"));
    assert(trie.starts_with("a"));
}

int main() {
    test_basic();
    test_prefix_finding();
    test_empty_and_edge_cases();
    test_main();
    std::cout << "All Prefix Tree tests passed!" << std::endl;
    return 0;
}