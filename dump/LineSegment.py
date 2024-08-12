from shapely.geometry import Point

class LineSegment:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def length(self) -> float:
        return self.start.distance_to(self.end)

    def midpoint(self) -> Point:
        mid_x = (self.start.x + self.end.x) / 2
        mid_y = (self.start.y + self.end.y) / 2
        return Point(mid_x, mid_y)

    def slope(self) -> float:
        if self.start.x == self.end.x:
            return float('inf')  # Infinite slope (vertical line)
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)

    def bisector(self) -> 'LineSegment':
        midpoint = self.midpoint()
        slope = self.slope()
        if slope == 0:  # Horizontal line
            return LineSegment(Point(midpoint.x, midpoint.y - 1), Point(midpoint.x, midpoint.y + 1))
        elif slope == float('inf'):  # Vertical line
            return LineSegment(Point(midpoint.x - 1, midpoint.y), Point(midpoint.x + 1, midpoint.y))
        else:
            perpendicular_slope = -1 / slope
            dx = 1  # Arbitrary small distance
            dy = perpendicular_slope * dx
            return LineSegment(Point(midpoint.x - dx, midpoint.y - dy), Point(midpoint.x + dx, midpoint.y + dy))

    def __repr__(self):
        return f"LineSegment(start={self.start}, end={self.end})"
