# Rapidly-Exploring Random Tree (RRT) for Ackerman Steering Vehicles

## Overview

This document outlines an implementation of the RRT algorithm for a robot with **Ackerman Steering**. Ackerman steering involves nonholonomic constraints, meaning the robot can only move forward or backward and turn within a defined turning radius.

- Potential Usage From this [Github Repo](https://github.com/ehvenimunis/Ackerman-Vehicle-Simple-Navigation), that even consists of Gazebo
- Other useful [Github Repo](https://github.com/adarsh2798/Fast-RRT-for-motion-planning-of-autonomous-vehicles) about Ackerman algorithm
- [Research Document](https://docs.google.com/document/d/1w6LAwQoav9d1Kn71S3fcBDMe9Q68AOpas56-qQEHq1k/edit?usp=sharing)

---

## Python Script

## How the Script Works

### 1. **Initialization**
The `AckermanRRT` class initializes parameters required for path planning:
- **Start/Goal Points**: Defined in `(x, y, theta)` format.
- **Obstacles**: A list of rectangular boundaries.
- **Bounds**: The operational area.
- **Step Size**: Maximum step the robot can take per iteration.
- **Wheelbase**: Distance between the front and rear axles.
- **Turning Radius**: Minimum turning radius based on the vehicle's geometry.

```python
ackerman_rrt = AckermanRRT(
    start=(10, 10, 0), 
    goal=(90, 90, 0), 
    obstacles=[(30, 30, 40, 70), (60, 20, 70, 50)], 
    bounds=(0, 0, 100, 100)
)
```

---

### 2. **Core Functions**

#### `distance(p1, p2)`
Calculates the Euclidean distance between two points, ignoring the heading (`theta`).

#### `sample_point()`
Generates random samples within the bounds for exploration.

#### `nearest_neighbor(point)`
Finds the closest existing tree node to the sampled point.

#### `is_collision(p1, p2)`
Checks if the straight line between two points collides with any obstacle.

#### `steer(p1, p2)`
Computes the new position based on Ackerman steering constraints:
- Aligns the vehicle toward the target within the allowable turning angle.
- Moves the vehicle by the specified step size.

#### `plan()`
Performs the RRT planning:
- Randomly samples points within bounds.
- Expands the tree toward sampled points, checking for collisions.
- Stops if the goal is reached within the allowable distance.

#### `plot()`
Visualizes the generated path, obstacles, and tree structure:
- Obstacles are gray rectangles.
- Tree edges are blue lines.
- Start and goal points are marked green and blue, respectively.

---

## Testing the Script

### Example Test Code

- Run it using `python test_ackerman_rrt.py`

```python
from ackerman_rrt import AckermanRRT

start = (10, 10, 0)
goal = (90, 90, 0)
obstacles = [
    (20, 0, 40, 90),
    (60, 10, 80, 100)
]
bounds = (0, 0, 100, 100)

ackerman_rrt = AckermanRRT(start=start, goal=goal, obstacles=obstacles, bounds=bounds, step_size=5, max_iter=2000)

if ackerman_rrt.plan():
    print("Path found!")
else:
    print("No path found.")

ackerman_rrt.plot()
```

---

## Explanation of Parameters

- **Start/Goal**: `(x, y, theta)` specifies the robot's initial and final positions with heading angles.
- **Obstacles**: Rectangular regions represented by `(x_min, y_min, x_max, y_max)`.
- **Bounds**: `(x_min, y_min, x_max, y_max)` specifies the operational area.
- **Step Size**: Controls how far the robot moves in one step.
- **Wheelbase**: Impacts the turning constraints.
- **Turning Radius**: Sets the minimum turning radius for realistic steering.

---

## Visualization

The visualization uses `matplotlib` to show:
1. Obstacles as gray rectangles.
2. Tree edges as blue lines.
3. Start and goal points as green and blue dots, respectively.

---

## Key Notes

1. **Collision Detection**:
   - Ensures the path does not intersect obstacles.
   - Each line segment connecting tree nodes is checked.

2. **Steering Limitations**:
   - The steering angle is constrained to ensure realistic turning.

3. **Goal Bias**:
   - The goal is prioritized as the tree grows to improve convergence.

4. **Performance**:
   - Increasing `max_iter` improves the chance of finding a path but increases computation time.

---

## Applications

1. **Autonomous Vehicles**:
   - Navigation in cluttered environments.

2. **Mobile Robots**:
   - Pathfinding for robots with nonholonomic constraints.

3. **Planning and Simulation**:
   - Testing different environments and obstacle arrangements.

---

## Future Enhancements

1. **Path Smoothing**:
   - Use splines or Bézier curves to optimize the planned path.

2. **Dynamic Obstacles**:
   - Incorporate real-time updates to handle moving obstacles.

3. **Multi-Agent Systems**:
   - Extend the algorithm for coordinated path planning among multiple agents.

---


### Dependencies
```python
import matplotlib.pyplot as plt
import numpy as np
import random
