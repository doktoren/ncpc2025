/*
Andrew's monotone chain algorithm for computing the convex hull of 2D points.

Time complexity: O(n log n) dominated by sorting.
Space complexity: O(n).
*/

#include <algorithm>
#include <cassert>
#include <iostream>
#include <vector>

struct Point {
    double x, y;

    bool operator<(const Point& other) const {
        return x < other.x || (x == other.x && y < other.y);
    }

    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
};

double cross(const Point& o, const Point& a, const Point& b) {
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x);
}

std::vector<Point> convex_hull(std::vector<Point> points) {
    if (points.size() <= 1) { return points; }

    std::sort(points.begin(), points.end());

    std::vector<Point> lower;
    for (const auto& p : points) {
        while (lower.size() >= 2 &&
               cross(lower[lower.size() - 2], lower[lower.size() - 1], p) <= 0) {
            lower.pop_back();
        }
        lower.push_back(p);
    }

    std::vector<Point> upper;
    for (int i = points.size() - 1; i >= 0; i--) {
        const auto& p = points[i];
        while (upper.size() >= 2 &&
               cross(upper[upper.size() - 2], upper[upper.size() - 1], p) <= 0) {
            upper.pop_back();
        }
        upper.push_back(p);
    }

    lower.pop_back();
    upper.pop_back();
    lower.insert(lower.end(), upper.begin(), upper.end());

    return lower;
}

void test_main() {
    std::vector<Point> pts = {{0, 0}, {1, 0}, {1, 1}, {0, 1}, {0.5, 0.5}};
    auto hull = convex_hull(pts);
    assert(hull.size() == 4);
    assert(std::find(hull.begin(), hull.end(), Point{0, 0}) != hull.end());
    assert(std::find(hull.begin(), hull.end(), Point{0.5, 0.5}) == hull.end());
}

// Don't write tests below during competition.

void test_empty() {
    assert(convex_hull({}).empty());
}

void test_single_point() {
    auto hull = convex_hull({{1, 2}});
    assert(hull.size() == 1);
}

void test_triangle() {
    std::vector<Point> pts = {{0, 0}, {2, 0}, {1, 2}};
    auto hull = convex_hull(pts);
    assert(hull.size() == 3);
}

void test_with_interior() {
    std::vector<Point> pts = {{0, 0}, {4, 0}, {4, 3}, {2, 4}, {0, 3}, {2, 2}, {2, 1}};
    auto hull = convex_hull(pts);
    assert(hull.size() == 5);
}

int main() {
    test_main();
    test_empty();
    test_single_point();
    test_triangle();
    test_with_interior();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}
