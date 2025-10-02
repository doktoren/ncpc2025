# Data structures and algorithms for programming competitions

Python has been locked to 3.9.18 for use with [NCPC 20225](https://docs.icpc.global/worldfinals-programming-environment/)

[Allowed python packages](https://image.icpc.global/icpc2025/pypy3.modules.txt).
None of these seems relevant for a programming contest.

These data structure modules are intended for use in a programming competition.
That is; these algorithms will be printed on paper such that they
can be typed quickly during a contest.

The type annotations will not be typed in during a contest and we cannot rely on linting
during a contest.

Only the test case `def test_compact(...)` should be typed in and run during a competition.
This test case is indented to catch errors from introducing an error while typing in
the implementation from paper. This test should be compact in size and quick to type.
