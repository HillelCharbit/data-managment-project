import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
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
    # Step 1: Add bounding box lines
    bbox_lines = [
        LineString([(bbox[0], bbox[1]), (bbox[2], bbox[1])]),  # Bottom
        LineString([(bbox[2], bbox[1]), (bbox[2], bbox[3])]),  # Right
        LineString([(bbox[2], bbox[3]), (bbox[0], bbox[3])]),  # Top
        LineString([(bbox[0], bbox[3]), (bbox[0], bbox[1])])   # Left
    ]
    lines.extend(bbox_lines)
    
    # Step 2: Combine all line segments into a MultiLineString
    multiline = MultiLineString(lines)

    # Step 3: Snap the lines together to fix small precision issues
    snapped_multiline = snap(multiline, multiline, tolerance=1e-8)

    # Step 4: Perform unary_union to merge any overlapping geometries and to find intersections
    merged_lines = unary_union(snapped_multiline)

    # Step 5: Calculate the polygons using polygonize
    polygons = list(polygonize(merged_lines))
    
    return polygons

def find_point_in_polygon(polygon):
    """
    Returns a point inside the given polygon. 
    The centroid is used as the point inside the polygon.
    """
    # Calculate the centroid
    centroid = polygon.centroid
    
    # Check if the centroid is inside the polygon
    if polygon.contains(centroid):
        return centroid
    else:
        # If not, use another method, like taking a vertex or an interior point
        return polygon.representative_point()  # Guaranteed to be inside the polygon

# Define the bounding box (xmin, ymin, xmax, ymax)
bbox = [0, 0, 800, 600]

points = [[92, 129], [477, 471], [323, 186], [554, 300], [708, 414]]

# Using your specific set of lines:
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

# Check how many polygons were detected
print(f"Number of polygons found: {len(polygons)}")

# Display results
for i, poly in enumerate(polygons, 1):
    print(f"Polygon {i}: {poly}")

# Visualization
fig, ax = plt.subplots()
patches = []

for poly in polygons:
    exterior_coords = np.array(poly.exterior.coords)
    mpl_poly = MplPolygon(exterior_coords, closed=True)
    patches.append(mpl_poly)

p = PatchCollection(patches, alpha=0.5, edgecolor='black')
ax.add_collection(p)

# Plot the original lines for reference
for line in lines:
    x, y = line.xy
    ax.plot(x, y, color='blue')

# Adjust the limits according to your data
ax.set_xlim(0, 800)
ax.set_ylim(0, 600)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

# Create a plot and add the polygons, circles, and points
fig, ax = plt.subplots()

for cell in vorCells:
    # Convert Shapely polygon to Matplotlib patch
    exterior_coords = np.array(cell.polygon.exterior.coords)
    mpl_poly = MplPolygon(exterior_coords, closed=True, edgecolor='black', facecolor='none')
    ax.add_patch(mpl_poly)
    
    if len(cell.circles) > 1:
        # Draw the circumferences of both circles with black edges and reduced thickness
        ax.plot(*cell.circles[0].exterior.xy, color='black', linewidth=0.8, alpha=0.8)
        ax.plot(*cell.circles[1].exterior.xy, color='black', linewidth=0.8, alpha=0.8)
        
        # Find and fill the intersection of the two circles
        intersection = cell.circles[0].intersection(cell.circles[1])
        if not intersection.is_empty:
            if isinstance(intersection, MultiLineString):  # Handle case where intersection is complex
                for geom in intersection.geoms:
                    x, y = geom.exterior.xy
                    ax.fill(x, y, color='green', alpha=1)
            else:
                x, y = intersection.exterior.xy
                ax.fill(x, y, color='green', alpha=1)

# Set limits and aspect ratio
plt.xlim(0, 800)
plt.ylim(0, 600)
plt.gca().set_aspect('equal', adjustable='box')

# Show the plot
plt.show()
