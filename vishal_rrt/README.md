# Rapidly-Exploring Random Tree (RRT) Algorithm

This repository contains a Python implementation of the Rapidly-Exploring Random Tree (RRT) algorithm for pathfinding in a grid-based environment. The algorithm is designed to efficiently navigate through complex spaces while avoiding obstacles.

## Features

- **Grid-Based Navigation**: Uses a binary grid map to represent free and occupied spaces.
- **Obstacle Avoidance**: Ensures paths do not intersect with obstacles.
- **Tree Expansion**: Dynamically grows a tree towards random points while respecting step size constraints.
- **Path Retracing**: Computes the path from the start point to the goal point if a solution is found.
- **Visualization**: Displays the tree expansion process and the final path using matplotlib.

## Prerequisites

To run the code, you'll need the following Python libraries installed:

- `numpy`
- `matplotlib`
- `Pillow`

Install them using pip:

```bash
pip install numpy matplotlib pillow
```

## Getting Started

### 1. Prepare the Grid Map

The grid map represents the environment with obstacles and free space. To set up the map:

1. Place a binary image (`map.png`) in the working directory, where white represents free space and black represents obstacles.
2. Run the following snippet (uncomment the relevant lines in the code):

```python
from PIL import Image, ImageOps
import numpy as np

image = ImageOps.grayscale(Image.open('map.png'))
image_np = np.array(image)
image_np = ~image_np  # Invert black and white
image_np[image_np > 0] = 1
np.save('map.npy', image_np)
```

This will create a `map.npy` file representing the grid.

### 2. Configure the Algorithm

Modify the following parameters in the main script:

- `start`: Starting coordinates (randomly selected by default).
- `end`: Goal coordinates (randomly selected by default).
- `stepSize`: Maximum step size for each tree expansion.
- `numIter`: Maximum number of iterations for tree expansion.

### 3. Run the Script

Execute the script:

```bash
python rrt_algorithm.py
```

The script will:

1. Load the grid map from `map.npy`.
2. Visualize the tree expansion process.
3. Plot the final path if the goal is reached.

## Code Overview

### Classes

1. **`treeNode`**
   - Represents a node in the RRT tree.
   - Stores position (`X`, `Y`), parent, and children.

2. **`RRTAlg`**
   - Implements the RRT algorithm.
   - Key methods:
     - `sampleAPoint()`: Samples a random point in the grid.
     - `steerToPoint()`: Moves a step closer to the sampled point.
     - `isInObstacle()`: Checks if a path intersects obstacles.
     - `findNearestNode()`: Finds the closest node in the tree to a point.
     - `retraceRRTPath()`: Traces the path from the goal back to the start.
     - `RRT()`: Main loop for the RRT algorithm.

### Visualization

- Start and goal points are marked with red and blue dots, respectively.
- Tree edges are plotted in green.
- The final path, if found, is highlighted in red.

## Example Output
