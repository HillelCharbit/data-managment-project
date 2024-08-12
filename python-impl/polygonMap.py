import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, MultiLineString, Point
from shapely.ops import polygonize, unary_union
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
from shapely.ops import snap
from scipy.spatial import distance

class vorCell:
    def __init__(self, polygon, points, radius=180):  # Set a default radius for circles
        self.polygon = polygon
        self.points = points
        self.circles = [Point(point).buffer(radius) for point in points]

def cellPointsFinder(polygon, points):
    point = find_point_in_polygon(polygon)
    distances = [distance.euclidean((p[0], p[1]), (point.x, point.y)) for p in points]
    closest_indices = np.argsort(distances)[:2]
    return [points[closest_indices[0]], points[closest_indices[1]]]

def find_polygons_from_lines(lines, bbox):
    bbox_lines = [
        LineString([(bbox[0], bbox[1]), (bbox[2], bbox[1])]),  # Bottom
        LineString([(bbox[2], bbox[1]), (bbox[2], bbox[3])]),  # Right
        LineString([(bbox[2], bbox[3]), (bbox[0], bbox[3])]),  # Top
        LineString([(bbox[0], bbox[3]), (bbox[0], bbox[1])])   # Left
    ]
    lines.extend(bbox_lines)
    
    multiline = MultiLineString(lines)
    snapped_multiline = snap(multiline, multiline, tolerance=1e-8)
    merged_lines = unary_union(snapped_multiline)
    polygons = list(polygonize(merged_lines))
    
    return polygons

def find_point_in_polygon(polygon):
    centroid = polygon.centroid
    if polygon.contains(centroid):
        return centroid
    else:
        return polygon.representative_point()

bbox = [0, 0, 800, 600]
points = [[92, 129], [477, 471], [323, 186], [554, 300], [708, 414]]

lines = [
    LineString([(98, 600), (129, 475)]),
    LineString([(296, 287), (402, 0)]),
    LineString([(129, 475), (296, 287)]),
    LineString([(262, 600), (395, 331)]),
    LineString([(0, 545), (129, 475)]),
    LineString([(395, 331), (545, 250)]),
    LineString([(545, 250), (693, 0)]),
    LineString([(296, 287), (395, 331)]),
    LineString([(586, 417), (800, 514)]),
    LineString([(451, 600), (586, 417)]),
    LineString([(545, 250), (586, 417)])
]

polygons = find_polygons_from_lines(lines, bbox)

vorCells = []
for polygon in polygons:
    cellPoints = cellPointsFinder(polygon, points)
    vorCells.append(vorCell(polygon, cellPoints))

fig, ax = plt.subplots()

for cell in vorCells:
    exterior_coords = np.array(cell.polygon.exterior.coords)
    mpl_poly = MplPolygon(exterior_coords, closed=True, edgecolor='black', facecolor='red', alpha=0.3)
    ax.add_patch(mpl_poly)
    
    plt.draw()  # Refresh the plot
    plt.pause(0.1)  # Pause to allow the update to be visible
    
    if len(cell.circles) > 1:
        ax.plot(*cell.circles[0].exterior.xy, color='black', linewidth=0.8, alpha=0.8)
        ax.plot(*cell.circles[1].exterior.xy, color='black', linewidth=0.8, alpha=0.8)
        
        intersection = cell.circles[0].intersection(cell.circles[1])
        if not intersection.is_empty:
            if isinstance(intersection, MultiLineString):  # Handle complex intersections
                for geom in intersection.geoms:
                    x, y = geom.exterior.xy
                    ax.fill(x, y, color='green', alpha=1)
            else:
                x, y = intersection.exterior.xy
                ax.fill(x, y, color='green', alpha=1)
        
        plt.draw()  # Refresh the plot
        plt.pause(0.5)  # Pause to allow the update to be visible

plt.xlim(0, 800)
plt.ylim(0, 600)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
