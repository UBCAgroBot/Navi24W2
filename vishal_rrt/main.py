from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.pyplot import rcParams

# Setting up image just do one time
# image = ImageOps.grayscale(Image.open('map.png'))

# image_np = np.array(image)
# image_np = ~image_np #invert BW
# image_np[image_np > 0] = 1

# plt.set_cmap('binary')
# plt.imshow(image_np)

# np.save('map.npy', image_np)

# grid = np.load('map.npy')
# plt.imshow(grid, cmap = 'binary')
# plt.tight_layout()
# plt.show()

# Tree Node Class
class treeNode():
    def __init__(self, X, Y):
        self.X = X  # X position
        self.Y = Y  # Y position
        self.children = []
        self.parent = None

# RRT Algorithm Class
class RRTAlg():
    def __init__(self, start, goal, grid, stepSize, numIterations):
        self.randomTree = treeNode(start[0], start[1])  # Root of the tree
        self.nearestNode = None  
        self.goal = treeNode(goal[0], goal[1]) 
        self.iterations = numIterations 
        self.grid = grid  
        self.rho = stepSize 
        self.path_dist = 0 
        self.nearestDst = 1000000  
        self.numWaypoints = 0  
        self.Waypoints = []

     # Add child to tree
    def addChild(self, X, Y):
        if X == self.goal.X and Y == self.goal.Y:
            self.nearestNode.children.append(self.goal)
            self.goal.parent = self.nearestNode
        else:
            temp = treeNode(X, Y)
            self.nearestNode.children.append(temp)
            temp.parent = self.nearestNode

    # Choose point in grid randomly
    def sampleAPoint(self):
        x = random.randint(0, self.grid.shape[1] - 1)
        y = random.randint(0, self.grid.shape[0] - 1)
        return np.array([x, y])

    # Move to start toward end by a step size
    def steerToPoint(self, start, end):
        direction = end - start
        distance = np.linalg.norm(direction)
        if distance <= self.rho:
            return end
        else:
            return start + (direction / distance) * self.rho

    # Check if path between start and end has obstacle in it
    def isInObstacle(self, start, end):
        points = np.linspace(start, end, num=100)
        for point in points:
            x, y = point.astype(int)
            if self.grid[y, x] == 1:
                return True
        return False

    # Eucldian distance between node and a point
    def distance(self, node, point):
        return np.linalg.norm(np.array([node.X, node.Y]) - point)
    
    # Find nearest node from given unconnected point
    def findNearestNode(self, root, point):
        if not root:
            return
        dist = self.distance(root, point)
        if dist < self.nearestDst:
            self.nearestNode = root
            self.nearestDst = dist
        for child in root.children:
            self.findNearestNode(child, point)

    # Check if end reached
    def goalFound(self, point):
        return self.distance(self.goal, point) <= self.rho

    # Reset near values of object
    def resetNearestValues(self):
        self.nearestNode = None
        self.nearestDst = 1000000

    # Retrace path from goal to start
    def retraceRRTPath(self, goal):
        if goal is None:
            return []
        path = []
        while goal is not None:
            path.append([goal.X, goal.Y])
            goal = goal.parent
        return path[::-1]  # Reverse to get start to goal

    def RRT(self, ax):
        for _ in range(self.iterations):
            self.resetNearestValues()
            random_point = self.sampleAPoint()
            self.findNearestNode(self.randomTree, random_point)
            new_point = self.steerToPoint(np.array([self.nearestNode.X, self.nearestNode.Y]), random_point)

            if not self.isInObstacle(np.array([self.nearestNode.X, self.nearestNode.Y]), new_point):
                self.addChild(new_point[0], new_point[1])
                # Plot the new edge
                ax.plot([self.nearestNode.X, new_point[0]], [self.nearestNode.Y, new_point[1]], '-g', linewidth=0.5)
                plt.pause(0.01)

                if self.goalFound(new_point):
                    self.addChild(self.goal.X, self.goal.Y)
                    path = self.retraceRRTPath(self.goal)
                    if path:
                        path = np.array(path)
                        ax.plot(path[:, 0], path[:, 1], '-r', linewidth=2) 
                        plt.pause(0.01)
                        plt.show()
                    return path
        return None

if __name__ == '__main__':
    # Load the grid map
    grid = np.load('vishal_rrt/map.npy')
    start = np.array([random.randint(0, 200), random.randint(0, 600)])
    end = np.array([random.randint(800, 900), random.randint(0, 600)])
    numIter = 400
    stepSize = 50

    # Initialize the plot
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap="binary")
    ax.plot(start[0], start[1], 'ro')
    ax.plot(end[0], end[1], 'bo')
    plt.tight_layout()

    rrt = RRTAlg(start, end, grid, stepSize, numIter)
    path = rrt.RRT(ax)