/*
Andrew's monotone chain algorithm for computing the convex hull of 2D points.

Computes the convex hull (smallest convex polygon containing all points) using
a simple and robust algorithm.

Key operations:
- convexHull(points): Returns convex hull vertices in counter-clockwise order

Time complexity: O(n log n) dominated by sorting
Space complexity: O(n)
*/

import java.util.*;

class convex_hull {
    static class Point implements Comparable<Point> {
        double x, y;

        Point(double x, double y) {
            this.x = x;
            this.y = y;
        }

        @Override
        public int compareTo(Point other) {
            if (this.x != other.x) {
                return Double.compare(this.x, other.x);
            }
            return Double.compare(this.y, other.y);
        }

        @Override
        public boolean equals(Object obj) {
            if (!(obj instanceof Point)) return false;
            Point p = (Point) obj;
            return this.x == p.x && this.y == p.y;
        }

        @Override
        public int hashCode() {
            return Objects.hash(x, y);
        }
    }

    static double cross(Point o, Point a, Point b) {
        return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x);
    }

    static List<Point> convexHull(List<Point> points) {
        if (points.size() <= 1) {
            return new ArrayList<>(points);
        }

        List<Point> sorted = new ArrayList<>(points);
        Collections.sort(sorted);

        List<Point> lower = new ArrayList<>();
        for (Point p : sorted) {
            while (lower.size() >= 2
                    && cross(lower.get(lower.size() - 2), lower.get(lower.size() - 1), p) <= 0) {
                lower.remove(lower.size() - 1);
            }
            lower.add(p);
        }

        List<Point> upper = new ArrayList<>();
        for (int i = sorted.size() - 1; i >= 0; i--) {
            Point p = sorted.get(i);
            while (upper.size() >= 2
                    && cross(upper.get(upper.size() - 2), upper.get(upper.size() - 1), p) <= 0) {
                upper.remove(upper.size() - 1);
            }
            upper.add(p);
        }

        lower.remove(lower.size() - 1);
        upper.remove(upper.size() - 1);
        lower.addAll(upper);

        return lower;
    }

    static void testMain() {
        List<Point> pts =
                Arrays.asList(
                        new Point(0, 0),
                        new Point(1, 0),
                        new Point(1, 1),
                        new Point(0, 1),
                        new Point(0.5, 0.5));
        List<Point> hull = convexHull(pts);
        assert hull.size() == 4;
        assert hull.contains(new Point(0, 0));
        assert hull.contains(new Point(1, 0));
        assert hull.contains(new Point(1, 1));
        assert hull.contains(new Point(0, 1));
        assert !hull.contains(new Point(0.5, 0.5));
    }

    // Don't write tests below during competition.

    static void testEmpty() {
        assert convexHull(new ArrayList<>()).isEmpty();
    }

    static void testSinglePoint() {
        List<Point> pts = Arrays.asList(new Point(1, 2));
        List<Point> hull = convexHull(pts);
        assert hull.size() == 1;
    }

    static void testTwoPoints() {
        List<Point> pts = Arrays.asList(new Point(0, 0), new Point(1, 1));
        List<Point> hull = convexHull(pts);
        assert hull.size() == 2;
    }

    static void testCollinearPoints() {
        List<Point> pts =
                Arrays.asList(
                        new Point(0, 0), new Point(1, 1),
                        new Point(2, 2), new Point(3, 3));
        List<Point> hull = convexHull(pts);
        assert hull.size() == 2;
        assert hull.contains(new Point(0, 0));
        assert hull.contains(new Point(3, 3));
    }

    static void testTriangle() {
        List<Point> pts = Arrays.asList(new Point(0, 0), new Point(2, 0), new Point(1, 2));
        List<Point> hull = convexHull(pts);
        assert hull.size() == 3;
    }

    static void testWithInteriorPoints() {
        List<Point> pts =
                Arrays.asList(
                        new Point(0, 0),
                        new Point(4, 0),
                        new Point(4, 3),
                        new Point(2, 4),
                        new Point(0, 3),
                        new Point(2, 2),
                        new Point(2, 1));
        List<Point> hull = convexHull(pts);
        assert hull.size() == 5;
        assert !hull.contains(new Point(2, 2));
        assert !hull.contains(new Point(2, 1));
    }

    static void testNegativeCoordinates() {
        List<Point> pts =
                Arrays.asList(
                        new Point(-1, -1), new Point(1, -1),
                        new Point(1, 1), new Point(-1, 1));
        List<Point> hull = convexHull(pts);
        assert hull.size() == 4;
    }

    static void testLargeSquare() {
        List<Point> pts = new ArrayList<>();
        for (int i = 0; i <= 10; i++) {
            for (int j = 0; j <= 10; j++) {
                pts.add(new Point(i, j));
            }
        }
        List<Point> hull = convexHull(pts);
        assert hull.size() == 4;
        assert hull.contains(new Point(0, 0));
        assert hull.contains(new Point(10, 0));
        assert hull.contains(new Point(10, 10));
        assert hull.contains(new Point(0, 10));
    }

    public static void main(String[] args) {
        testMain();
        testEmpty();
        testSinglePoint();
        testTwoPoints();
        testCollinearPoints();
        testTriangle();
        testWithInteriorPoints();
        testNegativeCoordinates();
        testLargeSquare();
        System.out.println("All tests passed!");
    }
}
