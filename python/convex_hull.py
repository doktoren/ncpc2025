"""
Andrew's monotone chain algorithm for computing the convex hull of 2D points.

Computes the convex hull (smallest convex polygon containing all points) using
a simple and robust algorithm. Works in sorted order to build lower and upper hulls.

Time complexity: O(n log n) dominated by sorting, where n is number of points.
Space complexity: O(n) for the hull and auxiliary structures.
"""

from __future__ import annotations

# Don't use annotations during contest
from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class Point:
    x: float
    y: float


def cross(o: Point, a: Point, b: Point) -> float:
    """
    Cross product of vectors OA and OB.
    Positive if OAB makes a counter-clockwise turn, negative if clockwise, zero if collinear.
    """
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)


def convex_hull(points: list[Point]) -> list[Point]:
    """
    Compute convex hull using Andrew's monotone chain algorithm.

    Returns points on the convex hull in counter-clockwise order starting from
    the leftmost point. Includes collinear points only if they are extreme points.
    """
    if len(points) <= 1:
        return points[:]

    # Sort points lexicographically (first by x, then by y)
    sorted_points = sorted(points)

    # Build lower hull
    lower: list[Point] = []
    for p in sorted_points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper: list[Point] = []
    for p in reversed(sorted_points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Remove last point of each half because it's repeated
    return lower[:-1] + upper[:-1]


def test_main() -> None:
    # Test square
    pts = [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1), Point(0.5, 0.5)]
    hull = convex_hull(pts)
    assert len(hull) == 4
    assert Point(0, 0) in hull
    assert Point(1, 0) in hull
    assert Point(1, 1) in hull
    assert Point(0, 1) in hull
    assert Point(0.5, 0.5) not in hull


# Don't write tests below during competition.


def test_empty() -> None:
    assert convex_hull([]) == []


def test_single_point() -> None:
    pts = [Point(1, 2)]
    hull = convex_hull(pts)
    assert hull == pts


def test_two_points() -> None:
    pts = [Point(0, 0), Point(1, 1)]
    hull = convex_hull(pts)
    assert len(hull) == 2
    assert Point(0, 0) in hull
    assert Point(1, 1) in hull


def test_collinear_points() -> None:
    pts = [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)]
    hull = convex_hull(pts)
    # Only endpoints should be in hull
    assert len(hull) == 2
    assert Point(0, 0) in hull
    assert Point(3, 3) in hull


def test_triangle() -> None:
    pts = [Point(0, 0), Point(2, 0), Point(1, 2)]
    hull = convex_hull(pts)
    assert len(hull) == 3
    for p in pts:
        assert p in hull


def test_with_interior_points() -> None:
    # Pentagon with interior points
    pts = [
        Point(0, 0),
        Point(4, 0),
        Point(4, 3),
        Point(2, 4),
        Point(0, 3),
        Point(2, 2),  # Interior
        Point(2, 1),  # Interior
    ]
    hull = convex_hull(pts)
    assert len(hull) == 5
    assert Point(2, 2) not in hull
    assert Point(2, 1) not in hull


def test_all_same_point() -> None:
    pts = [Point(1, 1), Point(1, 1), Point(1, 1)]
    hull = convex_hull(pts)
    # Algorithm returns one point per position (duplicates removed by sorting)
    assert all(p == Point(1, 1) for p in hull)


def test_negative_coordinates() -> None:
    pts = [Point(-1, -1), Point(1, -1), Point(1, 1), Point(-1, 1)]
    hull = convex_hull(pts)
    assert len(hull) == 4


def test_large_square_with_interior() -> None:
    # 10x10 grid, hull should be the 4 corners
    pts = [Point(float(i), float(j)) for i in range(11) for j in range(11)]
    hull = convex_hull(pts)
    assert len(hull) == 4
    assert Point(0, 0) in hull
    assert Point(10, 0) in hull
    assert Point(10, 10) in hull
    assert Point(0, 10) in hull


def test_circle_approximation() -> None:
    import math

    # Points on a circle
    pts = [Point(math.cos(i * 0.5), math.sin(i * 0.5)) for i in range(13)]
    hull = convex_hull(pts)
    # All points should be on the hull (circle is convex)
    assert len(hull) == len(pts)


def main() -> None:
    test_main()
    test_empty()
    test_single_point()
    test_two_points()
    test_collinear_points()
    test_triangle()
    test_with_interior_points()
    test_all_same_point()
    test_negative_coordinates()
    test_large_square_with_interior()
    test_circle_approximation()


if __name__ == "__main__":
    main()
