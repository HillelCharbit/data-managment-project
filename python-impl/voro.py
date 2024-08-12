import numpy as np
import pandas as pd
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
from scipy.spatial import voronoi_plot_2d


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
k = 10  # Number of lines to read
    
# Load the CSV file without headers
data = pd.read_csv(csv_file, header=None)
# Select the first k rows and the first two columns (longitude and latitude)
data = data.iloc[:k, :2]
# Normalize the data
data = normalize_data(data.to_numpy())
    
# Create a Voronoi object
vor = Voronoi(data)
vertices = vor.vertices
cells = vor.regions
print(vertices)
print(cells)

plot = voronoi_plot_2d(vor)
plt.show()