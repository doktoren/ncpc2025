/*
Suffix Array construction with Longest Common Prefix (LCP) array using Kasai's algorithm.

Time complexity: O(n log n) for suffix array, O(n) for LCP array.
Space complexity: O(n).
*/

#include <algorithm>
#include <cassert>
#include <iostream>
#include <string>
#include <vector>

class SuffixArray {
  private:
    std::string text;
    int n;
    std::vector<int> sa;
    std::vector<int> lcp;

    std::vector<int> build_suffix_array() {
        std::vector<int> suffixes(n);
        for (int i = 0; i < n; i++) { suffixes[i] = i; }
        std::sort(suffixes.begin(), suffixes.end(),
                  [this](int a, int b) { return text.substr(a) < text.substr(b); });
        return suffixes;
    }

    std::vector<int> build_lcp_array() {
        if (n == 0) { return {}; }

        std::vector<int> rank(n);
        for (int i = 0; i < n; i++) { rank[sa[i]] = i; }

        std::vector<int> lcp(n, 0);
        int h = 0;

        for (int i = 0; i < n; i++) {
            if (rank[i] > 0) {
                int j = sa[rank[i] - 1];
                while (i + h < n && j + h < n && text[i + h] == text[j + h]) { h++; }
                lcp[rank[i]] = h;
                if (h > 0) { h--; }
            }
        }

        return lcp;
    }

  public:
    SuffixArray(const std::string& text) : text(text), n(text.length()) {
        sa = build_suffix_array();
        lcp = build_lcp_array();
    }

    std::vector<int> find_pattern(const std::string& pattern) {
        if (pattern.empty()) { return {}; }

        int m = pattern.length();
        int left = 0, right = n;

        while (left < right) {
            int mid = (left + right) / 2;
            if (text.substr(sa[mid]) < pattern) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        int start = left;
        left = start;
        right = n;

        while (left < right) {
            int mid = (left + right) / 2;
            std::string suffix = text.substr(sa[mid], std::min(m, n - sa[mid]));
            if (suffix <= pattern) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        int end = left;

        std::vector<int> result;
        for (int i = start; i < end; i++) {
            if (sa[i] + m <= n && text.substr(sa[i], m) == pattern) { result.push_back(sa[i]); }
        }

        std::sort(result.begin(), result.end());
        return result;
    }

    const std::vector<int>& get_sa() const {
        return sa;
    }

    const std::vector<int>& get_lcp() const {
        return lcp;
    }
};

void test_main() {
    SuffixArray sa("banana");
    assert(sa.get_sa() == std::vector<int>({5, 3, 1, 0, 4, 2}));
    assert(sa.get_lcp() == std::vector<int>({0, 1, 3, 0, 0, 2}));

    auto positions = sa.find_pattern("ana");
    assert(positions == std::vector<int>({1, 3}));
}

// Don't write tests below during competition.

void test_empty_string() {
    SuffixArray sa("");
    assert(sa.get_sa().empty());
    assert(sa.get_lcp().empty());
}

void test_single_char() {
    SuffixArray sa("a");
    assert(sa.get_sa().size() == 1);
}

void test_repeated_chars() {
    SuffixArray sa("aaaa");
    assert(sa.get_sa() == std::vector<int>({3, 2, 1, 0}));
    assert(sa.get_lcp() == std::vector<int>({0, 1, 2, 3}));
}

void test_pattern_not_found() {
    SuffixArray sa("hello");
    assert(sa.find_pattern("world").empty());
}

void test_overlapping_patterns() {
    SuffixArray sa("aabaabaa");
    auto positions = sa.find_pattern("aa");
    assert(positions == std::vector<int>({0, 3, 6}));
}

int main() {
    test_main();
    test_empty_string();
    test_single_char();
    test_repeated_chars();
    test_pattern_not_found();
    test_overlapping_patterns();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}
