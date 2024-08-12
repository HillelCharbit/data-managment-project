import java.awt.geom.Point2D;
import java.util.ArrayList;
import java.util.List;

public class UncoveredRegion2D {
    private List<Point2D> points;
    private double radius;
    private int k;

    public UncoveredRegion2D(double radius, int k) {
        this.points = new ArrayList<>();
        this.radius = radius;
        this.k = k;
    }

    public void addPoint(double x, double y) {
        points.add(new Point2D.Double(x, y));
    }

    public List<Point2D> identifyUncoveredRegions() {
        List<Point2D> uncoveredPoints = new ArrayList<>();
        for (Point2D queryPoint : points) {
            int count = 0;
            for (Point2D point : points) {
                if (!point.equals(queryPoint) && queryPoint.distance(point) <= radius) {
                    count++;
                }
            }
            if (count < k) {
                uncoveredPoints.add(queryPoint);
            }
        }
        return uncoveredPoints;
    }

    public List<Point2D> getPoints() {
        return points;
    }

    public double getRadius() {
        return radius;
    }



    // private Point2D findClosestPoint(Point2D queryPoint) {
    //     double minDist = Double.MAX_VALUE;
    //     Point2D closest = null;
    //     for (Point2D point : points) {
    //         double dist = queryPoint.distance(point);
    //         if (dist < minDist) {
    //             minDist = dist;
    //             closest = point;
    //         }
    //     }
    //     return closest;
    // }

    // private boolean isPointInVoronoiCell(Point2D point, Point2D queryPoint) {
    //     double distanceToQuery = queryPoint.distance(point);
    //     for (Point2D otherPoint : points) {
    //         if (!otherPoint.equals(point) && queryPoint.distance(otherPoint) < distanceToQuery) {
    //             return false;
    //         }
    //     }
    //     return true;
    // }
}
