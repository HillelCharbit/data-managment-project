import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import LineString, MultiLineString
from shapely.ops import polygonize, unary_union
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
from shapely.ops import snap

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

# Define the bounding box (xmin, ymin, xmax, ymax)
bbox = [0, 0, 800, 600]

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
