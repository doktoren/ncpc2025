/*
Suffix Array construction with Longest Common Prefix (LCP) array using Kasai's algorithm.

A suffix array is a sorted array of all suffixes of a string. The LCP array stores the length
of the longest common prefix between consecutive suffixes in the suffix array.

Key operations:
- Constructor: Build suffix array and LCP array for a string
- findPattern(pattern): Find all occurrences of pattern in text

Time complexity: O(n log n) for suffix array, O(n) for LCP array
Space complexity: O(n)
*/

import java.util.*;

class suffix_array {
    static class SuffixArray {
        private String text;
        private int n;
        private int[] sa;
        private int[] lcp;

        SuffixArray(String text) {
            this.text = text;
            this.n = text.length();
            this.sa = buildSuffixArray();
            this.lcp = buildLCPArray();
        }

        private int[] buildSuffixArray() {
            Integer[] suffixes = new Integer[n];
            for (int i = 0; i < n; i++) {
                suffixes[i] = i;
            }
            Arrays.sort(suffixes, (a, b) -> text.substring(a).compareTo(text.substring(b)));

            int[] result = new int[n];
            for (int i = 0; i < n; i++) {
                result[i] = suffixes[i];
            }
            return result;
        }

        private int[] buildLCPArray() {
            if (n == 0) return new int[0];

            int[] rank = new int[n];
            for (int i = 0; i < n; i++) {
                rank[sa[i]] = i;
            }

            int[] lcp = new int[n];
            int h = 0;

            for (int i = 0; i < n; i++) {
                if (rank[i] > 0) {
                    int j = sa[rank[i] - 1];
                    while (i + h < n && j + h < n && text.charAt(i + h) == text.charAt(j + h)) {
                        h++;
                    }
                    lcp[rank[i]] = h;
                    if (h > 0) h--;
                }
            }

            return lcp;
        }

        List<Integer> findPattern(String pattern) {
            if (pattern.isEmpty()) return new ArrayList<>();

            int m = pattern.length();
            int left = 0, right = n;

            while (left < right) {
                int mid = (left + right) / 2;
                String suffix = text.substring(sa[mid]);
                if (suffix.compareTo(pattern) < 0) {
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
                String suffix = text.substring(sa[mid], Math.min(sa[mid] + m, n));
                if (suffix.compareTo(pattern) <= 0) {
                    left = mid + 1;
                } else {
                    right = mid;
                }
            }

            int end = left;

            List<Integer> result = new ArrayList<>();
            for (int i = start; i < end; i++) {
                if (sa[i] + m <= n && text.substring(sa[i], sa[i] + m).equals(pattern)) {
                    result.add(sa[i]);
                }
            }

            Collections.sort(result);
            return result;
        }

        int[] getSA() {
            return sa;
        }

        int[] getLCP() {
            return lcp;
        }
    }

    static void testMain() {
        SuffixArray sa = new SuffixArray("banana");
        assert Arrays.equals(sa.getSA(), new int[] {5, 3, 1, 0, 4, 2});
        assert Arrays.equals(sa.getLCP(), new int[] {0, 1, 3, 0, 0, 2});

        List<Integer> positions = sa.findPattern("ana");
        assert positions.equals(Arrays.asList(1, 3));
    }

    // Don't write tests below during competition.

    static void testEmptyString() {
        SuffixArray sa = new SuffixArray("");
        assert sa.getSA().length == 0;
        assert sa.getLCP().length == 0;
        assert sa.findPattern("a").isEmpty();
    }

    static void testSingleChar() {
        SuffixArray sa = new SuffixArray("a");
        assert sa.getSA().length == 1;
        assert sa.getSA()[0] == 0;
    }

    static void testRepeatedChars() {
        SuffixArray sa = new SuffixArray("aaaa");
        assert Arrays.equals(sa.getSA(), new int[] {3, 2, 1, 0});
        assert Arrays.equals(sa.getLCP(), new int[] {0, 1, 2, 3});
    }

    static void testPatternNotFound() {
        SuffixArray sa = new SuffixArray("hello");
        assert sa.findPattern("world").isEmpty();
    }

    static void testPatternAtEnd() {
        SuffixArray sa = new SuffixArray("hello");
        assert sa.findPattern("lo").equals(Arrays.asList(3));
    }

    static void testOverlappingPatterns() {
        SuffixArray sa = new SuffixArray("aabaabaa");
        List<Integer> positions = sa.findPattern("aa");
        Collections.sort(positions);
        assert positions.equals(Arrays.asList(0, 3, 6));
    }

    static void testEntireString() {
        String text = "programming";
        SuffixArray sa = new SuffixArray(text);
        assert sa.findPattern(text).equals(Arrays.asList(0));
    }

    static void testLCPCalculation() {
        SuffixArray sa = new SuffixArray("abcab");
        assert Arrays.equals(sa.getSA(), new int[] {3, 0, 4, 1, 2});
        assert sa.getLCP()[0] == 0;
        assert sa.getLCP()[1] == 2;
        assert sa.getLCP()[2] == 0;
        assert sa.getLCP()[3] == 1;
        assert sa.getLCP()[4] == 0;
    }

    static void testAllUniqueChars() {
        SuffixArray sa = new SuffixArray("abcd");
        assert Arrays.equals(sa.getSA(), new int[] {0, 1, 2, 3});
        assert Arrays.equals(sa.getLCP(), new int[] {0, 0, 0, 0});
    }

    static void testPalindrome() {
        SuffixArray sa = new SuffixArray("racecar");
        List<Integer> positions = sa.findPattern("r");
        Collections.sort(positions);
        assert positions.equals(Arrays.asList(0, 6));
    }

    static void testLongPattern() {
        String text = "thequickbrownfoxjumpsoverthelazydog";
        SuffixArray sa = new SuffixArray(text);
        assert sa.findPattern("jumps").equals(Arrays.asList(16));
        List<Integer> thePos = sa.findPattern("the");
        Collections.sort(thePos);
        assert thePos.equals(Arrays.asList(0, 25));
    }

    public static void main(String[] args) {
        testMain();
        testEmptyString();
        testSingleChar();
        testRepeatedChars();
        testPatternNotFound();
        testPatternAtEnd();
        testOverlappingPatterns();
        testEntireString();
        testLCPCalculation();
        testAllUniqueChars();
        testPalindrome();
        testLongPattern();
        System.out.println("All tests passed!");
    }
}
