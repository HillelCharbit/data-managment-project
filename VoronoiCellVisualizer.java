import javax.swing.*;
import java.awt.*;
import java.awt.geom.Point2D;

public class VoronoiCellVisualizer extends JPanel {
    private Cell selectedCell;
    private Point2D intersectionPoint;

    public VoronoiCellVisualizer(Cell selectedCell, Point2D intersectionPoint) {
        this.selectedCell = selectedCell;
        this.intersectionPoint = intersectionPoint;
        setPreferredSize(new Dimension(800, 800));
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;

        // Fill background red
        g2d.setColor(Color.RED);
        g2d.fillRect(0, 0, getWidth(), getHeight());

        if (selectedCell != null) {
            // Draw Voronoi line in white
            g2d.setColor(Color.WHITE);
            Point2D p1 = selectedCell.getPoint1();
            Point2D p2 = selectedCell.getPoint2();
            g2d.drawLine((int) (p1.getX() * getWidth()), (int) (p1.getY() * getHeight()),
                         (int) (p2.getX() * getWidth()), (int) (p2.getY() * getHeight()));

            // Draw intersection point in green
            if (intersectionPoint != null) {
                g2d.setColor(Color.GREEN);
                int x = (int) (intersectionPoint.getX() * getWidth());
                int y = (int) (intersectionPoint.getY() * getHeight());
                g2d.fillOval(x - 5, y - 5, 10, 10); // Draw a small green circle at the intersection point
            }
        }
    }
}
