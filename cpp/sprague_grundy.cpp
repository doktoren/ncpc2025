/*
Sprague-Grundy theorem implementation for impartial games (finite, acyclic, normal-play).

The Sprague-Grundy theorem states that every impartial game is equivalent to a Nim heap
of size equal to its Grundy number (nimber). For multiple independent games,
XOR the Grundy numbers to determine the combined game value.

API:
- GrundyEngine(moveFunction): makes it easy to plug in any game.
- grundy(state): compute nimber for a state (must be hashable).
- grundy_multi(states): XOR of nimbers for independent subgames.
- is_winning_position(states): true iff XOR != 0.

Includes implementations for:
- Nim (single heap).
- Subtraction game (allowed moves = {1,3,4}) with period detection.
- Kayles (bowling pins) with splits into subgames via vector representation.

Requirements:
- State must be hashable and canonically represented (e.g., sorted vectors).
- moveFunction must not create cycles.
*/

#include <algorithm>
#include <cassert>
#include <functional>
#include <iostream>
#include <map>
#include <optional>
#include <set>
#include <vector>

// Minimum EXcludant: smallest non-negative integer not occurring in 'values'
int mex(const std::vector<int>& values) {
    std::set<int> s(values.begin(), values.end());
    int g = 0;
    while (s.count(g)) { g++; }
    return g;
}

template <typename T>
class GrundyEngine {
  private:
    std::function<std::vector<T>(const T&)> moves;
    mutable std::map<T, int> cache;

  public:
    GrundyEngine(std::function<std::vector<T>(const T&)> move_function) : moves(move_function) {}

    int grundy(const T& state) const {
        if (cache.count(state)) { return cache[state]; }

        std::vector<T> next_states = moves(state);
        if (next_states.empty()) {
            cache[state] = 0;
            return 0;
        }

        std::vector<int> nimbers;
        for (const auto& next_state : next_states) { nimbers.push_back(grundy(next_state)); }

        int result = mex(nimbers);
        cache[state] = result;
        return result;
    }

    int grundy_multi(const std::vector<T>& states) const {
        int result = 0;
        for (const auto& state : states) { result ^= grundy(state); }
        return result;
    }

    bool is_winning_position(const std::vector<T>& states) const {
        return grundy_multi(states) != 0;
    }
};

// Optional functionality (not always needed during competition)

std::optional<int> detect_period(const std::vector<int>& seq, int min_period = 1,
                                 std::optional<int> max_period = std::nullopt) {
    int n = seq.size();
    if (!max_period) { max_period = n / 2; }

    for (int p = min_period; p <= *max_period; p++) {
        bool ok = true;
        for (int i = 0; i < n; i++) {
            if (seq[i] != seq[i % p]) {
                ok = false;
                break;
            }
        }
        if (ok) { return p; }
    }
    return std::nullopt;
}

std::vector<int> nim_moves_single_heap(int n) {
    std::vector<int> moves;
    for (int k = 0; k < n; k++) {
        moves.push_back(k);  // leave 0..n-1
    }
    return moves;
}

std::function<std::vector<int>(int)> subtraction_game_moves_factory(const std::set<int>& allowed) {
    std::vector<int> allowed_sorted(allowed.begin(), allowed.end());

    return [allowed_sorted](int n) -> std::vector<int> {
        std::vector<int> moves;
        for (int d : allowed_sorted) {
            if (d <= n) { moves.push_back(n - d); }
        }
        return moves;
    };
}

std::vector<std::vector<int>> kayles_moves(const std::vector<int>& segments) {
    std::set<std::vector<int>> result_set;

    for (size_t idx = 0; idx < segments.size(); idx++) {
        int n = segments[idx];
        if (n <= 0) continue;

        // Remove one pin at position i (0..n-1)
        for (int i = 0; i < n; i++) {
            int left = i;
            int right = n - i - 1;
            std::vector<int> new_seg;

            for (size_t j = 0; j < idx; j++) { new_seg.push_back(segments[j]); }
            if (left > 0) new_seg.push_back(left);
            if (right > 0) new_seg.push_back(right);
            for (size_t j = idx + 1; j < segments.size(); j++) { new_seg.push_back(segments[j]); }

            std::sort(new_seg.begin(), new_seg.end());
            result_set.insert(new_seg);
        }

        // Remove two adjacent pins at position i,i+1 (0..n-2)
        for (int i = 0; i < n - 1; i++) {
            int left = i;
            int right = n - i - 2;
            std::vector<int> new_seg;

            for (size_t j = 0; j < idx; j++) { new_seg.push_back(segments[j]); }
            if (left > 0) new_seg.push_back(left);
            if (right > 0) new_seg.push_back(right);
            for (size_t j = idx + 1; j < segments.size(); j++) { new_seg.push_back(segments[j]); }

            std::sort(new_seg.begin(), new_seg.end());
            result_set.insert(new_seg);
        }
    }

    return std::vector<std::vector<int>>(result_set.begin(), result_set.end());
}

void test_main() {
    // Test Nim with larger values
    GrundyEngine<int> eng(nim_moves_single_heap);
    assert(eng.grundy(42) == 42);
    assert(eng.grundy_multi({17, 23, 31}) == 25);           // 17^23^31 = 25
    assert(eng.is_winning_position({15, 27, 36}) == true);  // 15^27^36 = 48 != 0

    // Test subtraction game {1,3,4} with period 7
    auto moves2 = subtraction_game_moves_factory({1, 3, 4});
    GrundyEngine<int> eng2(moves2);
    assert(eng2.grundy(14) == 0);  // 14 % 7 = 0 → grundy = 0
    assert(eng2.grundy(15) == 1);  // 15 % 7 = 1 → grundy = 1
    assert(eng2.grundy(18) == 2);  // 18 % 7 = 4 → grundy = 2

    // Test Kayles
    GrundyEngine<std::vector<int>> eng3(kayles_moves);
    assert(eng3.grundy({7}) == 2);     // K(7) = 2
    assert(eng3.grundy({3, 5}) == 7);  // K(3)^K(5) = 3^4 = 7
}

// Don't write tests below during competition.

void test_nim_extended() {
    GrundyEngine<int> eng(nim_moves_single_heap);
    // Known: grundy(n) = n for all n in Nim
    for (int n = 0; n < 64; n++) { assert(eng.grundy(n) == n); }
}

void test_subtraction_game_period() {
    // Allowed moves = {1,3,4}. Classic periodic sequence.
    auto moves = subtraction_game_moves_factory({1, 3, 4});
    GrundyEngine<int> eng(moves);

    std::vector<int> seq;
    for (int n = 0; n < 200; n++) { seq.push_back(eng.grundy(n)); }

    // For {1,3,4} the period is 7: [0,1,0,1,2,3,2] ...
    auto p = detect_period(seq, 1, 50);
    assert(p && *p == 7);

    std::vector<int> base(seq.begin(), seq.begin() + *p);
    // Check repetition
    for (size_t i = 0; i < seq.size(); i++) { assert(seq[i] == base[i % *p]); }

    // Winning N: those with grundy(n) != 0
    std::vector<int> wins;
    for (int n = 0; n < 30; n++) {
        if (seq[n] != 0) { wins.push_back(n); }
    }
    std::vector<int> expected = {1, 3, 4, 5, 6, 8, 10, 11, 12, 13};
    assert(std::equal(wins.begin(), wins.begin() + 10, expected.begin()));
}

void test_sum_of_independent_subgames() {
    // Same subtraction game. Combined position = multiple independent heaps (ints).
    auto moves = subtraction_game_moves_factory({1, 3, 4});
    GrundyEngine<int> eng(moves);

    // Build some positions
    std::vector<int> A = {5, 7};  // grundy(5)=3, grundy(7)=2 → XOR=1 → winning
    std::vector<int> B = {8, 9};  // Let's compute what g(8) and g(9) are:
    int GA = eng.grundy_multi(A);
    int GB = eng.grundy_multi(B);
    assert(GA != 0);
    assert(GB == (eng.grundy(8) ^ eng.grundy(9)));
    assert(eng.is_winning_position(A) == true);
    assert(eng.is_winning_position(B) == (GB != 0));
}

void test_kayles_small() {
    GrundyEngine<std::vector<int>> eng(kayles_moves);

    // Known first values for K(n) (reasonably small n)
    std::vector<int> vals;
    for (int n = 0; n < 15; n++) { vals.push_back(eng.grundy({n})); }

    // Not trivial pattern; we check a few hand-picked facts (from direct computation):
    std::vector<int> expected = {0, 1, 2, 3, 1, 4, 3, 2, 1, 4};
    assert(std::equal(vals.begin(), vals.begin() + 10, expected.begin()));

    // Splits: (n,) can end in (a,b) → XOR rule implicit in recursion.
    // Extra sanity: composite segments
    assert(eng.grundy({2, 2}) == (eng.grundy({2}) ^ eng.grundy({2})));
}

void test_long_application_scan() {
    /*
    Typical competition application:
    - Given a parameter N, derive for which N the position is winning.
    - Use period if it exists.
    Here we use subtraction game {1,3,4}.
    */
    auto moves = subtraction_game_moves_factory({1, 3, 4});
    GrundyEngine<int> eng(moves);
    int N = 500;
    std::vector<int> seq;
    for (int n = 0; n <= N; n++) { seq.push_back(eng.grundy(n)); }

    auto period = detect_period(seq, 1, 100);
    assert(period && *period == 7);

    // Winning N up to 60:
    std::vector<int> winning_N;
    for (int n = 0; n <= 60; n++) {
        if (seq[n] != 0) { winning_N.push_back(n); }
    }

    // Spot-check the first few values
    std::vector<int> expected = {1, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 17};
    assert(std::equal(winning_N.begin(), winning_N.begin() + 12, expected.begin()));
}

void test_cycle_guard_note() {
    /*
    Theory requirement: no cycles. This test is 'meta' and documents the assumption.
    We do NOT build a cyclic moves function here; we just note the requirement.
    */
    assert(true);
}

void test() {
    test_nim_extended();
    test_subtraction_game_period();
    test_sum_of_independent_subgames();
    test_kayles_small();
    test_long_application_scan();
    test_cycle_guard_note();
}

int main() {
    test_main();
    test();
    std::cout << "All Sprague–Grundy tests passed!" << std::endl;
    return 0;
}