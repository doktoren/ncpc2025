"""
2-SAT solver using Kosaraju's SCC algorithm on implication graph.

2-SAT (Boolean Satisfiability with 2 literals per clause) determines if a Boolean formula
in CNF with at most 2 literals per clause is satisfiable. Uses implication graph where
each variable x has nodes x and not-x, and clause (a OR b) creates edges not-a -> b
and not-b -> a.

The formula is satisfiable iff no variable x has x and not-x in the same SCC.

Time complexity: O(n + m) where n is variables and m is clauses.
Space complexity: O(n + m) for the implication graph.
"""

from __future__ import annotations

# Don't use annotations during contest
from typing import Final


class TwoSAT:
    def __init__(self, n: int) -> None:
        """Initialize 2-SAT solver for n Boolean variables (indexed 0 to n-1)."""
        self.n: Final[int] = n
        # Implication graph: node 2*i is x_i, node 2*i+1 is ¬x_i
        self.graph: list[list[int]] = [[] for _ in range(2 * n)]
        self.transpose: list[list[int]] = [[] for _ in range(2 * n)]

    def add_clause(self, a: int, b: int, *, a_neg: bool, b_neg: bool) -> None:
        """
        Add clause (a OR b) where a and b are variable indices.
        a_neg=True means not-a, a_neg=False means a.
        Creates implications: not-a -> b and not-b -> a.
        """
        # Map to graph nodes: 2*i = xi, 2*i+1 = ¬xi
        a_node = 2 * a + (1 if a_neg else 0)  # If a_neg, use ¬a (2*a+1); else use a (2*a)
        b_node = 2 * b + (1 if b_neg else 0)  # If b_neg, use ¬b (2*b+1); else use b (2*b)
        na_node = 2 * a + (0 if a_neg else 1)  # Negation of a_node
        nb_node = 2 * b + (0 if b_neg else 1)  # Negation of b_node

        # ¬a → b and ¬b → a
        self.graph[na_node].append(b_node)
        self.graph[nb_node].append(a_node)
        self.transpose[b_node].append(na_node)
        self.transpose[a_node].append(nb_node)

    def solve(self) -> list[bool] | None:
        """
        Solve 2-SAT problem.

        Returns assignment [x_0, x_1, ..., x_{n-1}] if satisfiable, None otherwise.
        If variable x and ¬x are in same SCC, formula is unsatisfiable.
        """
        # Kosaraju's algorithm for SCCs
        visited: list[bool] = [False] * (2 * self.n)
        finish_order: list[int] = []

        def dfs1(node: int) -> None:
            visited[node] = True
            for neighbor in self.graph[node]:
                if not visited[neighbor]:
                    dfs1(neighbor)
            finish_order.append(node)

        for node in range(2 * self.n):
            if not visited[node]:
                dfs1(node)

        # Second DFS pass on transpose
        visited = [False] * (2 * self.n)
        scc_id: list[int] = [-1] * (2 * self.n)
        current_scc = 0

        def dfs2(node: int, scc: int) -> None:
            visited[node] = True
            scc_id[node] = scc
            for neighbor in self.transpose[node]:
                if not visited[neighbor]:
                    dfs2(neighbor, scc)

        for node in reversed(finish_order):
            if not visited[node]:
                dfs2(node, current_scc)
                current_scc += 1

        # Check satisfiability: x and ¬x must not be in same SCC
        for i in range(self.n):
            if scc_id[2 * i] == scc_id[2 * i + 1]:
                return None

        # Construct assignment: if SCC(x) > SCC(not-x), set x=True (reverse topo order)
        return [scc_id[2 * i] > scc_id[2 * i + 1] for i in range(self.n)]


def test_main() -> None:
    # Test: (x0 ∨ x1) ∧ (¬x0 ∨ x1) ∧ (x0 ∨ ¬x1)
    # Simplifies to: x1 ∧ x0, so both must be True
    sat: TwoSAT = TwoSAT(2)
    sat.add_clause(0, 1, a_neg=False, b_neg=False)  # x0 ∨ x1
    sat.add_clause(0, 1, a_neg=True, b_neg=False)  # ¬x0 ∨ x1
    sat.add_clause(0, 1, a_neg=False, b_neg=True)  # x0 ∨ ¬x1

    result = sat.solve()
    assert result is not None

    # Verify solution satisfies all clauses
    assert result[0] or result[1]  # x0 ∨ x1
    assert (not result[0]) or result[1]  # ¬x0 ∨ x1
    assert result[0] or (not result[1])  # x0 ∨ ¬x1


# Don't write tests below during competition.


def test_unsatisfiable() -> None:
    # Test: (x ∨ y) ∧ (x ∨ ¬y) ∧ (¬x ∨ y) ∧ (¬x ∨ ¬y)
    # This is equivalent to x ∧ ¬x, which is unsatisfiable
    sat: TwoSAT = TwoSAT(2)
    sat.add_clause(0, 1, a_neg=False, b_neg=False)  # x ∨ y
    sat.add_clause(0, 1, a_neg=False, b_neg=True)  # x ∨ ¬y
    sat.add_clause(0, 1, a_neg=True, b_neg=False)  # ¬x ∨ y
    sat.add_clause(0, 1, a_neg=True, b_neg=True)  # ¬x ∨ ¬y

    result = sat.solve()
    assert result is None


def test_single_variable() -> None:
    # Test: (x ∨ x) which is just x
    sat: TwoSAT = TwoSAT(1)
    sat.add_clause(0, 0, a_neg=False, b_neg=False)  # x ∨ x

    result = sat.solve()
    assert result is not None
    assert result[0] is True


def test_trivial_satisfiable() -> None:
    # Test: (x ∨ ¬x) which is always true
    sat: TwoSAT = TwoSAT(1)
    sat.add_clause(0, 0, a_neg=False, b_neg=True)  # x ∨ ¬x

    result = sat.solve()
    assert result is not None  # Can be either True or False


def test_implication_chain() -> None:
    # Test: (¬x0 ∨ x1) ∧ (¬x1 ∨ x2) ∧ (¬x2 ∨ x3)
    # This creates chain: x0 → x1 → x2 → x3
    # Satisfiable with x0=False or all True
    sat: TwoSAT = TwoSAT(4)
    sat.add_clause(0, 1, a_neg=True, b_neg=False)  # ¬x0 ∨ x1 (x0 → x1)
    sat.add_clause(1, 2, a_neg=True, b_neg=False)  # ¬x1 ∨ x2 (x1 → x2)
    sat.add_clause(2, 3, a_neg=True, b_neg=False)  # ¬x2 ∨ x3 (x2 → x3)

    result = sat.solve()
    assert result is not None
    # Verify implications
    if result[0]:
        assert result[1]
    if result[1]:
        assert result[2]
    if result[2]:
        assert result[3]


def test_mutual_implication() -> None:
    # Test: (¬x ∨ y) ∧ (¬y ∨ x)
    # This means x ↔ y (x and y must have same value)
    sat: TwoSAT = TwoSAT(2)
    sat.add_clause(0, 1, a_neg=True, b_neg=False)  # ¬x ∨ y (x → y)
    sat.add_clause(1, 0, a_neg=True, b_neg=False)  # ¬y ∨ x (y → x)

    result = sat.solve()
    assert result is not None
    assert result[0] == result[1]


def test_large_satisfiable() -> None:
    # Test with 10 variables, random satisfiable clauses
    sat: TwoSAT = TwoSAT(10)

    # Add clauses that form a satisfiable system
    for i in range(9):
        sat.add_clause(i, i + 1, a_neg=False, b_neg=False)  # xi ∨ xi+1

    result = sat.solve()
    assert result is not None
    # At least one variable in each pair should be True
    for i in range(9):
        assert result[i] or result[i + 1]


def test_contradictory_implications() -> None:
    # Test: x → y and x → ¬y, which means ¬x must be True
    sat: TwoSAT = TwoSAT(2)
    sat.add_clause(0, 1, a_neg=True, b_neg=False)  # ¬x ∨ y (x → y)
    sat.add_clause(0, 1, a_neg=True, b_neg=True)  # ¬x ∨ ¬y (x → ¬y)

    result = sat.solve()
    assert result is not None
    assert result[0] is False  # x must be False


def test_complex_system() -> None:
    # 5 variables with multiple constraints
    sat: TwoSAT = TwoSAT(5)
    sat.add_clause(0, 1, a_neg=False, b_neg=False)  # x0 ∨ x1
    sat.add_clause(1, 2, a_neg=True, b_neg=False)  # ¬x1 ∨ x2
    sat.add_clause(2, 3, a_neg=True, b_neg=True)  # ¬x2 ∨ ¬x3
    sat.add_clause(3, 4, a_neg=False, b_neg=False)  # x3 ∨ x4
    sat.add_clause(4, 0, a_neg=True, b_neg=True)  # ¬x4 ∨ ¬x0

    result = sat.solve()
    assert result is not None

    # Verify all clauses
    assert result[0] or result[1]
    assert (not result[1]) or result[2]
    assert (not result[2]) or (not result[3])
    assert result[3] or result[4]
    assert (not result[4]) or (not result[0])


def test_xor_constraint() -> None:
    # Test XOR: x ⊕ y (exactly one of x, y is True)
    # XOR = (x ∨ y) ∧ (¬x ∨ ¬y)
    sat: TwoSAT = TwoSAT(2)
    sat.add_clause(0, 1, a_neg=False, b_neg=False)  # x ∨ y
    sat.add_clause(0, 1, a_neg=True, b_neg=True)  # ¬x ∨ ¬y

    result = sat.solve()
    assert result is not None
    # Exactly one should be True
    assert (result[0] and not result[1]) or (not result[0] and result[1])


def main() -> None:
    test_main()
    test_unsatisfiable()
    test_single_variable()
    test_trivial_satisfiable()
    test_implication_chain()
    test_mutual_implication()
    test_large_satisfiable()
    test_contradictory_implications()
    test_complex_system()
    test_xor_constraint()


if __name__ == "__main__":
    main()
