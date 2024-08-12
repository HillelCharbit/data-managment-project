from shapely.geometry import Point
from Polygon import Polygon


class VorCell:
    def __init__(self, polygon: Polygon, points: list[Point], rho: float, width = 800):
        """
        Initialize the Voronoi cell with a polygon and associated points.
        
        :param polygon: The polygon representing the Voronoi cell.
        :param points: A list of points associated with the cell.
        :param rho: The rho for generating circles around the points
        """
        self.polygon = polygon
        self.points = points
        self.rho = width*rho
        self.circles = [Point(point).buffer(self.rho) for point in points]

    
    def contains_point(self, point: Point) -> bool:
        """
        Check if a point is contained within the Voronoi cell.

        :param point: The point to check.
        :return: True if the point is inside the polygon, False otherwise.
        """
        return self.polygon.contains(point)

    def __repr__(self):
        return f"vorCell(polygon={self.polygon}, points={self.points})"
