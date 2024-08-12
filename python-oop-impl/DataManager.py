import pandas as pd

class DataManager:
    def __init__(self, filepath: str, num_points: int):
        self.filepath = filepath
        self.num_points = num_points  # Assign num_points first
        self.data = self.load_data()  # Load data using the num_points attribute

    def load_data(self):
        # Load the CSV file without headers
        data = pd.read_csv(self.filepath, header=None)
        # Select the first n rows and the first two columns (longitude and latitude)
        data = data.iloc[:self.num_points, :2]
        return data.to_numpy()

    def normalize_data(self):
        if len(self.data) == 0:
            return []  # Handle empty data case with consistent return type
        
        # Initialize an empty list to store normalized data
        normalized_data = []

        # Min and max values for x and y (longitude and latitude)
        min_x = 41.64467013
        max_x = 42.02106425
        min_y = -87.90687413
        max_y = -87.52509414

        # Normalize each point in data
        for i in range(len(self.data)):
            normalized_x = (self.data[i][0] - min_x) / (max_x - min_x)  # Normalize x
            normalized_y = (self.data[i][1] - min_y) / (max_y - min_y)  # Normalize y
            normalized_data.append([normalized_x, normalized_y])
            
        return normalized_data
    @staticmethod
    def frame_normalization(data, width, height):
        if len(data) == 0:
            return []  # Handle empty data case with consistent return type
        
        frame_normalized_data = []
        for i in range(len(data)):
            x = data[i][0] * (width - 30) + 15
            y = data[i][1] * (height - 30) + 15
            frame_normalized_data.append((x, y))
        return frame_normalized_data

    def __repr__(self):
        return f"DataManager(filepath='{self.filepath}', num_points={len(self.data)}, num_points={self.num_points})"
