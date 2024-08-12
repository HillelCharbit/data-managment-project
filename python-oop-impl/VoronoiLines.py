import numpy as np
import matplotlib.pyplot as plt      
from shapely.geometry import LineString, MultiLineString
from shapely.ops import polygonize, unary_union, snap


class Hivoro:
    def __init__(self, data, order, width=800, height=800):
        self.data = data
        self.background_color = 'black'
        self.text_color = 'yellow'
        self.line_colors = ['green', 'white', '#c76fee']
        self.width = width
        self.height = height
        self.num_points = len(data)
        self.lines = []
        self.order = order - 1

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
                            if slope2 != slope4:  # Ensure no division by zero
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
                        if closer_points_count == self.order:
                            ax.plot([x1_int, x2_int], [y1_int, y2_int], color=self.line_colors[closer_points_count])
                            self.lines.append([x1_int, y1_int, x2_int, y2_int])

        plt.show()
    
    def get_lines(self):
        lines = []
        for line in self.lines:
            lines.append(LineString([line[:2], line[2:]]))
    
        return lines
    
    @staticmethod
    def find_polygons_from_lines(lines, bbox):
        # Step 1: Add bounding box lines
        bbox_lines = [
            LineString([(bbox[0], bbox[1]), (bbox[2], bbox[1])]),  # Bottom
            LineString([(bbox[2], bbox[1]), (bbox[2], bbox[3])]),  # Right
            LineString([(bbox[2], bbox[3]), (bbox[0], bbox[3])]),  # Top
            LineString([(bbox[0], bbox[3]), (bbox[0], bbox[1])])   # Left
        ]
    
        # Combine the Voronoi lines with the bounding box lines
        combined_lines = unary_union(MultiLineString(lines + bbox_lines))
    
        # Step 2: Find polygons from lines
        polygons = list(polygonize(combined_lines))
    
        return polygons
