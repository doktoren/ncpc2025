"""
Sprague-Grundy theorem implementation for impartial games (finite, acyclic, normal-play).

The Sprague-Grundy theorem states that every impartial game is equivalent to a Nim heap
of size equal to its Grundy number (nimber). For multiple independent games,
XOR the Grundy numbers to determine the combined game value.

API:
- GrundyEngine(get_valid_moves): makes it easy to plug in any game.
- grundy(state): compute nimber for a state (must be hashable).
- grundy_multi(states): XOR of nimbers for independent subgames.
- is_winning_position(states): True iff XOR != 0.

Includes implementations for:
- Nim (single heap).
- Subtraction game (allowed moves = {1,3,4}) with period detection.
- Kayles (bowling pins) with splits into subgames via tuple representation.

Requirements:
- State must be hashable and canonically represented (e.g., tuple/sorted tuple).
- get_valid_moves(state) must not create cycles.
"""

# Don't use annotations during contest
from __future__ import annotations

from functools import lru_cache
from typing import Callable, Hashable, Iterable, Final


State = Hashable
MovesFn = Callable[[State], Iterable[State]]


def mex(values: Iterable[int]) -> int:
    """Minimum EXcludant: smallest non-negative integer not occurring in 'values'."""
    s = set(values)
    g = 0
    while g in s:
        g += 1
    return g


class GrundyEngine:
    """Wrapper that binds a move function and provides grundy(), XOR operations, etc."""
    def __init__(self, get_valid_moves: MovesFn) -> None:
        self._moves: Final = get_valid_moves

        @lru_cache(maxsize=None)
        def _grundy_cached(state: State) -> int:
            nxt = tuple(self._moves(state))
            if not nxt:
                return 0
            return mex(_grundy_cached(s) for s in nxt)

        self._grundy_cached = _grundy_cached

    def grundy(self, state: State) -> int:
        return self._grundy_cached(state)

    def grundy_multi(self, states: Iterable[State]) -> int:
        g = 0
        for s in states:
            g ^= self._grundy_cached(s)
        return g

    def is_winning_position(self, states: Iterable[State]) -> bool:
        return self.grundy_multi(states) != 0


# Optional functionality (not always needed during competition)

def detect_period(seq: list[int], min_period: int = 1, max_period: int | None = None) -> int | None:
    """Find smallest period p such that seq repeats (completely) with period p."""
    n = len(seq)
    if max_period is None:
        max_period = n // 2
    for p in range(min_period, max_period + 1):
        ok = True
        for i in range(n):
            if seq[i] != seq[i % p]:
                ok = False
                break
        if ok:
            return p
    return None


def nim_moves_single_heap(n: int) -> Iterable[int]:
    """Nim: single heap. Move: take 1..n stones."""
    for k in range(n):
        yield k  # leave 0..n-1


def subtraction_game_moves_factory(allowed: set[int]) -> MovesFn:
    """Subtraction game: state = int; allowed moves = move sizes in 'allowed'."""
    allowed_sorted = tuple(sorted(allowed))
    def moves(n: int) -> Iterable[int]:
        for d in allowed_sorted:
            if d <= n:
                yield n - d
    return moves


def kayles_moves(segments: tuple[int, ...]) -> Iterable[tuple[int, ...]]:
    """
    Kayles (bowling pins):
    State: sorted tuple of segment lengths. A move removes 1 pin or 2 adjacent pins in one segment,
    thus splitting it into up to two new segments. Return new canonical (sorted) state.
    """
    res: set[tuple[int, ...]] = set()
    for idx, n in enumerate(segments):
        if n <= 0:
            continue

        # Remove one pin at position i (0..n-1)
        for i in range(n):
            left = i
            right = n - i - 1
            new_seg = [*segments[:idx]]
            if left > 0:
                new_seg.append(left)
            if right > 0:
                new_seg.append(right)
            new_seg.extend(segments[idx + 1 :])
            res.add(tuple(sorted(new_seg)))

        # Remove two adjacent pins at position i,i+1 (0..n-2)
        for i in range(n - 1):
            left = i
            right = n - i - 2
            new_seg = [*segments[:idx]]
            if left > 0:
                new_seg.append(left)
            if right > 0:
                new_seg.append(right)
            new_seg.extend(segments[idx + 1 :])
            res.add(tuple(sorted(new_seg)))

    return res


def test_main() -> None:
    # Test Nim with larger values
    eng = GrundyEngine(nim_moves_single_heap)
    assert eng.grundy(42) == 42
    assert eng.grundy_multi([17, 23, 31]) == 25  # 17^23^31 = 25
    assert eng.is_winning_position([15, 27, 36]) is True  # 15^27^36 = 48 != 0

    # Test subtraction game {1,3,4} with period 7
    eng2 = GrundyEngine(subtraction_game_moves_factory({1, 3, 4}))
    assert eng2.grundy(14) == 0  # 14 % 7 = 0 → grundy = 0
    assert eng2.grundy(15) == 1  # 15 % 7 = 1 → grundy = 1
    assert eng2.grundy(18) == 2  # 18 % 7 = 4 → grundy = 2

    # Test Kayles
    eng3 = GrundyEngine(kayles_moves)
    assert eng3.grundy((7,)) == 2  # K(7) = 2
    assert eng3.grundy((3, 5)) == 7  # K(3)^K(5) = 3^4 = 7


# Don't write tests below during competition.


def test_nim_extended() -> None:
    eng = GrundyEngine(nim_moves_single_heap)
    # Known: grundy(n) = n for all n in Nim
    for n in range(0, 64):
        assert eng.grundy(n) == n


def test_subtraction_game_period() -> None:
    # Allowed moves = {1,3,4}. Classic periodic sequence.
    moves = subtraction_game_moves_factory({1, 3, 4})
    eng = GrundyEngine(moves)

    seq = [eng.grundy(n) for n in range(0, 200)]
    # For {1,3,4} the period is 7: [0,1,0,1,2,3,2] ...
    p = detect_period(seq, min_period=1, max_period=50)
    assert p == 7

    base = seq[:p]
    # Check repetition
    for i, g in enumerate(seq):
        assert g == base[i % p]

    # Winning N: those with grundy(n) != 0
    wins = [n for n, g in enumerate(seq[:30]) if g != 0]
    assert wins[:10] == [1, 3, 4, 5, 6, 8, 10, 11, 12, 13]


def test_sum_of_independent_subgames() -> None:
    # Same subtraction game. Combined position = multiple independent heaps (ints).
    eng = GrundyEngine(subtraction_game_moves_factory({1, 3, 4}))

    # Build some positions
    A = [5, 7]   # grundy(5)=3, grundy(7)=2 → XOR=1 → winning
    B = [8, 9]   # Let's compute what g(8) and g(9) are:
    GA = eng.grundy_multi(A)
    GB = eng.grundy_multi(B)
    assert GA != 0
    assert GB == (eng.grundy(8) ^ eng.grundy(9))
    assert eng.is_winning_position(A) is True
    assert eng.is_winning_position(B) == (GB != 0)


def test_kayles_small() -> None:
    eng = GrundyEngine(kayles_moves)

    # Known first values for K(n) (reasonably small n)
    # Not all precisely known by heart, but we validate consistency/monotone checks.
    vals = [eng.grundy((n,)) for n in range(0, 15)]
    # Not trivial pattern; we check a few hand-picked facts (from direct computation):
    assert vals[:10] == [0, 1, 2, 3, 1, 4, 3, 2, 1, 4]
    # Splits: (n,) can end in (a,b) → XOR rule implicit in recursion.
    # Extra sanity: composite segments
    assert eng.grundy((2, 2)) == (eng.grundy((2,)) ^ eng.grundy((2,)))


def test_long_application_scan() -> None:
    """
    Typical competition application:
    - Given a parameter N, derive for which N the position is winning.
    - Use period if it exists.
    Here we use subtraction game {1,3,4}.
    """
    eng = GrundyEngine(subtraction_game_moves_factory({1, 3, 4}))
    N = 500
    seq = [eng.grundy(n) for n in range(N + 1)]
    period = detect_period(seq, min_period=1, max_period=100)
    assert period == 7

    # Winning N up to 60:
    winning_N = [n for n in range(61) if seq[n] != 0]
    # Spot-check the first few values
    assert winning_N[:12] == [1, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 17]


def test_cycle_guard_note() -> None:
    """
    Theory requirement: no cycles. This test is 'meta' and documents the assumption.
    We do NOT build a cyclic moves function here; we just note the requirement.
    """
    assert True


def test() -> None:
    test_nim_extended()
    test_subtraction_game_period()
    test_sum_of_independent_subgames()
    test_kayles_small()
    test_long_application_scan()
    test_cycle_guard_note()


def main() -> None:
    test_main()
    test()
    print("All Sprague–Grundy tests passed!")


if __name__ == "__main__":
    main()
