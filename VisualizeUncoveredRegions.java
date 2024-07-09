import javax.swing.*;
import java.awt.*;
import java.awt.geom.Point2D;
import java.awt.geom.Ellipse2D;
import java.util.List;

public class VisualizeUncoveredRegions extends JPanel {
    private UncoveredRegion2D uncoveredRegion;

    public VisualizeUncoveredRegions(UncoveredRegion2D ur) {
        this.uncoveredRegion = ur;
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;

        List<Point2D> uncoveredPoints = uncoveredRegion.identifyUncoveredRegions();
        List<Point2D> allPoints = uncoveredRegion.getPoints();
        double radius = uncoveredRegion.getRadius();

        // Adjust the scaling factors as needed to fit the points in the window
        int scale = getWidth();

        // Draw the grid and circles
        for (int i = 0; i < getWidth(); i++) {
            for (int j = 0; j < getHeight(); j++) {
                Point2D.Double testPoint = new Point2D.Double((double) i / scale, (double) j / scale);
                boolean covered = false;
                for (Point2D point : allPoints) {
                    if (testPoint.distance(point) <= radius) {
                        covered = true;
                        break;
                    }
                }
                if (covered) {
                    g2d.setColor(new Color(0, 255, 0, 50)); // light green
                } else {
                    g2d.setColor(new Color(255, 0, 0, 50)); // light red
                }
                g2d.fillRect(i, j, 1, 1);
            }
        }

        // Draw circles and points
        for (Point2D point : allPoints) {
            int x = (int) (point.getX() * scale);
            int y = (int) (point.getY() * scale);
            int r = (int) (radius * scale * 2);

            g2d.setColor(Color.BLACK);
            g2d.draw(new Ellipse2D.Double(x - r / 2, y - r / 2, r, r));

            if (uncoveredPoints.contains(point)) {
                g2d.setColor(Color.RED);
            } else {
                g2d.setColor(Color.GREEN);
            }
            g2d.fillOval(x - 5, y - 5, 10, 10);
        }
    }

    public static void visualize(UncoveredRegion2D ur) {
        JFrame frame = new JFrame("Uncovered Regions Visualization");
        VisualizeUncoveredRegions panel = new VisualizeUncoveredRegions(ur);
        frame.add(panel);
        frame.setSize(800, 600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}
