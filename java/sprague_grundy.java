/*
Sprague-Grundy theorem implementation for impartial games (finite, acyclic, normal-play).

The Sprague-Grundy theorem states that every impartial game is equivalent to a Nim heap
of size equal to its Grundy number (nimber). For multiple independent games,
XOR the Grundy numbers to determine the combined game value.

API:
- GrundyEngine(moveFunction): makes it easy to plug in any game.
- grundy(state): compute nimber for a state (must be hashable).
- grundyMulti(states): XOR of nimbers for independent subgames.
- isWinningPosition(states): true iff XOR != 0.

Includes implementations for:
- Nim (single heap).
- Subtraction game (allowed moves = {1,3,4}) with period detection.
- Kayles (bowling pins) with splits into subgames via array representation.

Requirements:
- State must be hashable and canonically represented (e.g., sorted arrays).
- moveFunction must not create cycles.
*/

import java.util.*;
import java.util.function.Function;

public class sprague_grundy {

    // Minimum EXcludant: smallest non-negative integer not occurring in 'values'
    public static int mex(Collection<Integer> values) {
        Set<Integer> s = new HashSet<>(values);
        int g = 0;
        while (s.contains(g)) {
            g++;
        }
        return g;
    }

    public static class GrundyEngine<T> {
        protected final Function<T, Collection<T>> moves;
        private final Map<T, Integer> cache = new HashMap<>();

        public GrundyEngine(Function<T, Collection<T>> moveFunction) {
            this.moves = moveFunction;
        }

        public int grundy(T state) {
            if (cache.containsKey(state)) {
                return cache.get(state);
            }

            Collection<T> nextStates = moves.apply(state);
            if (nextStates.isEmpty()) {
                cache.put(state, 0);
                return 0;
            }

            List<Integer> nimbers = new ArrayList<>();
            for (T nextState : nextStates) {
                nimbers.add(grundy(nextState));
            }

            int result = mex(nimbers);
            cache.put(state, result);
            return result;
        }

        public int grundyMulti(Collection<T> states) {
            int result = 0;
            for (T state : states) {
                result ^= grundy(state);
            }
            return result;
        }

        public boolean isWinningPosition(Collection<T> states) {
            return grundyMulti(states) != 0;
        }
    }

    // Wrapper class for Kayles segments with proper equals/hashCode
    public static class KaylesState {
        private final int[] segments;
        private final int hashCode;

        public KaylesState(int[] segments) {
            this.segments = segments.clone();
            Arrays.sort(this.segments); // Ensure canonical form
            this.hashCode = Arrays.hashCode(this.segments);
        }

        public KaylesState(List<Integer> segments) {
            this(segments.stream().mapToInt(Integer::intValue).toArray());
        }

        public int[] getSegments() {
            return segments.clone();
        }

        @Override
        public boolean equals(Object obj) {
            if (this == obj) return true;
            if (obj == null || getClass() != obj.getClass()) return false;
            KaylesState that = (KaylesState) obj;
            return Arrays.equals(segments, that.segments);
        }

        @Override
        public int hashCode() {
            return hashCode;
        }

        @Override
        public String toString() {
            return Arrays.toString(segments);
        }
    }

    // Optional functionality (not always needed during competition)

    public static Integer detectPeriod(List<Integer> seq, int minPeriod, Integer maxPeriod) {
        int n = seq.size();
        if (maxPeriod == null) {
            maxPeriod = n / 2;
        }
        for (int p = minPeriod; p <= maxPeriod; p++) {
            boolean ok = true;
            for (int i = 0; i < n; i++) {
                if (!seq.get(i).equals(seq.get(i % p))) {
                    ok = false;
                    break;
                }
            }
            if (ok) {
                return p;
            }
        }
        return null;
    }

    public static Collection<Integer> nimMovesSingleHeap(int n) {
        List<Integer> moves = new ArrayList<>();
        for (int k = 0; k < n; k++) {
            moves.add(k); // leave 0..n-1
        }
        return moves;
    }

    public static Function<Integer, Collection<Integer>> subtractionGameMovesFactory(
            Set<Integer> allowed) {
        List<Integer> allowedSorted = new ArrayList<>(allowed);
        Collections.sort(allowedSorted);

        return n -> {
            List<Integer> moves = new ArrayList<>();
            for (int d : allowedSorted) {
                if (d <= n) {
                    moves.add(n - d);
                }
            }
            return moves;
        };
    }

    public static Collection<KaylesState> kaylesMovesHelper(KaylesState state) {
        Set<KaylesState> resultSet = new HashSet<>();
        int[] segments = state.getSegments();

        for (int idx = 0; idx < segments.length; idx++) {
            int n = segments[idx];
            if (n <= 0) continue;

            // Remove one pin at position i (0..n-1)
            for (int i = 0; i < n; i++) {
                int left = i;
                int right = n - i - 1;
                List<Integer> newSeg = new ArrayList<>();

                for (int j = 0; j < idx; j++) {
                    newSeg.add(segments[j]);
                }
                if (left > 0) newSeg.add(left);
                if (right > 0) newSeg.add(right);
                for (int j = idx + 1; j < segments.length; j++) {
                    newSeg.add(segments[j]);
                }

                resultSet.add(new KaylesState(newSeg));
            }

            // Remove two adjacent pins at position i,i+1 (0..n-2)
            for (int i = 0; i < n - 1; i++) {
                int left = i;
                int right = n - i - 2;
                List<Integer> newSeg = new ArrayList<>();

                for (int j = 0; j < idx; j++) {
                    newSeg.add(segments[j]);
                }
                if (left > 0) newSeg.add(left);
                if (right > 0) newSeg.add(right);
                for (int j = idx + 1; j < segments.length; j++) {
                    newSeg.add(segments[j]);
                }

                resultSet.add(new KaylesState(newSeg));
            }
        }

        return new ArrayList<>(resultSet);
    }

    public static Function<KaylesState, Collection<KaylesState>> kaylesMovesFactory() {
        return sprague_grundy::kaylesMovesHelper;
    }

    public static void testMain() {
        // Test Nim with larger values
        GrundyEngine<Integer> eng = new GrundyEngine<>(sprague_grundy::nimMovesSingleHeap);
        assert eng.grundy(42) == 42;
        assert eng.grundyMulti(Arrays.asList(17, 23, 31)) == 25; // 17^23^31 = 25
        assert eng.isWinningPosition(Arrays.asList(15, 27, 36)) == true; // 15^27^36 = 48 != 0

        // Test subtraction game {1,3,4} with period 7
        GrundyEngine<Integer> eng2 =
                new GrundyEngine<>(subtractionGameMovesFactory(Set.of(1, 3, 4)));
        assert eng2.grundy(14) == 0; // 14 % 7 = 0 → grundy = 0
        assert eng2.grundy(15) == 1; // 15 % 7 = 1 → grundy = 1
        assert eng2.grundy(18) == 2; // 18 % 7 = 4 → grundy = 2

        // Test Kayles
        GrundyEngine<KaylesState> eng3 = new GrundyEngine<>(kaylesMovesFactory());
        assert eng3.grundy(new KaylesState(new int[] {7})) == 2; // K(7) = 2
        assert eng3.grundy(new KaylesState(new int[] {3, 5})) == 7; // K(3)^K(5) = 3^4 = 7
    }

    // Don't write tests below during competition.

    public static void testNimExtended() {
        GrundyEngine<Integer> eng = new GrundyEngine<>(sprague_grundy::nimMovesSingleHeap);
        // Known: grundy(n) = n for all n in Nim
        for (int n = 0; n < 64; n++) {
            assert eng.grundy(n) == n;
        }
    }

    public static void testSubtractionGamePeriod() {
        // Allowed moves = {1,3,4}. Classic periodic sequence.
        GrundyEngine<Integer> eng =
                new GrundyEngine<>(subtractionGameMovesFactory(Set.of(1, 3, 4)));

        List<Integer> seq = new ArrayList<>();
        for (int n = 0; n < 200; n++) {
            seq.add(eng.grundy(n));
        }

        // For {1,3,4} the period is 7: [0,1,0,1,2,3,2] ...
        Integer p = detectPeriod(seq, 1, 50);
        assert p != null && p == 7;

        List<Integer> base = seq.subList(0, p);
        // Check repetition
        for (int i = 0; i < seq.size(); i++) {
            assert seq.get(i).equals(base.get(i % p));
        }

        // Winning N: those with grundy(n) != 0
        List<Integer> wins = new ArrayList<>();
        for (int n = 0; n < 30; n++) {
            if (seq.get(n) != 0) {
                wins.add(n);
            }
        }
        List<Integer> expected = Arrays.asList(1, 3, 4, 5, 6, 8, 10, 11, 12, 13);
        assert wins.subList(0, 10).equals(expected);
    }

    public static void testSumOfIndependentSubgames() {
        // Same subtraction game. Combined position = multiple independent heaps (ints).
        GrundyEngine<Integer> eng =
                new GrundyEngine<>(subtractionGameMovesFactory(Set.of(1, 3, 4)));

        // Build some positions
        List<Integer> A = Arrays.asList(5, 7); // grundy(5)=3, grundy(7)=2 → XOR=1 → winning
        List<Integer> B = Arrays.asList(8, 9); // Let's compute what g(8) and g(9) are:
        int GA = eng.grundyMulti(A);
        int GB = eng.grundyMulti(B);
        assert GA != 0;
        assert GB == (eng.grundy(8) ^ eng.grundy(9));
        assert eng.isWinningPosition(A) == true;
        assert eng.isWinningPosition(B) == (GB != 0);
    }

    public static void testKaylesSmall() {
        GrundyEngine<KaylesState> eng = new GrundyEngine<>(kaylesMovesFactory());

        // Known first values for K(n) (reasonably small n)
        List<Integer> vals = new ArrayList<>();
        for (int n = 0; n < 15; n++) {
            vals.add(eng.grundy(new KaylesState(new int[] {n})));
        }

        // Not trivial pattern; we check a few hand-picked facts (from direct computation):
        List<Integer> expected = Arrays.asList(0, 1, 2, 3, 1, 4, 3, 2, 1, 4);
        assert vals.subList(0, 10).equals(expected);

        // Splits: (n,) can end in (a,b) → XOR rule implicit in recursion.
        // Extra sanity: composite segments
        assert eng.grundy(new KaylesState(new int[] {2, 2}))
                == (eng.grundy(new KaylesState(new int[] {2}))
                        ^ eng.grundy(new KaylesState(new int[] {2})));
    }

    public static void testLongApplicationScan() {
        /*
        Typical competition application:
        - Given a parameter N, derive for which N the position is winning.
        - Use period if it exists.
        Here we use subtraction game {1,3,4}.
        */
        GrundyEngine<Integer> eng =
                new GrundyEngine<>(subtractionGameMovesFactory(Set.of(1, 3, 4)));
        int N = 500;
        List<Integer> seq = new ArrayList<>();
        for (int n = 0; n <= N; n++) {
            seq.add(eng.grundy(n));
        }

        Integer period = detectPeriod(seq, 1, 100);
        assert period != null && period == 7;

        // Winning N up to 60:
        List<Integer> winningN = new ArrayList<>();
        for (int n = 0; n <= 60; n++) {
            if (seq.get(n) != 0) {
                winningN.add(n);
            }
        }

        // Spot-check the first few values
        List<Integer> expected = Arrays.asList(1, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 17);
        assert winningN.subList(0, 12).equals(expected);
    }

    public static void testCycleGuardNote() {
        /*
        Theory requirement: no cycles. This test is 'meta' and documents the assumption.
        We do NOT build a cyclic moves function here; we just note the requirement.
        */
        assert true;
    }

    public static void test() {
        testNimExtended();
        testSubtractionGamePeriod();
        testSumOfIndependentSubgames();
        testKaylesSmall();
        testLongApplicationScan();
        testCycleGuardNote();
    }

    public static void main(String[] args) {
        testMain();
        test();
        System.out.println("All Sprague–Grundy tests passed!");
    }
}
