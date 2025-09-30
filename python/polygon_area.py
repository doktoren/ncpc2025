"""
Shoelace formula (Gauss's area formula) for computing the area of a polygon.

Computes the area of a simple polygon given its vertices in order (clockwise or
counter-clockwise). Works for both convex and concave polygons.

The formula: Area = 1/2 * |sum(x_i * y_(i+1) - x_(i+1) * y_i)|

Time complexity: O(n) where n is the number of vertices.
Space complexity: O(1) additional space.
"""

from __future__ import annotations


def polygon_area(vertices: list[tuple[float, float]]) -> float:
    """
    Calculate the area of a polygon using the Shoelace formula.

    Args:
        vertices: List of (x, y) coordinates in order (clockwise or counter-clockwise)

    Returns:
        The area of the polygon (always positive)
    """
    if len(vertices) < 3:
        return 0.0

    n = len(vertices)
    area = 0.0

    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]

    return abs(area) / 2.0


def polygon_signed_area(vertices: list[tuple[float, float]]) -> float:
    """
    Calculate the signed area of a polygon.

    Returns positive area for counter-clockwise vertices, negative for clockwise.
    Useful for determining polygon orientation.

    Args:
        vertices: List of (x, y) coordinates in order

    Returns:
        The signed area (positive for CCW, negative for CW)
    """
    if len(vertices) < 3:
        return 0.0

    n = len(vertices)
    area = 0.0

    for i in range(n):
        j = (i + 1) % n
        area += vertices[i][0] * vertices[j][1]
        area -= vertices[j][0] * vertices[i][1]

    return area / 2.0


def is_clockwise(vertices: list[tuple[float, float]]) -> bool:
    """Check if polygon vertices are in clockwise order."""
    return polygon_signed_area(vertices) < 0


def test_main() -> None:
    # Simple square with side length 2
    square = [(0.0, 0.0), (2.0, 0.0), (2.0, 2.0), (0.0, 2.0)]
    assert polygon_area(square) == 4.0

    # Triangle with base 3 and height 4
    triangle = [(0.0, 0.0), (3.0, 0.0), (1.5, 4.0)]
    assert polygon_area(triangle) == 6.0

    # Test orientation
    ccw_square = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    assert not is_clockwise(ccw_square)


# Don't write tests below during competition.


def test_rectangle() -> None:
    # Rectangle 5 x 3
    rect = [(0.0, 0.0), (5.0, 0.0), (5.0, 3.0), (0.0, 3.0)]
    assert polygon_area(rect) == 15.0

    # Same rectangle, clockwise order
    rect_cw = [(0.0, 0.0), (0.0, 3.0), (5.0, 3.0), (5.0, 0.0)]
    assert polygon_area(rect_cw) == 15.0


def test_triangle_variations() -> None:
    # Right triangle
    tri1 = [(0.0, 0.0), (4.0, 0.0), (0.0, 3.0)]
    assert polygon_area(tri1) == 6.0

    # Same triangle, different order
    tri2 = [(0.0, 3.0), (0.0, 0.0), (4.0, 0.0)]
    assert polygon_area(tri2) == 6.0

    # Equilateral-ish triangle
    tri3 = [(0.0, 0.0), (2.0, 0.0), (1.0, 1.732)]
    area = polygon_area(tri3)
    assert abs(area - 1.732) < 0.01


def test_pentagon() -> None:
    # Regular pentagon (approximate)
    import math
    n = 5
    radius = 1.0
    vertices = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append((x, y))

    area = polygon_area(vertices)
    # Area of regular pentagon with radius 1
    expected = 2.377  # approximately
    assert abs(area - expected) < 0.01


def test_concave_polygon() -> None:
    # L-shaped polygon (concave)
    l_shape = [
        (0.0, 0.0), (2.0, 0.0), (2.0, 1.0),
        (1.0, 1.0), (1.0, 2.0), (0.0, 2.0)
    ]
    # Area = 2x1 rectangle + 1x1 square = 3
    assert polygon_area(l_shape) == 3.0


def test_degenerate_cases() -> None:
    # Empty polygon
    assert polygon_area([]) == 0.0

    # Single point
    assert polygon_area([(1.0, 1.0)]) == 0.0

    # Two points (line segment)
    assert polygon_area([(0.0, 0.0), (1.0, 1.0)]) == 0.0


def test_floating_point() -> None:
    # Polygon with floating point coordinates
    poly = [(0.5, 0.5), (3.7, 0.5), (3.7, 2.8), (0.5, 2.8)]
    area = polygon_area(poly)
    expected = (3.7 - 0.5) * (2.8 - 0.5)
    assert abs(area - expected) < 1e-10


def test_signed_area() -> None:
    # Counter-clockwise square (positive area)
    ccw = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    assert polygon_signed_area(ccw) == 1.0
    assert not is_clockwise(ccw)

    # Clockwise square (negative area)
    cw = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)]
    assert polygon_signed_area(cw) == -1.0
    assert is_clockwise(cw)


def test_large_polygon() -> None:
    # Polygon with many vertices (octagon)
    import math
    n = 8
    radius = 5.0
    vertices = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        vertices.append((x, y))

    area = polygon_area(vertices)
    # Area of regular polygon: (n * r^2 * sin(2π/n)) / 2
    expected = (n * radius * radius * math.sin(2 * math.pi / n)) / 2
    assert abs(area - expected) < 0.01


def test_negative_coordinates() -> None:
    # Polygon with negative coordinates
    poly = [(-2.0, -1.0), (1.0, -1.0), (1.0, 2.0), (-2.0, 2.0)]
    area = polygon_area(poly)
    expected = 3.0 * 3.0
    assert area == expected


def test_diamond() -> None:
    # Diamond shape (rhombus)
    diamond = [(0.0, 2.0), (3.0, 0.0), (0.0, -2.0), (-3.0, 0.0)]
    area = polygon_area(diamond)
    # Area = (d1 * d2) / 2 where d1=6, d2=4
    expected = 12.0
    assert area == expected


def test_integer_coordinates() -> None:
    # Ensure integer coordinates work correctly
    poly = [(0.0, 0.0), (10.0, 0.0), (10.0, 5.0), (0.0, 5.0)]
    area = polygon_area(poly)
    assert area == 50.0


def main() -> None:
    test_rectangle()
    test_triangle_variations()
    test_pentagon()
    test_concave_polygon()
    test_degenerate_cases()
    test_floating_point()
    test_signed_area()
    test_large_polygon()
    test_negative_coordinates()
    test_diamond()
    test_integer_coordinates()
    test_main()


if __name__ == "__main__":
    main()
