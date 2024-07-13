import java.awt.geom.Point2D;
import java.util.ArrayList;
import java.util.List;

public class VoronoiCell {
    private List<Point2D> vertices;

    public VoronoiCell() {
        vertices = new ArrayList<>();
    }

    public void addVertex(Point2D vertex) {
        vertices.add(vertex);
    }

    public List<Point2D> getVertices() {
        return vertices;
    }
}
