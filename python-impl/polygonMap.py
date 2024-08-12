import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon as MplPolygon
from shapely.geometry import Point


class vorCell:
    def __init__(self, polygon, points, radius=180):  # Set a default radius for circles
        self.polygon = polygon
        self.points = points
        self.circles = [Point(point).buffer(radius) for point in points]

# Define vertices for each polygon
vertices_p1 = np.array([[0, 545], [0, 600], [98, 600], [129, 475]])
vertices_p2 = np.array([[0, 0], [0, 545], [129, 475], [296, 287], [402, 0]])
vertices_p3 = np.array([[98, 600], [262, 600], [395, 331], [296, 287], [129, 475]])
vertices_p4 = np.array([[262, 600], [451, 600], [586, 417], [545, 250], [395, 331]])
vertices_p5 = np.array([[296, 287], [395, 331], [545, 250], [693, 0], [402, 0]])
vertices_p6 = np.array([[451, 600], [800, 600], [800, 514], [586, 417]])
vertices_p7 = np.array([[545, 250], [586, 417], [800, 514], [800, 0], [693, 0]])

# Create Polygon objects with 'closed' parameter as a keyword argument
polygon1 = MplPolygon(vertices_p1, closed=True, edgecolor='black', facecolor='red', alpha=0.3)
points1 = np.array([[92, 129], [477, 471]])
polygon2 = MplPolygon(vertices_p2, closed=True, edgecolor='black', facecolor='red', alpha=0.3)
points2 = np.array([[92, 129], [323, 186]])
polygon3 = MplPolygon(vertices_p3, closed=True, edgecolor='black', facecolor='red', alpha=0.3)
points3 = np.array([[323, 186], [477, 471]])
polygon4 = MplPolygon(vertices_p4, closed=True, edgecolor='black', facecolor='red', alpha=0.3)
points4 = np.array([[477, 471], [554, 300]])
polygon5 = MplPolygon(vertices_p5, closed=True, edgecolor='black', facecolor='red', alpha=0.3)
points5 = np.array([[323, 186], [554, 300]])
polygon6 = MplPolygon(vertices_p6, closed=True, edgecolor='black', facecolor='red', alpha=0.3)
points6 = np.array([[477, 471], [554, 300]])
polygon7 = MplPolygon(vertices_p7, closed=True, edgecolor='black', facecolor='red', alpha=0.3)
points7 = np.array([[554, 300], [708, 414]])

# Create a list of vorCell objects
vorCells = [
    vorCell(polygon1, points1),
    vorCell(polygon2, points2),
    vorCell(polygon3, points3),
    vorCell(polygon4, points4),
    vorCell(polygon5, points5),
    vorCell(polygon6, points6),
    vorCell(polygon7, points7)
]

# Create a plot and add the polygons, circles, and points
fig, ax = plt.subplots()

for cell in vorCells:
    ax.add_patch(cell.polygon)
    
    if len(cell.circles) > 1:
        # Draw the circumferences of both circles with black edges and reduced thickness
        ax.plot(*cell.circles[0].exterior.xy, color='black', linewidth=0.8, alpha=0.8)
        ax.plot(*cell.circles[1].exterior.xy, color='black', linewidth=0.8, alpha=0.8)
        
        # Find and fill the intersection of the two circles
        intersection = cell.circles[0].intersection(cell.circles[1])
        if not intersection.is_empty:
            x, y = intersection.exterior.xy
            ax.fill(x, y, color='green', alpha=1)

# Set limits and aspect ratio
plt.xlim(0, 800)
plt.ylim(0, 600)
plt.gca().set_aspect('equal', adjustable='box')

# Show the plot
plt.show()
