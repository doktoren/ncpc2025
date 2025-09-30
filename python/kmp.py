"""
Knuth-Morris-Pratt (KMP) algorithm for efficient string pattern matching.

Finds all occurrences of a pattern string within a text string using a failure function
to avoid redundant comparisons. The preprocessing phase builds a table that allows
skipping characters during mismatches.

Time complexity: O(n + m) where n is text length and m is pattern length.
Space complexity: O(m) for the failure function table.
"""

from __future__ import annotations


def compute_failure_function(pattern: str) -> list[int]:
    """
    Compute the failure function for KMP algorithm.

    failure[i] = length of longest proper prefix of pattern[0:i+1]
    that is also a suffix of pattern[0:i+1]
    """
    m = len(pattern)
    failure = [0] * m
    j = 0

    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = failure[j - 1]

        if pattern[i] == pattern[j]:
            j += 1

        failure[i] = j

    return failure


def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Find all starting positions where pattern occurs in text.

    Returns a list of 0-indexed positions where pattern begins in text.
    """
    if not pattern:
        return []

    n, m = len(text), len(pattern)
    if m > n:
        return []

    failure = compute_failure_function(pattern)
    matches = []
    j = 0  # index for pattern

    for i in range(n):  # index for text
        while j > 0 and text[i] != pattern[j]:
            j = failure[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == m:
            matches.append(i - m + 1)
            j = failure[j - 1]

    return matches


def kmp_count(text: str, pattern: str) -> int:
    """Count number of occurrences of pattern in text."""
    return len(kmp_search(text, pattern))


def test_main() -> None:
    text = "ababcababa"
    pattern = "aba"
    matches = kmp_search(text, pattern)
    assert matches == [0, 5, 7]
    assert kmp_count(text, pattern) == 3

    # Test failure function
    failure = compute_failure_function("abcabcab")
    assert failure == [0, 0, 0, 1, 2, 3, 4, 5]


# Don't write tests below during competition.


def test_empty_patterns() -> None:
    # Empty pattern should return empty list
    assert kmp_search("hello", "") == []
    assert kmp_count("hello", "") == 0

    # Empty text with non-empty pattern
    assert kmp_search("", "abc") == []
    assert kmp_count("", "abc") == 0

    # Both empty
    assert kmp_search("", "") == []
    assert kmp_count("", "") == 0


def test_single_character() -> None:
    # Single character pattern in single character text
    assert kmp_search("a", "a") == [0]
    assert kmp_search("a", "b") == []

    # Single character pattern in longer text
    assert kmp_search("aaaa", "a") == [0, 1, 2, 3]
    assert kmp_search("abab", "a") == [0, 2]
    assert kmp_search("abab", "b") == [1, 3]


def test_pattern_longer_than_text() -> None:
    assert kmp_search("abc", "abcdef") == []
    assert kmp_search("x", "xyz") == []
    assert kmp_count("short", "verylongpattern") == 0


def test_overlapping_matches() -> None:
    # Pattern that overlaps with itself
    text = "aaaa"
    pattern = "aa"
    assert kmp_search(text, pattern) == [0, 1, 2]
    assert kmp_count(text, pattern) == 3

    # More complex overlapping
    text = "abababab"
    pattern = "abab"
    assert kmp_search(text, pattern) == [0, 2, 4]


def test_no_matches() -> None:
    assert kmp_search("abcdef", "xyz") == []
    assert kmp_search("hello world", "goodbye") == []
    assert kmp_count("mississippi", "xyz") == 0


def test_full_text_match() -> None:
    text = "hello"
    pattern = "hello"
    assert kmp_search(text, pattern) == [0]
    assert kmp_count(text, pattern) == 1


def test_repeated_patterns() -> None:
    # All same character
    text = "aaaaaaa"
    pattern = "aaa"
    assert kmp_search(text, pattern) == [0, 1, 2, 3, 4]

    # Repeated subpattern
    text = "abcabcabcabc"
    pattern = "abcabc"
    assert kmp_search(text, pattern) == [0, 3, 6]


def test_failure_function_edge_cases() -> None:
    # No repeating prefixes
    failure = compute_failure_function("abcdef")
    assert failure == [0, 0, 0, 0, 0, 0]

    # All same character
    failure = compute_failure_function("aaaa")
    assert failure == [0, 1, 2, 3]

    # Complex pattern with multiple prefix-suffix matches
    failure = compute_failure_function("abcabcabcab")
    assert failure == [0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8]

    # Pattern with internal repetition
    failure = compute_failure_function("ababcabab")
    assert failure == [0, 0, 1, 2, 0, 1, 2, 3, 4]


def test_case_sensitive() -> None:
    # Should be case sensitive
    assert kmp_search("Hello", "hello") == []
    assert kmp_search("HELLO", "hello") == []
    assert kmp_search("Hello", "H") == [0]
    assert kmp_search("Hello", "h") == []


def test_special_characters() -> None:
    text = "a@b#c$d%e"
    pattern = "@b#"
    assert kmp_search(text, pattern) == [1]

    text = "...test..."
    pattern = "..."
    assert kmp_search(text, pattern) == [0, 7]


def test_large_text_small_pattern() -> None:
    # Large text with small repeated pattern
    text = "a" * 1000 + "b" + "a" * 1000
    pattern = "b"
    assert kmp_search(text, pattern) == [1000]
    assert kmp_count(text, pattern) == 1

    # Pattern at end
    text = "x" * 999 + "target"
    pattern = "target"
    assert kmp_search(text, pattern) == [999]


def test_stress_many_matches() -> None:
    # Many overlapping matches
    text = "a" * 100
    pattern = "a" * 10
    expected = list(range(91))  # Positions 0 through 90
    assert kmp_search(text, pattern) == expected
    assert kmp_count(text, pattern) == 91


def test_binary_strings() -> None:
    # Binary pattern matching
    text = "1010101010"
    pattern = "101"
    assert kmp_search(text, pattern) == [0, 2, 4, 6]

    # No matches in binary
    text = "0000000000"
    pattern = "101"
    assert kmp_search(text, pattern) == []


def test_periodic_patterns() -> None:
    # Highly periodic pattern
    text = "abababababab"
    pattern = "ababab"
    assert kmp_search(text, pattern) == [0, 2, 4, 6]

    # Pattern is prefix of text
    text = "abcdefghijk"
    pattern = "abcde"
    assert kmp_search(text, pattern) == [0]


def test_failure_function_comprehensive() -> None:
    # Test various complex failure function cases

    # Palindromic pattern
    failure = compute_failure_function("abacaba")
    assert failure == [0, 0, 1, 0, 1, 2, 3]

    # Pattern with nested repetitions
    failure = compute_failure_function("aabaaaba")
    assert failure == [0, 1, 0, 1, 2, 2, 3, 4]

    # Long repetitive pattern
    failure = compute_failure_function("ababababab")
    assert failure == [0, 0, 1, 2, 3, 4, 5, 6, 7, 8]


def test_unicode_strings() -> None:
    # Unicode text and pattern
    text = "αβγδεζηθ"
    pattern = "γδε"
    assert kmp_search(text, pattern) == [2]

    text = "🙂🙃🙂🙃🙂"
    pattern = "🙂🙃"
    assert kmp_search(text, pattern) == [0, 2]


def main() -> None:
    test_main()
    test_empty_patterns()
    test_single_character()
    test_pattern_longer_than_text()
    test_overlapping_matches()
    test_no_matches()
    test_full_text_match()
    test_repeated_patterns()
    test_failure_function_edge_cases()
    test_case_sensitive()
    test_special_characters()
    test_large_text_small_pattern()
    test_stress_many_matches()
    test_binary_strings()
    test_periodic_patterns()
    test_failure_function_comprehensive()
    test_unicode_strings()


if __name__ == "__main__":
    main()
