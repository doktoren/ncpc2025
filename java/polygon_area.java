/*
Shoelace formula (Gauss's area formula) for computing the area of a polygon.

Computes the area of a simple polygon given its vertices in order (clockwise or
counter-clockwise). Works for both convex and concave polygons.

The formula: Area = 1/2 * |sum(x_i * y_(i+1) - x_(i+1) * y_i)|

Time complexity: O(n) where n is the number of vertices.
Space complexity: O(1) additional space.
*/

class polygon_area {
    static class Point {
        double x, y;

        Point(double x, double y) {
            this.x = x;
            this.y = y;
        }
    }

    static double polygonArea(Point[] vertices) {
        if (vertices.length < 3) {
            return 0.0;
        }

        int n = vertices.length;
        double area = 0.0;

        for (int i = 0; i < n; i++) {
            int j = (i + 1) % n;
            area += vertices[i].x * vertices[j].y;
            area -= vertices[j].x * vertices[i].y;
        }

        return Math.abs(area) / 2.0;
    }

    static double polygonSignedArea(Point[] vertices) {
        if (vertices.length < 3) {
            return 0.0;
        }

        int n = vertices.length;
        double area = 0.0;

        for (int i = 0; i < n; i++) {
            int j = (i + 1) % n;
            area += vertices[i].x * vertices[j].y;
            area -= vertices[j].x * vertices[i].y;
        }

        return area / 2.0;
    }

    static boolean isClockwise(Point[] vertices) {
        return polygonSignedArea(vertices) < 0;
    }

    static void testMain() {
        // Simple square with side length 2
        Point[] square = {
            new Point(0.0, 0.0), new Point(2.0, 0.0), new Point(2.0, 2.0), new Point(0.0, 2.0)
        };
        assert Math.abs(polygonArea(square) - 4.0) < 1e-9;

        // Triangle with base 3 and height 4
        Point[] triangle = {new Point(0.0, 0.0), new Point(3.0, 0.0), new Point(1.5, 4.0)};
        assert Math.abs(polygonArea(triangle) - 6.0) < 1e-9;

        // Test orientation
        Point[] ccwSquare = {
            new Point(0.0, 0.0), new Point(1.0, 0.0), new Point(1.0, 1.0), new Point(0.0, 1.0)
        };
        assert !isClockwise(ccwSquare);
    }

    // Don't write tests below during competition.

    static void testRectangle() {
        Point[] rect = {
            new Point(0.0, 0.0), new Point(5.0, 0.0), new Point(5.0, 3.0), new Point(0.0, 3.0)
        };
        assert polygonArea(rect) == 15.0;

        Point[] rectCw = {
            new Point(0.0, 0.0), new Point(0.0, 3.0), new Point(5.0, 3.0), new Point(5.0, 0.0)
        };
        assert polygonArea(rectCw) == 15.0;
    }

    static void testDiamond() {
        Point[] diamond = {
            new Point(0.0, 2.0), new Point(3.0, 0.0), new Point(0.0, -2.0), new Point(-3.0, 0.0)
        };
        double area = polygonArea(diamond);
        assert area == 12.0;
    }

    static void testSignedArea() {
        Point[] ccw = {
            new Point(0.0, 0.0), new Point(1.0, 0.0), new Point(1.0, 1.0), new Point(0.0, 1.0)
        };
        assert polygonSignedArea(ccw) == 1.0;
        assert !isClockwise(ccw);

        Point[] cw = {
            new Point(0.0, 0.0), new Point(0.0, 1.0), new Point(1.0, 1.0), new Point(1.0, 0.0)
        };
        assert polygonSignedArea(cw) == -1.0;
        assert isClockwise(cw);
    }

    public static void main(String[] args) {
        testRectangle();
        testDiamond();
        testSignedArea();
        testMain();
        System.out.println("All tests passed!");
    }
}
