/*
Knuth-Morris-Pratt (KMP) string matching algorithm.

Efficiently finds all occurrences of a pattern in a text string.

Key operations:
- computeLPS(pattern): Compute Longest Proper Prefix which is also Suffix array
- search(text, pattern): Find all starting positions where pattern occurs in text

Time complexity: O(n + m) where n is text length and m is pattern length
Space complexity: O(m) for the LPS array
*/

import java.util.*;

class kmp {
    static int[] computeLPS(String pattern) {
        int m = pattern.length();
        int[] lps = new int[m];
        int len = 0;
        int i = 1;

        lps[0] = 0;

        while (i < m) {
            if (pattern.charAt(i) == pattern.charAt(len)) {
                len++;
                lps[i] = len;
                i++;
            } else {
                if (len != 0) {
                    len = lps[len - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }

        return lps;
    }

    static List<Integer> search(String text, String pattern) {
        List<Integer> result = new ArrayList<>();

        if (pattern.isEmpty()) {
            return result;
        }

        int n = text.length();
        int m = pattern.length();
        int[] lps = computeLPS(pattern);

        int i = 0; // index for text
        int j = 0; // index for pattern

        while (i < n) {
            if (text.charAt(i) == pattern.charAt(j)) {
                i++;
                j++;
            }

            if (j == m) {
                result.add(i - j);
                j = lps[j - 1];
            } else if (i < n && text.charAt(i) != pattern.charAt(j)) {
                if (j != 0) {
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }

        return result;
    }

    static void testMain() {
        String text = "ababcababa";
        String pattern = "aba";
        List<Integer> matches = search(text, pattern);
        assert matches.equals(Arrays.asList(0, 5, 7));
        assert matches.size() == 3;

        // Test failure function
        int[] failure = computeLPS("abcabcab");
        assert Arrays.equals(failure, new int[] {0, 0, 0, 1, 2, 3, 4, 5});
    }

    // Don't write tests below during competition.

    static void testNoMatch() {
        List<Integer> result = search("ABCDEF", "XYZ");
        assert result.isEmpty();
    }

    static void testSingleChar() {
        List<Integer> result = search("AAAAA", "A");
        assert result.equals(Arrays.asList(0, 1, 2, 3, 4));
    }

    static void testEmptyPattern() {
        List<Integer> result = search("ABC", "");
        assert result.isEmpty();
    }

    static void testPatternLongerThanText() {
        List<Integer> result = search("AB", "ABCD");
        assert result.isEmpty();
    }

    static void testOverlappingMatches() {
        List<Integer> result = search("AAAA", "AA");
        assert result.equals(Arrays.asList(0, 1, 2));
    }

    static void testLPS() {
        int[] lps = computeLPS("AAAA");
        assert Arrays.equals(lps, new int[] {0, 1, 2, 3});

        lps = computeLPS("ABCDE");
        assert Arrays.equals(lps, new int[] {0, 0, 0, 0, 0});

        lps = computeLPS("AABAAA");
        assert Arrays.equals(lps, new int[] {0, 1, 0, 1, 2, 2});
    }

    static void testFullMatch() {
        List<Integer> result = search("PATTERN", "PATTERN");
        assert result.equals(Arrays.asList(0));
    }

    static void testMultipleOccurrences() {
        List<Integer> result = search("ABABABAB", "ABA");
        assert result.equals(Arrays.asList(0, 2, 4));
    }

    static void testComplexPattern() {
        String text = "ABCABDABCABC";
        String pattern = "ABC";
        List<Integer> result = search(text, pattern);
        assert result.equals(Arrays.asList(0, 6, 9));
    }

    public static void main(String[] args) {
        testNoMatch();
        testSingleChar();
        testEmptyPattern();
        testPatternLongerThanText();
        testOverlappingMatches();
        testLPS();
        testFullMatch();
        testMultipleOccurrences();
        testComplexPattern();
        testMain();
        System.out.println("All tests passed!");
    }
}
