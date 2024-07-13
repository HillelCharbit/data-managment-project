import java.awt.geom.Point2D;

public class Cell {
    private Point2D point1;
    private Point2D point2;

    public Cell(Point2D point1, Point2D point2) {
        this.point1 = point1;
        this.point2 = point2;
    }

    public Point2D getPoint1() {
        return point1;
    }

    public Point2D getPoint2() {
        return point2;
    }
}
