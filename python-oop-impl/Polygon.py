import numpy as np
from matplotlib.patches import Polygon as MplPolygon
from shapely.geometry import Point
from scipy.spatial import distance

class Polygon(MplPolygon):
    def __init__(self, vertices: np.ndarray, **kwargs):
        # Convert numpy array to a list of Points
        points = [Point(xy) for xy in vertices]
        xy = [(point.x, point.y) for point in points]
        super().__init__(xy, **kwargs)
        self.vertices = points

    def contains_point(self, point: Point) -> bool:
        # Ray-casting algorithm for point-in-polygon
        n = len(self.vertices)
        inside = False
        x, y = point.x, point.y
        p1x, p1y = self.vertices[0].x, self.vertices[0].y
        for i in range(n + 1):
            p2x, p2y = self.vertices[i % n].x, self.vertices[i % n].y
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
    
    @staticmethod
    def cell_points_finder(polygon, points, order):
        # point = polygon.centroid
        point = polygon.representative_point()
        distances = [distance.euclidean((p[0], p[1]), (point.x, point.y)) for p in points]
        closest_indices = np.argsort(distances)[:order]
        return [points[i] for i in closest_indices]

    def __repr__(self):
        return f"Polygon(vertices={self.vertices})"
