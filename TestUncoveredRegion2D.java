import java.awt.geom.Point2D;
import java.util.List;

public class TestUncoveredRegion2D {
    public static void main(String[] args) {
        UncoveredRegion2D ur = new UncoveredRegion2D(0.1, 2);
        ur.addPoint(0.1, 0.2);
        ur.addPoint(0.2, 0.2);
        ur.addPoint(0.3, 0.3);
        ur.addPoint(0.4, 0.4);
        ur.addPoint(0.5, 0.5);

        List<Point2D> uncoveredRegions = ur.identifyUncoveredRegions();
        for (Point2D point : uncoveredRegions) {
            System.out.println("Uncovered Point: (" + point.getX() + ", " + point.getY() + ")");
        }
    }
}

