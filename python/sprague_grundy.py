"""
Sprague-Grundy reference (impartial, finite, acyclic, normal-play).

API:
- GrundyEngine(get_valid_moves): gør det let at plugge et spil på.
- grundy(state): nimber for en state (hashable).
- grundy_multi(states): XOR af nimbers for uafhængige delspil.
- is_winning_position(states): True iff XOR != 0.

Inkluderer:
- Nim (én bunke).
- Subtraction game (tilladte træk = {1,3,4}) med periode-detektion.
- Kayles (bowlingpins) m. split til delspil via tuple-repræsentation.

Krav:
- State skal være hashable og kanonisk repræsenteret (fx tuple/sorteret tuple).
- get_valid_moves(state) må ikke skabe cykler.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Callable, Hashable, Iterable, Final


State = Hashable
MovesFn = Callable[[State], Iterable[State]]


def mex(values: Iterable[int]) -> int:
    """Minimum EXcludant: mindste ikke-negative heltal, der ikke forekommer i 'values'."""
    s = set(values)
    g = 0
    while g in s:
        g += 1
    return g


class GrundyEngine:
    """Wrapper der binder en move-funktion og leverer grundy(), XOR osv."""
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


# -----------------------------
# Hjælpefunktioner til tests
# -----------------------------

def detect_period(seq: list[int], min_period: int = 1, max_period: int | None = None) -> int | None:
    """Find mindste periode p, så seq gentager sig (helt) med periode p."""
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


# -----------------------------
# Spil-definitioner (bruges i tests)
# -----------------------------

def nim_moves_single_heap(n: int) -> Iterable[int]:
    """Nim: én bunke. Træk: tag 1..n sten."""
    for k in range(n):
        yield k  # efterlad 0..n-1


def subtraction_game_moves_factory(allowed: set[int]) -> MovesFn:
    """Subtraction game: state = int; tilladte træk = trækstørrelser i 'allowed'."""
    allowed_sorted = tuple(sorted(allowed))
    def moves(n: int) -> Iterable[int]:
        for d in allowed_sorted:
            if d <= n:
                yield n - d
    return moves


def kayles_moves(segments: tuple[int, ...]) -> Iterable[tuple[int, ...]]:
    """
    Kayles (bowlingpins):
    State: sorteret tuple af segment-længder. Et træk fjerner 1 pin eller 2 nabo-pins i ét segment
    og splitter dermed i op til to nye segmenter. Returnér ny kanonisk (sorteret) state.
    """
    res: set[tuple[int, ...]] = set()
    for idx, n in enumerate(segments):
        if n <= 0:
            continue

        # Fjern én pin ved position i (0..n-1)
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

        # Fjern to nabo-pins ved position i,i+1 (0..n-2)
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


# -----------------------------
# Tests
# -----------------------------

def test_nim_basic() -> None:
    eng = GrundyEngine(nim_moves_single_heap)
    # Kendt: grundy(n) = n
    for n in range(0, 64):
        assert eng.grundy(n) == n

    # Multi-heap: XOR-regel
    assert eng.grundy_multi([3, 4, 5]) == (3 ^ 4 ^ 5)
    assert eng.is_winning_position([1, 2, 3]) is False  # 1^2^3 = 0
    assert eng.is_winning_position([1, 2, 4]) is True   # 1^2^4 != 0


def test_subtraction_game_period() -> None:
    # Tilladte træk = {1,3,4}. Klassisk periodisk sekvens.
    moves = subtraction_game_moves_factory({1, 3, 4})
    eng = GrundyEngine(moves)

    seq = [eng.grundy(n) for n in range(0, 200)]
    # For {1,3,4} er perioden 7: [0,1,0,1,2,3,2] ...
    p = detect_period(seq, min_period=1, max_period=50)
    assert p == 7

    base = seq[:p]
    # Tjek gentagelse
    for i, g in enumerate(seq):
        assert g == base[i % p]

    # Vindbare N: dem med grundy(n) != 0
    wins = [n for n, g in enumerate(seq[:30]) if g != 0]
    assert wins[:10] == [1, 3, 4, 5, 6, 8, 10, 11, 12, 13]


def test_sum_of_independent_subgames() -> None:
    # Samme subtraction game. Samlet stilling = flere uafhængige bunker (ints).
    eng = GrundyEngine(subtraction_game_moves_factory({1, 3, 4}))

    # Byg nogle stillinger
    A = [5, 7]   # grundy(5)=3, grundy(7)=2 → XOR=1 → winning
    B = [8, 9]   # g(8)=0? Lad os beregne:
    GA = eng.grundy_multi(A)
    GB = eng.grundy_multi(B)
    assert GA != 0
    assert GB == (eng.grundy(8) ^ eng.grundy(9))
    assert eng.is_winning_position(A) is True
    assert eng.is_winning_position(B) == (GB != 0)


def test_kayles_small() -> None:
    eng = GrundyEngine(kayles_moves)

    # Kendte første værdier for K(n) (rimelig små n)
    # Ikke alle præcis kendte i hovedet, men vi validerer konsistens/monotone checks.
    vals = [eng.grundy((n,)) for n in range(0, 15)]
    # Ikke trivielt mønster; vi checker et par håndplukkede facts (fra direkte beregning):
    assert vals[:10] == [0, 1, 2, 3, 1, 4, 3, 2, 1, 4]
    # Splits: (n,) kan ende i (a,b) → XOR-regel implicit i rekursionen.
    # Ekstra sanity: sammensatte segmenter
    assert eng.grundy((2, 2)) == (eng.grundy((2,)) ^ eng.grundy((2,)))


def test_long_application_scan() -> None:
    """
    Typisk konkurrenceanvendelse:
    - Givet en parameter N, udled for hvilke N stillingen er vindbar.
    - Brug periode hvis den findes.
    Her bruger vi subtraction game {1,3,4}.
    """
    eng = GrundyEngine(subtraction_game_moves_factory({1, 3, 4}))
    N = 500
    seq = [eng.grundy(n) for n in range(N + 1)]
    period = detect_period(seq, min_period=1, max_period=100)
    assert period == 7

    # Vindbare N op til 60:
    winning_N = [n for n in range(61) if seq[n] != 0]
    # Spot-check de første par værdier
    assert winning_N[:12] == [1, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 17]


def test_cycle_guard_note() -> None:
    """
    Teori-krav: ingen cykler. Denne test er 'meta' og dokumenterer antagelsen.
    Vi bygger IKKE en cyklisk moves-funktion her; vi noterer blot kravet.
    """
    assert True


# -----------------------------
# Kompakt samlet test
# -----------------------------

def test_main() -> None:
    test_nim_basic()
    test_subtraction_game_period()
    test_sum_of_independent_subgames()
    test_kayles_small()
    test_long_application_scan()
    test_cycle_guard_note()


def main() -> None:
    test_main()
    print("All Sprague–Grundy tests passed!")


if __name__ == "__main__":
    main()
