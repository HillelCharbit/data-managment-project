import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.spatial import voronoi_plot_2d
from scipy.spatial import Voronoi
from shapely.geometry import Point, Polygon
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection

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

csv_file = "C:\\Users\\ASUS\\Downloads\\Food_Inspections_-_1_1_2010_-_6_30_2018_20240704.csv"
k = 50  # Number of lines to read
    
# Load the CSV file without headers
data = pd.read_csv(csv_file, header=None)
# Select the first k rows and the first two columns (longitude and latitude)
data = data.iloc[:k, :2]
# Normalize the data
data = normalize_data(data.to_numpy())
    
# Create a Voronoi object
vor = Voronoi(data)

# Initialize a plot
fig, ax = plt.subplots()

# List to store Matplotlib polygons
mpl_polygons = []

# Iterate over the Voronoi regions
for region_index in vor.point_region:
    region = vor.regions[region_index]
    
    if not region or -1 in region:
        continue  # Skip empty regions and those with points at infinity

    # Get the coordinates of the Voronoi vertices for this region
    polygon = Polygon([vor.vertices[i] for i in region])
    
    # Convert the Shapely polygon to a Matplotlib Polygon
    mpl_polygon = MplPolygon(np.array(polygon.exterior.coords), closed=True)
    mpl_polygons.append(mpl_polygon)

# Add the Voronoi polygons to the plot
p = PatchCollection(mpl_polygons, edgecolor='black', facecolor='none', linewidths=1)
ax.add_collection(p)

# Plot the original points
ax.plot(data[:, 0], data[:, 1], 'ro')

# Set the limits for the plot
ax.set_xlim(vor.min_bound[0] - 0.1, vor.max_bound[0] + 0.1)
ax.set_ylim(vor.min_bound[1] - 0.1, vor.max_bound[1] + 0.1)

# Display the plot
plt.show()



