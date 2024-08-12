import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from shapely.geometry import MultiLineString

from DataManager import DataManager 
from VoronoiLines import Hivoro  
from VorCell import VorCell  
from Polygon import Polygon  

if __name__ == "__main__":
    csv_file = "C:\\Users\\ASUS\\Downloads\\Food_Inspections_-_1_1_2010_-_6_30_2018_20240704.csv"
    num_points = 50  # Number of lines to read
    rho = 0.1  # Threshold for coverage
    order = 2  # Order of Voronoi, number of points to cover
    frame_width = 800
    frame_height = 800
    
    data_manager = DataManager(csv_file, num_points)  # Instantiate the DataManager class with 'n' as order
    data = data_manager.normalize_data()

    hivoro = Hivoro(data, order)  
    
    hivoro.plot()
    lines = hivoro.get_lines()
    
    # Define the bounding box (xmin, ymin, xmax, ymax)
    bbox = [0, 0, frame_width, frame_height]
    polygons = hivoro.find_polygons_from_lines(lines, bbox)
    
    points = data_manager.frame_normalization(data, frame_width, frame_height)
    vorCells = []
    for polygon in polygons:
        cellPoints = Polygon.cell_points_finder(polygon, points, order)
        vorCells.append(VorCell(polygon, cellPoints, rho))
        
    # Create a plot and add the polygons, circles, and points
    fig, ax = plt.subplots()

    for cell in vorCells:
        # Convert Shapely polygon to Matplotlib patch
        exterior_coords = np.array(cell.polygon.exterior.coords)
        mpl_poly = Polygon(exterior_coords, closed=True, edgecolor='black', facecolor='red', alpha=0.3)
        ax.add_patch(mpl_poly)
        
        # Draw the circumferences of all circles with black edges and reduced thickness
        for circle in cell.circles:
            ax.plot(*circle.exterior.xy, color='black', linewidth=0.8, alpha=0.8)
        
        # Handle intersections of k-order circles
        if len(cell.circles) >= order:
            intersection = cell.circles[0]
            for i in range(1, order):
                intersection = intersection.intersection(cell.circles[i])
            
            if not intersection.is_empty:
                if isinstance(intersection, MultiLineString):  # Handle case where intersection is complex
                    for geom in intersection.geoms:
                        x, y = geom.exterior.xy
                        ax.fill(x, y, color='green', alpha=1)
                else:
                    x, y = intersection.exterior.xy
                    ax.fill(x, y, color='green', alpha=1)
                    
        plt.draw()  # Refresh the plot
        plt.pause(0.1)  # Pause to allow the update to be visible
                    
    # Set limits and aspect ratio
    plt.xlim(0, frame_width)
    plt.ylim(0, frame_height)
    plt.gca().set_aspect('equal', adjustable='box')

    # Show the plot
    plt.show()
    print("Done")