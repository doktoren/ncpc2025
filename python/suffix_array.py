"""
Suffix Array construction with Longest Common Prefix (LCP) array using Kasai's algorithm.

A suffix array is a sorted array of all suffixes of a string. The LCP array stores the length
of the longest common prefix between consecutive suffixes in the suffix array. These structures
enable efficient string pattern matching and various string algorithms.

Time complexity: O(n log n) for suffix array construction, O(n) for LCP array.
Space complexity: O(n) for suffix array and LCP array.
"""

from __future__ import annotations

# Don't use annotations during contest
from typing import Final


class SuffixArray:
    def __init__(self, text: str) -> None:
        self.text: Final[str] = text
        self.n: Final[int] = len(text)
        self.sa: list[int] = self._build_suffix_array()
        self.lcp: list[int] = self._build_lcp_array()

    def _build_suffix_array(self) -> list[int]:
        """Build suffix array using Python's sort with custom key."""
        suffixes = list(range(self.n))
        suffixes.sort(key=lambda i: self.text[i:])
        return suffixes

    def _build_lcp_array(self) -> list[int]:
        """
        Build LCP array using Kasai's algorithm.

        lcp[i] = length of longest common prefix between sa[i] and sa[i-1].
        lcp[0] is defined as 0.
        """
        if self.n == 0:
            return []

        # Build rank array: rank[i] = position of suffix i in suffix array
        rank = [0] * self.n
        for i in range(self.n):
            rank[self.sa[i]] = i

        lcp = [0] * self.n
        h = 0  # Length of current LCP

        for i in range(self.n):
            if rank[i] > 0:
                j = self.sa[rank[i] - 1]  # Previous suffix in sorted order
                # Extend LCP from previous calculation
                while i + h < self.n and j + h < self.n and self.text[i + h] == self.text[j + h]:
                    h += 1
                lcp[rank[i]] = h
                if h > 0:
                    h -= 1

        return lcp

    def find_pattern(self, pattern: str) -> list[int]:
        """
        Find all occurrences of pattern in text.

        Returns list of starting positions where pattern occurs, in sorted order.
        """
        if not pattern:
            return []

        m = len(pattern)
        # Binary search for first occurrence
        left, right = 0, self.n

        # Find leftmost position where suffix >= pattern
        while left < right:
            mid = (left + right) // 2
            suffix = self.text[self.sa[mid]:]
            if suffix < pattern:
                left = mid + 1
            else:
                right = mid

        start = left

        # Find rightmost position where suffix starts with pattern
        left, right = start, self.n
        while left < right:
            mid = (left + right) // 2
            suffix = self.text[self.sa[mid]:self.sa[mid] + m]
            if suffix <= pattern:
                left = mid + 1
            else:
                right = mid

        end = left

        # Collect all matching positions
        result = [
            self.sa[i]
            for i in range(start, end)
            if self.text[self.sa[i]:self.sa[i] + m] == pattern
        ]
        return sorted(result)


def test_main() -> None:
    # Test suffix array and LCP for "banana"
    sa = SuffixArray("banana")
    # Suffixes in sorted order: "a", "ana", "anana", "banana", "na", "nana"
    # Corresponding starting positions: 5, 3, 1, 0, 4, 2
    assert sa.sa == [5, 3, 1, 0, 4, 2]
    # LCP: [0, 1, 3, 0, 0, 2]
    assert sa.lcp == [0, 1, 3, 0, 0, 2]

    # Test pattern finding
    positions = sa.find_pattern("ana")
    assert positions == [1, 3]


# Don't write tests below during competition.


def test_empty_string() -> None:
    sa = SuffixArray("")
    assert sa.sa == []
    assert sa.lcp == []
    assert sa.find_pattern("a") == []


def test_single_char() -> None:
    sa = SuffixArray("a")
    assert sa.sa == [0]
    assert sa.lcp == [0]


def test_repeated_chars() -> None:
    sa = SuffixArray("aaaa")
    assert sa.sa == [3, 2, 1, 0]
    # LCP: all have LCP with previous (except first)
    assert sa.lcp == [0, 1, 2, 3]


def test_pattern_not_found() -> None:
    sa = SuffixArray("hello")
    assert sa.find_pattern("world") == []


def test_pattern_at_end() -> None:
    sa = SuffixArray("hello")
    assert sa.find_pattern("lo") == [3]


def test_overlapping_patterns() -> None:
    sa = SuffixArray("aabaabaa")
    positions = sa.find_pattern("aa")
    assert sorted(positions) == [0, 3, 6]


def test_entire_string() -> None:
    text = "programming"
    sa = SuffixArray(text)
    assert sa.find_pattern(text) == [0]


def test_lcp_calculation() -> None:
    sa = SuffixArray("abcab")
    # Suffixes sorted: "ab", "abcab", "b", "bcab", "cab"
    # Positions: 3, 0, 4, 1, 2
    assert sa.sa == [3, 0, 4, 1, 2]
    # LCP between consecutive suffixes
    assert sa.lcp[0] == 0  # First has no predecessor
    assert sa.lcp[1] == 2  # "ab" and "abcab" share "ab"
    assert sa.lcp[2] == 0  # "abcab" and "b" share nothing
    assert sa.lcp[3] == 1  # "b" and "bcab" share "b"
    assert sa.lcp[4] == 0  # "bcab" and "cab" share nothing


def test_all_unique_chars() -> None:
    sa = SuffixArray("abcd")
    assert sa.sa == [0, 1, 2, 3]
    assert sa.lcp == [0, 0, 0, 0]


def test_palindrome() -> None:
    sa = SuffixArray("racecar")
    positions = sa.find_pattern("r")
    assert sorted(positions) == [0, 6]


def test_long_pattern() -> None:
    text = "thequickbrownfoxjumpsoverthelazydog"
    sa = SuffixArray(text)
    assert sa.find_pattern("jumps") == [16]
    assert sa.find_pattern("the") == [0, 25]


def main() -> None:
    test_main()
    test_empty_string()
    test_single_char()
    test_repeated_chars()
    test_pattern_not_found()
    test_pattern_at_end()
    test_overlapping_patterns()
    test_entire_string()
    test_lcp_calculation()
    test_all_unique_chars()
    test_palindrome()
    test_long_pattern()


if __name__ == "__main__":
    main()
