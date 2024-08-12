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
import pandas as pd

class Hivoro:
    def __init__(self, data):
        self.data = data
        self.background_color = 'black'
        self.text_color = 'yellow'
        self.line_colors = ['green', 'white', '#c76fee']
        self.width = 800
        self.height = 600
        self.num_points = len(data)
        self.lines = []

        self.x_coords = np.zeros(100000)
        self.y_coords = np.zeros(100000)
        self.x_int_coords = np.zeros(100000, dtype=int)
        self.y_int_coords = np.zeros(100000, dtype=int)
        self.distances = np.zeros(100000)
        self.bisector_x = np.zeros(100000)
        self.bisector_y = np.zeros(100000)
        self.unused = np.zeros(100000)

        for k in range(self.num_points):
            self.x_coords[k] = data[k][0] * (self.width - 30) + 15
            self.y_coords[k] = data[k][1] * (self.height - 30) + 15
            self.x_int_coords[k] = int(self.x_coords[k] + 0.5)
            self.y_int_coords[k] = int(self.y_coords[k] + 0.5)
            self.distances[k] = np.sqrt(self.x_coords[k] ** 2 + self.y_coords[k] ** 2)

        self.heap_sort(self.distances, self.x_coords, self.y_coords, self.num_points)

    def heap_sort(self, arr1, arr2, arr3, size):
        def heapify(arr1, arr2, arr3, n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2
            if l < n and arr1[i] < arr1[l]:
                largest = l
            if r < n and arr1[largest] < arr1[r]:
                largest = r
            if largest != i:
                arr1[i], arr1[largest] = arr1[largest], arr1[i]
                arr2[i], arr2[largest] = arr2[largest], arr2[i]
                arr3[i], arr3[largest] = arr3[largest], arr3[i]
                heapify(arr1, arr2, arr3, n, largest)

        for i in range(size // 2 - 1, -1, -1):
            heapify(arr1, arr2, arr3, size, i)

        for i in range(size - 1, 0, -1):
            arr1[i], arr1[0] = arr1[0], arr1[i]
            arr2[i], arr2[0] = arr2[0], arr2[i]
            arr3[i], arr3[0] = arr3[0], arr3[i]
            heapify(arr1, arr2, arr3, i, 0)

    def plot(self):
        fig, ax = plt.subplots()
        ax.set_facecolor(self.background_color)
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)

        ax.scatter(self.x_int_coords[:self.num_points], self.y_int_coords[:self.num_points], color=self.text_color)

        for i in range(1, self.num_points):
            for j in range(i + 1, self.num_points + 1):
                delta_x = self.x_coords[i - 1] - self.x_coords[j - 1]
                if delta_x == 0:
                    continue  # Skip this pair if the x-coordinates are the same

                slope1 = (self.y_coords[i - 1] - self.y_coords[j - 1]) / delta_x
                slope2 = -1 / slope1
                mid_y = (self.y_coords[i - 1] + self.y_coords[j - 1]) / 2
                mid_x = (self.x_coords[i - 1] + self.x_coords[j - 1]) / 2
                y_intercept = mid_y - mid_x * slope2
                
                if 0 < y_intercept < self.height:
                    x0, y0 = 0, y_intercept
                elif slope2 > 0:
                    x0, y0 = -y_intercept / slope2, 0
                else:
                    x0, y0 = (self.height - y_intercept) / slope2, self.height

                y_max = slope2 * self.width + y_intercept
                if 0 < y_max < self.height:
                    x_end, y_end = self.width, y_max
                elif slope2 > 0:
                    x_end, y_end = (self.height - y_intercept) / slope2, self.height
                else:
                    x_end, y_end = -y_intercept / slope2, 0

                l = 1
                self.bisector_x[l - 1], self.bisector_y[l - 1] = x0, y0

                for k in range(1, self.num_points + 1):
                    if k != i and k != j:
                        delta_x_k = self.x_coords[i - 1] - self.x_coords[k - 1]
                        if delta_x_k == 0:
                            continue  # Skip this pair if the x-coordinates are the same

                        slope3 = (self.y_coords[i - 1] - self.y_coords[k - 1]) / delta_x_k
                        slope4 = -1 / slope3
                        mid_y3 = (self.y_coords[i - 1] + self.y_coords[k - 1]) / 2
                        mid_x3 = (self.x_coords[i - 1] + self.x_coords[k - 1]) / 2
                        y_intercept3 = mid_y3 - mid_x3 * slope4
                        y_at_x0 = slope4 * x0 + y_intercept3
                        y_at_x_end = slope4 * x_end + y_intercept3
                        sign1 = y0 - y_at_x0
                        sign2 = y_end - y_at_x_end
                        if sign1 * sign2 < 0:
                            l += 1
                            self.bisector_x[l - 1] = (y_intercept3 - y_intercept) / (slope2 - slope4)
                            self.bisector_y[l - 1] = slope2 * self.bisector_x[l - 1] + y_intercept

                l += 1
                self.bisector_x[l - 1], self.bisector_y[l - 1] = x_end, y_end

                self.heap_sort(self.bisector_x, self.bisector_y, self.unused, l)

                for k in range(1, l):
                    next_ = k + 1
                    mid_x_bisector = (self.bisector_x[k - 1] + self.bisector_x[next_ - 1]) / 2
                    mid_y_bisector = slope2 * mid_x_bisector + y_intercept
                    mid_dist_squared = (mid_x_bisector - self.x_coords[i - 1]) ** 2 + (mid_y_bisector - self.y_coords[i - 1]) ** 2
                    closer_points_count = 0
                    for u in range(1, self.num_points + 1):
                        if u != i and u != j:
                            point_dist_squared = (mid_x_bisector - self.x_coords[u - 1]) ** 2 + (mid_y_bisector - self.y_coords[u - 1]) ** 2
                            if point_dist_squared < mid_dist_squared:
                                closer_points_count += 1
                    if closer_points_count < 3:
                        x1_int = int(self.bisector_x[k - 1] + 0.5)
                        y1_int = int(self.bisector_y[k - 1] + 0.5)
                        x2_int = int(self.bisector_x[next_ - 1] + 0.5)
                        y2_int = int(self.bisector_y[next_ - 1] + 0.5)
                        if closer_points_count == 1:
                            ax.plot([x1_int, x2_int], [y1_int, y2_int], color=self.line_colors[closer_points_count])
                            self.lines.append([x1_int, y1_int, x2_int, y2_int])

        plt.show()

def normalize_data(data):
    if len(data) == 0:
        return  # Handle empty data case

    # Find min and max values for x and y (longitude and latitude)
    min_x = 41.64467013
    max_x = 42.02106425
    min_y = -87.90687413
    max_y = -87.52509414

    # Normalize each point in data
    for i in range(len(data)):
        data[i][0] = (data[i][0] - min_x) / (max_x - min_x)  # Normalize x
        data[i][1] = (data[i][1] - min_y) / (max_y - min_y)  # Normalize y
        
    return data


class vorCell:
    def __init__(self, polygon, points, rho=50):  # Set a default rho for circles
        self.polygon = polygon
        self.points = points
        self.circles = [Point(point).buffer(rho) for point in points]
        
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

if __name__ == "__main__":
    csv_file = "C:\\Users\\ASUS\\Downloads\\Food_Inspections_-_1_1_2010_-_6_30_2018_20240704.csv"
    k = 30  # Number of lines to read
    
    # Load the CSV file without headers
    data = pd.read_csv(csv_file, header=None)
    # Select the first k rows and the first two columns (longitude and latitude)
    data = data.iloc[:k, :2]
    # Normalize the data
    data = normalize_data(data.to_numpy())
    
    
    hivoro = Hivoro(data)
    
       
    hivoro.plot()
    plt.show()
    
    lines = []
    for line in hivoro.lines:
        lines.append(LineString([line[:2], line[2:]]))
     
    # Define the bounding box (xmin, ymin, xmax, ymax)
    bbox = [0, 0, 800, 600]

    polygons = find_polygons_from_lines(lines, bbox)
    points = []
    for k in range(hivoro.num_points):
        x = data[k][0] * (hivoro.width - 30) + 15
        y = data[k][1] * (hivoro.height - 30) + 15
        points.append((x, y))
        
    vorCells = []
    for polygon in polygons:
        cellPoints = cellPointsFinder(polygon, points)
        vorCells.append(vorCell(polygon, cellPoints))
        print(polygon)
        print(cellPoints)

# Create a plot and add the polygons, circles, and points
fig, ax = plt.subplots()

for cell in vorCells:
    # Convert Shapely polygon to Matplotlib patch
    exterior_coords = np.array(cell.polygon.exterior.coords)
    mpl_poly = MplPolygon(exterior_coords, closed=True, edgecolor='black', facecolor='red', alpha=0.3)
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
