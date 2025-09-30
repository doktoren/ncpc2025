"""
Write-only prefix tree (trie) for efficient string storage and retrieval.

Supports adding strings and finding all strings that are prefixes of a given string.
The tree structure allows for efficient storage of strings with common prefixes.

Time complexity: O(m) for add and find operations, where m is the length of the string.
Space complexity: O(ALPHABET_SIZE * N * M) in the worst case, where N is the number
of strings and M is the average length of strings.
"""

from __future__ import annotations

import bisect


class PrefixTree:
    def __init__(self) -> None:
        self.keys: list[str] = []
        self.values: list[PrefixTree | None] = []

    def pp(self, indent: int = 0) -> None:
        for key, value in zip(self.keys, self.values):  # Note: add strict=False for Python 3.10+
            print(" " * indent + key + ": " + ("-" if value is None else ""))
            if value is not None:
                value.pp(indent + 2)

    def find_all(self, s: str, offset: int, append_to: list[int]) -> None:
        """Add matching end indexes to append_to."""
        if self.keys and self.keys[0] == "":
            append_to.append(offset)
        index = bisect.bisect_left(self.keys, s[offset : offset + 1])
        if index == len(self.keys):
            return
        if s[offset : offset + len(self.keys[index])] == self.keys[index]:
            pt = self.values[index]
            if pt is None:
                append_to.append(offset + len(self.keys[index]))
            else:
                pt.find_all(s, offset + len(self.keys[index]), append_to)

    def max_len(self) -> int:
        result = 0
        for key, value in zip(self.keys, self.values):  # Note: add strict=False for Python 3.10+
            result = max(result, len(key) + (0 if value is None else value.max_len()))
        return result

    def add(self, s: str) -> None:
        if not s or not self.keys:
            self.keys.insert(0, s)
            self.values.insert(0, None)
            return

        pos = bisect.bisect_left(self.keys, s)
        if pos and self.keys[pos - 1] and self.keys[pos - 1][0] == s[0]:
            pos -= 1
        if pos < len(self.keys) and self.keys[pos][:1] == s[:1]:
            # Merge
            if s.startswith(self.keys[pos]):
                pt = self.values[pos]
                if pt is None:
                    child = PrefixTree()
                    child.keys.append("")
                    child.values.append(None)
                    self.values[pos] = pt = child
                pt.add(s[len(self.keys[pos]) :])
            elif self.keys[pos].startswith(s):
                child = PrefixTree()
                child.keys.append("")
                child.values.append(None)
                child.keys.append(self.keys[pos][len(s) :])
                child.values.append(self.values[pos])
                self.keys[pos] = s
                self.values[pos] = child
            else:
                prefix = 1
                while s[prefix] == self.keys[pos][prefix]:
                    prefix += 1
                child = PrefixTree()
                if s < self.keys[pos]:
                    child.keys.append(s[prefix:])
                    child.values.append(None)
                child.keys.append(self.keys[pos][prefix:])
                child.values.append(self.values[pos])
                if s >= self.keys[pos]:
                    child.keys.append(s[prefix:])
                    child.values.append(None)
                self.keys[pos] = s[:prefix]
                self.values[pos] = child
        else:
            self.keys.insert(pos, s)
            self.values.insert(pos, None)


def test_main() -> None:
    p = PrefixTree()
    p.add("cat")
    p.add("car")
    p.add("card")
    l: list[int] = []
    p.find_all("card", 0, l)
    assert l == [3, 4]
    assert p.max_len() == 4


# Don't write tests below during competition.


def main() -> None:
    test_main()


if __name__ == "__main__":
    main()
