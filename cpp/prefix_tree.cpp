/*
Write-only prefix tree (trie) for efficient string storage and retrieval.

Supports adding strings and finding all strings that are prefixes of a given string.
The tree structure allows for efficient storage of strings with common prefixes.

Time complexity: O(m) for add and find operations, where m is the length of the string.
Space complexity: O(ALPHABET_SIZE * N * M) in the worst case, where N is the number
of strings and M is the average length of strings.
*/

#include <algorithm>
#include <cassert>
#include <iostream>
#include <string>
#include <vector>

class PrefixTree {
  private:
    std::vector<std::string> keys;
    std::vector<PrefixTree*> values;

  public:
    PrefixTree() {}

    ~PrefixTree() {
        for (auto* child : values) { delete child; }
    }

    void pp(int indent = 0) {
        // Pretty-print tree structure for debugging
        for (size_t i = 0; i < keys.size(); i++) {
            for (int j = 0; j < indent; j++) std::cout << " ";
            std::cout << keys[i] << ": " << (values[i] == nullptr ? "-" : "") << std::endl;
            if (values[i] != nullptr) { values[i]->pp(indent + 2); }
        }
    }

    void find_all(const std::string& s, int offset, std::vector<int>& append_to) {
        // Find all strings in tree that are prefixes of s[offset:]. Appends end positions.
        if (!keys.empty() && keys[0] == "") { append_to.push_back(offset); }
        if (offset >= s.length()) { return; }
        std::string target_char = s.substr(offset, 1);
        auto it = std::lower_bound(keys.begin(), keys.end(), target_char);
        int index = it - keys.begin();
        if (index == keys.size()) { return; }
        std::string key_substr = s.substr(offset, keys[index].length());
        if (key_substr == keys[index]) {
            PrefixTree* pt = values[index];
            if (pt == nullptr) {
                append_to.push_back(offset + keys[index].length());
            } else {
                pt->find_all(s, offset + keys[index].length(), append_to);
            }
        }
    }

    int max_len() {
        // Return length of longest string in tree
        int result = 0;
        for (size_t i = 0; i < keys.size(); i++) {
            result = std::max(
                result, (int)keys[i].length() + (values[i] == nullptr ? 0 : values[i]->max_len()));
        }
        return result;
    }

    void add(const std::string& s) {
        // Add string to tree
        if (s.empty() || keys.empty()) {
            keys.insert(keys.begin(), s);
            values.insert(values.begin(), nullptr);
            return;
        }

        auto it = std::lower_bound(keys.begin(), keys.end(), s);
        int pos = it - keys.begin();
        if (pos > 0 && !keys[pos - 1].empty() && keys[pos - 1][0] == s[0]) { pos--; }
        if (pos < keys.size() && !keys[pos].empty() && keys[pos][0] == s[0]) {
            // Merge
            if (s.find(keys[pos]) == 0 && s.length() >= keys[pos].length()) {
                // s starts with keys[pos]
                PrefixTree* pt = values[pos];
                if (pt == nullptr) {
                    PrefixTree* child = new PrefixTree();
                    child->keys.push_back("");
                    child->values.push_back(nullptr);
                    values[pos] = pt = child;
                }
                pt->add(s.substr(keys[pos].length()));
            } else if (keys[pos].find(s) == 0 && keys[pos].length() >= s.length()) {
                // keys[pos] starts with s
                PrefixTree* child = new PrefixTree();
                child->keys.push_back("");
                child->values.push_back(nullptr);
                child->keys.push_back(keys[pos].substr(s.length()));
                child->values.push_back(values[pos]);
                keys[pos] = s;
                values[pos] = child;
            } else {
                // Find common prefix
                int prefix = 1;
                while (prefix < s.length() && prefix < keys[pos].length() &&
                       s[prefix] == keys[pos][prefix]) {
                    prefix++;
                }
                PrefixTree* child = new PrefixTree();
                if (s < keys[pos]) {
                    child->keys.push_back(s.substr(prefix));
                    child->values.push_back(nullptr);
                }
                child->keys.push_back(keys[pos].substr(prefix));
                child->values.push_back(values[pos]);
                if (s >= keys[pos]) {
                    child->keys.push_back(s.substr(prefix));
                    child->values.push_back(nullptr);
                }
                keys[pos] = s.substr(0, prefix);
                values[pos] = child;
            }
        } else {
            keys.insert(keys.begin() + pos, s);
            values.insert(values.begin() + pos, nullptr);
        }
    }
};

void test_main() {
    PrefixTree p;
    p.add("cat");
    p.add("car");
    p.add("card");
    std::vector<int> l;
    p.find_all("card", 0, l);
    assert(l.size() == 2 && l[0] == 3 && l[1] == 4);
    assert(p.max_len() == 4);
}

// Don't write tests below during competition.

void test_empty_tree() {
    PrefixTree p;
    std::vector<int> l;
    p.find_all("test", 0, l);
    assert(l.empty());
    assert(p.max_len() == 0);
}

void test_single_string() {
    PrefixTree p;
    p.add("hello");
    std::vector<int> l;
    p.find_all("hello world", 0, l);
    assert(l.size() == 1);
    assert(l[0] == 5);
    assert(p.max_len() == 5);
}

void test_empty_string() {
    PrefixTree p;
    p.add("");
    std::vector<int> l;
    p.find_all("anything", 0, l);
    assert(l.size() == 1);
    assert(l[0] == 0);  // Empty string matches at position 0
}

void test_no_match() {
    PrefixTree p;
    p.add("cat");
    p.add("car");
    std::vector<int> l;
    p.find_all("dog", 0, l);
    assert(l.empty());
}

void test_partial_match() {
    PrefixTree p;
    p.add("catalog");
    std::vector<int> l;
    p.find_all("cat", 0, l);
    assert(l.empty());  // "catalog" is not a prefix of "cat"
}

void test_overlapping_strings() {
    PrefixTree p;
    p.add("a");
    p.add("ab");
    p.add("abc");
    std::vector<int> l;
    p.find_all("abcdef", 0, l);
    assert(l.size() == 3);
    assert(l[0] == 1);
    assert(l[1] == 2);
    assert(l[2] == 3);
}

void test_different_offsets() {
    PrefixTree p;
    p.add("test");
    std::vector<int> l;
    p.find_all("xxtest", 2, l);
    assert(l.size() == 1);
    assert(l[0] == 6);  // "test" found starting at offset 2, ends at 6
}

void test_multiple_words() {
    PrefixTree p;
    std::vector<std::string> words = {"the", "then", "there", "answer",
                                      "any", "by",   "bye",   "their"};
    for (const auto& word : words) { p.add(word); }

    std::vector<int> l;
    p.find_all("their", 0, l);
    // "the", "their" are prefixes of "their"
    bool found_3 = false, found_5 = false;
    for (int pos : l) {
        if (pos == 3) found_3 = true;
        if (pos == 5) found_5 = true;
    }
    assert(found_3 && found_5);
}

void test_common_prefix() {
    PrefixTree p;
    p.add("pre");
    p.add("prefix");
    p.add("prepare");

    std::vector<int> l;
    p.find_all("prefix", 0, l);
    assert(l.size() == 2);
    assert(l[0] == 3);  // "pre"
    assert(l[1] == 6);  // "prefix"
}

void test_max_len() {
    PrefixTree p;
    assert(p.max_len() == 0);

    p.add("a");
    assert(p.max_len() == 1);

    p.add("abc");
    assert(p.max_len() == 3);

    p.add("ab");
    assert(p.max_len() == 3);
}

void test_duplicate_add() {
    PrefixTree p;
    p.add("test");
    p.add("test");  // Add same string again

    std::vector<int> l;
    p.find_all("test", 0, l);
    // Should still work correctly
    bool found_4 = false;
    for (int pos : l) {
        if (pos == 4) found_4 = true;
    }
    assert(found_4);
}

int main() {
    test_empty_tree();
    test_single_string();
    test_empty_string();
    test_no_match();
    test_partial_match();
    test_overlapping_strings();
    test_different_offsets();
    test_multiple_words();
    test_common_prefix();
    test_max_len();
    test_duplicate_add();
    test_main();
    std::cout << "All Prefix Tree tests passed!" << std::endl;
    return 0;
}