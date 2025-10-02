/*
Knuth-Morris-Pratt (KMP) algorithm for efficient string pattern matching.

Finds all occurrences of a pattern string within a text string using a failure function
to avoid redundant comparisons. The preprocessing phase builds a table that allows
skipping characters during mismatches.

Time complexity: O(n + m) where n is text length and m is pattern length.
Space complexity: O(m) for the failure function table.
*/

#include <cassert>
#include <iostream>
#include <string>
#include <vector>

std::vector<int> compute_failure_function(const std::string& pattern) {
    /*
    Compute the failure function for KMP algorithm.

    failure[i] = length of longest proper prefix of pattern[0:i+1]
    that is also a suffix of pattern[0:i+1]
    */
    int m = pattern.length();
    std::vector<int> failure(m, 0);
    int j = 0;

    for (int i = 1; i < m; i++) {
        while (j > 0 && pattern[i] != pattern[j]) { j = failure[j - 1]; }

        if (pattern[i] == pattern[j]) { j++; }

        failure[i] = j;
    }

    return failure;
}

std::vector<int> kmp_search(const std::string& text, const std::string& pattern) {
    /*
    Find all starting positions where pattern occurs in text.

    Returns a list of 0-indexed positions where pattern begins in text.
    */
    if (pattern.empty()) { return {}; }

    int n = text.length(), m = pattern.length();
    if (m > n) { return {}; }

    std::vector<int> failure = compute_failure_function(pattern);
    std::vector<int> matches;
    int j = 0;  // index for pattern

    for (int i = 0; i < n; i++) {  // index for text
        while (j > 0 && text[i] != pattern[j]) { j = failure[j - 1]; }

        if (text[i] == pattern[j]) { j++; }

        if (j == m) {
            matches.push_back(i - m + 1);
            j = failure[j - 1];
        }
    }

    return matches;
}

int kmp_count(const std::string& text, const std::string& pattern) {
    /* Count number of occurrences of pattern in text. */
    return kmp_search(text, pattern).size();
}

void test_main() {
    std::string text = "ababcababa";
    std::string pattern = "aba";
    std::vector<int> matches = kmp_search(text, pattern);
    assert(matches == std::vector<int>({0, 5, 7}));
    assert(kmp_count(text, pattern) == 3);

    // Test failure function
    std::vector<int> failure = compute_failure_function("abcabcab");
    assert(failure == std::vector<int>({0, 0, 0, 1, 2, 3, 4, 5}));
}

// Don't write tests below during competition.

void test_empty_patterns() {
    // Empty pattern should return empty list
    assert(kmp_search("hello", "").empty());
    assert(kmp_count("hello", "") == 0);

    // Empty text with non-empty pattern
    assert(kmp_search("", "abc").empty());
    assert(kmp_count("", "abc") == 0);

    // Both empty
    assert(kmp_search("", "").empty());
    assert(kmp_count("", "") == 0);
}

void test_single_character() {
    // Single character pattern in single character text
    assert(kmp_search("a", "a") == std::vector<int>({0}));
    assert(kmp_search("a", "b").empty());

    // Single character pattern in longer text
    assert(kmp_search("aaaa", "a") == std::vector<int>({0, 1, 2, 3}));
    assert(kmp_search("abab", "a") == std::vector<int>({0, 2}));
    assert(kmp_search("abab", "b") == std::vector<int>({1, 3}));
}

void test_pattern_longer_than_text() {
    assert(kmp_search("abc", "abcdef").empty());
    assert(kmp_search("x", "xyz").empty());
    assert(kmp_count("short", "verylongpattern") == 0);
}

void test_overlapping_matches() {
    // Pattern that overlaps with itself
    std::string text = "aaaa";
    std::string pattern = "aa";
    assert(kmp_search(text, pattern) == std::vector<int>({0, 1, 2}));
    assert(kmp_count(text, pattern) == 3);

    // More complex overlapping
    text = "abababab";
    pattern = "abab";
    assert(kmp_search(text, pattern) == std::vector<int>({0, 2, 4}));
}

void test_no_matches() {
    assert(kmp_search("abcdef", "xyz").empty());
    assert(kmp_search("hello world", "goodbye").empty());
    assert(kmp_count("mississippi", "xyz") == 0);
}

void test_full_text_match() {
    std::string text = "hello";
    std::string pattern = "hello";
    assert(kmp_search(text, pattern) == std::vector<int>({0}));
    assert(kmp_count(text, pattern) == 1);
}

void test_repeated_patterns() {
    // All same character
    std::string text = "aaaaaaa";
    std::string pattern = "aaa";
    assert(kmp_search(text, pattern) == std::vector<int>({0, 1, 2, 3, 4}));

    // Repeated subpattern
    text = "abcabcabcabc";
    pattern = "abcabc";
    assert(kmp_search(text, pattern) == std::vector<int>({0, 3, 6}));
}

void test_failure_function_edge_cases() {
    // No repeating prefixes
    std::vector<int> failure = compute_failure_function("abcdef");
    assert(failure == std::vector<int>({0, 0, 0, 0, 0, 0}));

    // All same character
    failure = compute_failure_function("aaaa");
    assert(failure == std::vector<int>({0, 1, 2, 3}));

    // Complex pattern with multiple prefix-suffix matches
    failure = compute_failure_function("abcabcabcab");
    assert(failure == std::vector<int>({0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8}));

    // Pattern with internal repetition
    failure = compute_failure_function("ababcabab");
    assert(failure == std::vector<int>({0, 0, 1, 2, 0, 1, 2, 3, 4}));
}

void test_case_sensitive() {
    // Should be case sensitive
    assert(kmp_search("Hello", "hello").empty());
    assert(kmp_search("HELLO", "hello").empty());
    assert(kmp_search("Hello", "H") == std::vector<int>({0}));
    assert(kmp_search("Hello", "h").empty());
}

void test_special_characters() {
    std::string text = "a@b#c$d%e";
    std::string pattern = "@b#";
    assert(kmp_search(text, pattern) == std::vector<int>({1}));

    text = "...test...";
    pattern = "...";
    assert(kmp_search(text, pattern) == std::vector<int>({0, 7}));
}

void test_large_text_small_pattern() {
    // Large text with small repeated pattern
    std::string text = std::string(1000, 'a') + "b" + std::string(1000, 'a');
    std::string pattern = "b";
    assert(kmp_search(text, pattern) == std::vector<int>({1000}));
    assert(kmp_count(text, pattern) == 1);

    // Pattern at end
    text = std::string(999, 'x') + "target";
    pattern = "target";
    assert(kmp_search(text, pattern) == std::vector<int>({999}));
}

void test_stress_many_matches() {
    // Many overlapping matches
    std::string text(100, 'a');
    std::string pattern(10, 'a');
    std::vector<int> expected;
    for (int i = 0; i <= 90; i++) { expected.push_back(i); }
    assert(kmp_search(text, pattern) == expected);
    assert(kmp_count(text, pattern) == 91);
}

void test_binary_strings() {
    // Binary pattern matching
    std::string text = "1010101010";
    std::string pattern = "101";
    assert(kmp_search(text, pattern) == std::vector<int>({0, 2, 4, 6}));

    // No matches in binary
    text = "0000000000";
    pattern = "101";
    assert(kmp_search(text, pattern).empty());
}

void test_periodic_patterns() {
    // Highly periodic pattern
    std::string text = "abababababab";
    std::string pattern = "ababab";
    assert(kmp_search(text, pattern) == std::vector<int>({0, 2, 4, 6}));

    // Pattern is prefix of text
    text = "abcdefghijk";
    pattern = "abcde";
    assert(kmp_search(text, pattern) == std::vector<int>({0}));
}

void test_failure_function_comprehensive() {
    // Test various complex failure function cases

    // Palindromic pattern
    std::vector<int> failure = compute_failure_function("abacaba");
    assert(failure == std::vector<int>({0, 0, 1, 0, 1, 2, 3}));

    // Pattern with nested repetitions
    failure = compute_failure_function("aabaaaba");
    assert(failure == std::vector<int>({0, 1, 0, 1, 2, 2, 3, 4}));

    // Long repetitive pattern
    failure = compute_failure_function("ababababab");
    assert(failure == std::vector<int>({0, 0, 1, 2, 3, 4, 5, 6, 7, 8}));
}

void test_unicode_strings() {
    // Unicode text and pattern
    std::string text = "αβγδεζηθ";
    std::string pattern = "γδε";
    assert(kmp_search(text, pattern) ==
           std::vector<int>({4}));  // Note: byte offset, not char offset

    text = "🙂🙃🙂🙃🙂";
    pattern = "🙂🙃";
    assert(kmp_search(text, pattern) == std::vector<int>({0, 8}));  // Note: byte offsets
}

int main() {
    test_empty_patterns();
    test_single_character();
    test_pattern_longer_than_text();
    test_overlapping_matches();
    test_no_matches();
    test_full_text_match();
    test_repeated_patterns();
    test_failure_function_edge_cases();
    test_case_sensitive();
    test_special_characters();
    test_large_text_small_pattern();
    test_stress_many_matches();
    test_binary_strings();
    test_periodic_patterns();
    test_failure_function_comprehensive();
    test_unicode_strings();
    test_main();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}
