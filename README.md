
# Voronoi Unrepresented Data Identifier

This project identifies unrepresented (uncovered) data regions using Voronoi diagrams, aiming to enhance machine learning models through comprehensive data coverage. By detecting gaps in data representation, this tool helps improve model performance through strategic data augmentation.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Class Descriptions](#class-descriptions)
6. [License](#license)

---

### Introduction

The **Voronoi Unrepresented Data Identifier** is a data management tool designed to analyze and detect gaps in data representation within a given dataset. Utilizing Voronoi diagrams, this tool identifies areas where additional data collection could significantly enhance machine learning model performance.

### Features

- **Voronoi Diagram Generation**: Generate Voronoi diagrams to visualize data distribution.
- **Unrepresented Region Detection**: Identify regions lacking sufficient data representation.
- **Data Visualization**: Display Voronoi diagrams and highlight unrepresented regions for easy analysis.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/HillelCharbit/voronoi-coverage-identifier.git
   ```

### Usage

After installation, you can run the project using:
```bash
python main.py
```
This command will initiate the Voronoi diagram generation process and identify unrepresented data regions within your dataset.

### Class Descriptions

#### Main

The **Main** class manages the workflow, executing Voronoi diagram generation and unrepresented region detection.

#### DataManager

Handles data input and management, organizing datasets for analysis.

#### Polygon

The **Polygon** class represents polygons formed from Voronoi cells and provides methods for geometric operations on these polygons.

#### VorCell

Manages individual Voronoi cells, including their creation and the calculation of unrepresented regions within each cell.

#### VoronoiLines

Processes datasets to prepare them for Voronoi diagram generation.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 

---
