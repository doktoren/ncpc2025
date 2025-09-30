/*
Shoelace formula (Gauss's area formula) for computing the area of a polygon.

Computes the area of a simple polygon given its vertices in order (clockwise or
counter-clockwise). Works for both convex and concave polygons.

The formula: Area = ½ |∑(xᵢ × yᵢ₊₁ - xᵢ₊₁ × yᵢ)|

Time complexity: O(n) where n is the number of vertices.
Space complexity: O(1) additional space.
*/

#include <iostream>
#include <vector>
#include <cmath>
#include <cassert>

struct Point {
    double x, y;
    Point(double x = 0, double y = 0) : x(x), y(y) {}
};

double polygon_area(const std::vector<Point>& vertices) {
    /*
    Calculate the area of a polygon using the Shoelace formula.

    Args:
        vertices: Vector of points in order (clockwise or counter-clockwise)

    Returns:
        The area of the polygon (always positive)
    */
    if (vertices.size() < 3) {
        return 0.0;
    }

    int n = vertices.size();
    double area = 0.0;

    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n;
        area += vertices[i].x * vertices[j].y;
        area -= vertices[j].x * vertices[i].y;
    }

    return std::abs(area) / 2.0;
}

double polygon_signed_area(const std::vector<Point>& vertices) {
    /*
    Calculate the signed area of a polygon.

    Returns positive area for counter-clockwise vertices, negative for clockwise.
    Useful for determining polygon orientation.

    Args:
        vertices: Vector of points in order

    Returns:
        The signed area (positive for CCW, negative for CW)
    */
    if (vertices.size() < 3) {
        return 0.0;
    }

    int n = vertices.size();
    double area = 0.0;

    for (int i = 0; i < n; i++) {
        int j = (i + 1) % n;
        area += vertices[i].x * vertices[j].y;
        area -= vertices[j].x * vertices[i].y;
    }

    return area / 2.0;
}

bool is_clockwise(const std::vector<Point>& vertices) {
    /* Check if polygon vertices are in clockwise order. */
    return polygon_signed_area(vertices) < 0;
}

void test_main() {
    // Simple square with side length 2
    std::vector<Point> square = {{0.0, 0.0}, {2.0, 0.0}, {2.0, 2.0}, {0.0, 2.0}};
    assert(polygon_area(square) == 4.0);

    // Triangle with base 3 and height 4
    std::vector<Point> triangle = {{0.0, 0.0}, {3.0, 0.0}, {1.5, 4.0}};
    assert(polygon_area(triangle) == 6.0);

    // Test orientation
    std::vector<Point> ccw_square = {{0.0, 0.0}, {1.0, 0.0}, {1.0, 1.0}, {0.0, 1.0}};
    assert(!is_clockwise(ccw_square));
}

// Don't write tests below during competition.

void test_rectangle() {
    // Rectangle 5 x 3
    std::vector<Point> rect = {{0.0, 0.0}, {5.0, 0.0}, {5.0, 3.0}, {0.0, 3.0}};
    assert(polygon_area(rect) == 15.0);

    // Same rectangle, clockwise order
    std::vector<Point> rect_cw = {{0.0, 0.0}, {0.0, 3.0}, {5.0, 3.0}, {5.0, 0.0}};
    assert(polygon_area(rect_cw) == 15.0);
}

void test_triangle_variations() {
    // Right triangle
    std::vector<Point> tri1 = {{0.0, 0.0}, {4.0, 0.0}, {0.0, 3.0}};
    assert(polygon_area(tri1) == 6.0);

    // Same triangle, different order
    std::vector<Point> tri2 = {{0.0, 3.0}, {0.0, 0.0}, {4.0, 0.0}};
    assert(polygon_area(tri2) == 6.0);

    // Equilateral-ish triangle
    std::vector<Point> tri3 = {{0.0, 0.0}, {2.0, 0.0}, {1.0, 1.732}};
    double area = polygon_area(tri3);
    assert(std::abs(area - 1.732) < 0.01);
}

void test_pentagon() {
    // Regular pentagon (approximate)
    int n = 5;
    double radius = 1.0;
    std::vector<Point> vertices;

    for (int i = 0; i < n; i++) {
        double angle = 2 * M_PI * i / n;
        double x = radius * std::cos(angle);
        double y = radius * std::sin(angle);
        vertices.push_back({x, y});
    }

    double area = polygon_area(vertices);
    // Area of regular pentagon with radius 1
    double expected = 2.377;  // approximately
    assert(std::abs(area - expected) < 0.01);
}

void test_concave_polygon() {
    // L-shaped polygon (concave)
    std::vector<Point> l_shape = {
        {0.0, 0.0}, {2.0, 0.0}, {2.0, 1.0},
        {1.0, 1.0}, {1.0, 2.0}, {0.0, 2.0}
    };
    // Area = 2x1 rectangle + 1x1 square = 3
    assert(polygon_area(l_shape) == 3.0);
}

void test_degenerate_cases() {
    // Empty polygon
    assert(polygon_area({}) == 0.0);

    // Single point
    assert(polygon_area({{1.0, 1.0}}) == 0.0);

    // Two points (line segment)
    assert(polygon_area({{0.0, 0.0}, {1.0, 1.0}}) == 0.0);
}

void test_floating_point() {
    // Polygon with floating point coordinates
    std::vector<Point> poly = {{0.5, 0.5}, {3.7, 0.5}, {3.7, 2.8}, {0.5, 2.8}};
    double area = polygon_area(poly);
    double expected = (3.7 - 0.5) * (2.8 - 0.5);
    assert(std::abs(area - expected) < 1e-10);
}

void test_signed_area() {
    // Counter-clockwise square (positive area)
    std::vector<Point> ccw = {{0.0, 0.0}, {1.0, 0.0}, {1.0, 1.0}, {0.0, 1.0}};
    assert(polygon_signed_area(ccw) == 1.0);
    assert(!is_clockwise(ccw));

    // Clockwise square (negative area)
    std::vector<Point> cw = {{0.0, 0.0}, {0.0, 1.0}, {1.0, 1.0}, {1.0, 0.0}};
    assert(polygon_signed_area(cw) == -1.0);
    assert(is_clockwise(cw));
}

void test_large_polygon() {
    // Polygon with many vertices (octagon)
    int n = 8;
    double radius = 5.0;
    std::vector<Point> vertices;

    for (int i = 0; i < n; i++) {
        double angle = 2 * M_PI * i / n;
        double x = radius * std::cos(angle);
        double y = radius * std::sin(angle);
        vertices.push_back({x, y});
    }

    double area = polygon_area(vertices);
    // Area of regular polygon: (n * r^2 * sin(2π/n)) / 2
    double expected = (n * radius * radius * std::sin(2 * M_PI / n)) / 2;
    assert(std::abs(area - expected) < 0.01);
}

void test_negative_coordinates() {
    // Polygon with negative coordinates
    std::vector<Point> poly = {{-2.0, -1.0}, {1.0, -1.0}, {1.0, 2.0}, {-2.0, 2.0}};
    double area = polygon_area(poly);
    double expected = 3.0 * 3.0;
    assert(area == expected);
}

void test_diamond() {
    // Diamond shape (rhombus)
    std::vector<Point> diamond = {{0.0, 2.0}, {3.0, 0.0}, {0.0, -2.0}, {-3.0, 0.0}};
    double area = polygon_area(diamond);
    // Area = (d1 * d2) / 2 where d1=6, d2=4
    double expected = 12.0;
    assert(area == expected);
}

void test_integer_coordinates() {
    // Ensure integer coordinates work correctly
    std::vector<Point> poly = {{0, 0}, {10, 0}, {10, 5}, {0, 5}};
    double area = polygon_area(poly);
    assert(area == 50.0);
}

int main() {
    test_rectangle();
    test_triangle_variations();
    test_pentagon();
    test_concave_polygon();
    test_degenerate_cases();
    test_floating_point();
    test_signed_area();
    test_large_polygon();
    test_negative_coordinates();
    test_diamond();
    test_integer_coordinates();
    test_main();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}
