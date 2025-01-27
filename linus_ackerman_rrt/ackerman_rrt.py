import matplotlib.pyplot as plt
import numpy as np
import random

class AckermanRRT:
    def __init__(self, start, goal, obstacles, bounds, step_size=2, max_iter=1000, wheelbase=2.5, turning_radius=0.5):
        self.start = np.array(start)  # (x, y, theta)
        self.goal = np.array(goal)   # (x, y, theta)
        self.obstacles = obstacles   # List of rectangles [(x_min, y_min, x_max, y_max), ...]
        self.bounds = bounds         # (x_min, y_min, x_max, y_max)
        self.step_size = step_size   # Maximum step size
        self.max_iter = max_iter     # Max iterations
        self.wheelbase = wheelbase   # Wheelbase length
        self.turning_radius = turning_radius  # Minimum turning radius
        self.tree = [self.start]     # Tree of nodes
        self.edges = []              # Edges between nodes

    def distance(self, p1, p2):
        return np.linalg.norm(p1[:2] - p2[:2])

    def sample_point(self):
        x = random.uniform(self.bounds[0], self.bounds[2])
        y = random.uniform(self.bounds[1], self.bounds[3])
        theta = random.uniform(-np.pi, np.pi)
        return np.array([x, y, theta])

    def nearest_neighbor(self, point):
        return min(self.tree, key=lambda node: self.distance(node, point))

    def is_collision(self, p1, p2):
        for obs in self.obstacles:
            x_min, y_min, x_max, y_max = obs
            if (min(p1[0], p2[0]) <= x_max and max(p1[0], p2[0]) >= x_min and
                min(p1[1], p2[1]) <= y_max and max(p1[1], p2[1]) >= y_min):
                return True
        return False

    def steer(self, p1, p2):
        direction = (p2[:2] - p1[:2]) / self.distance(p1, p2)
        target_theta = np.arctan2(direction[1], direction[0])
        delta_theta = target_theta - p1[2]

        if abs(delta_theta) > np.pi / 4:  # Limit the steering angle
            delta_theta = np.sign(delta_theta) * np.pi / 4

        new_theta = p1[2] + delta_theta
        new_x = p1[0] + self.step_size * np.cos(new_theta)
        new_y = p1[1] + self.step_size * np.sin(new_theta)

        return np.array([new_x, new_y, new_theta])

    def plan(self):
        for _ in range(self.max_iter):
            rand_point = self.sample_point()
            nearest = self.nearest_neighbor(rand_point)
            new_point = self.steer(nearest, rand_point)

            if not self.is_collision(nearest, new_point):
                self.tree.append(new_point)
                self.edges.append((nearest, new_point))

                if self.distance(new_point, self.goal) < self.step_size:
                    self.tree.append(self.goal)
                    self.edges.append((new_point, self.goal))
                    return True
        return False

    def plot(self):
        plt.figure(figsize=(10, 10))
        for obs in self.obstacles:
            x_min, y_min, x_max, y_max = obs
            plt.gca().add_patch(plt.Rectangle((x_min, y_min), x_max-x_min, y_max-y_min, color="gray"))

        for edge in self.edges:
            p1, p2 = edge
            plt.plot([p1[0], p2[0]], [p1[1], p2[1]], "b")

        plt.scatter(*zip(*[node[:2] for node in self.tree]), s=10, c="red")
        plt.scatter(*self.start[:2], c="green", s=100, label="Start")
        plt.scatter(*self.goal[:2], c="blue", s=100, label="Goal")
        plt.xlim(self.bounds[0], self.bounds[2])
        plt.ylim(self.bounds[1], self.bounds[3])
        plt.legend()
        plt.grid(True)
        plt.show()

# Test Template

# if __name__ == "__main__":
#     start = (10, 10, 0)  # Start at (x=10, y=10) with heading θ=0
#     goal = (90, 90, 0)   # Goal at (x=90, y=90) with heading θ=0
#     obstacles = [
#         (30, 30, 40, 70),
#         (60, 20, 70, 50)
#     ]
#     bounds = (0, 0, 100, 100)

#     ackerman_rrt = AckermanRRT(start=start, goal=goal, obstacles=obstacles, bounds=bounds)
#     if ackerman_rrt.plan():
#         print("Path found!")
#     else:
#         print("No path found.")
#     ackerman_rrt.plot()
