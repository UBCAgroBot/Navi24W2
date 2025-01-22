from ackerman_rrt import AckermanRRT

start = (10, 10, 0)
goal = (90, 90, 0)
obstacles = [
    (20, 0, 40, 90),
    (60, 10, 80, 100)
]
bounds = (0, 0, 100, 100)

ackerman_rrt = AckermanRRT(start=start, goal=goal, obstacles=obstacles, bounds=bounds, step_size=10, max_iter=2000)

if ackerman_rrt.plan():
    print("Path found!")
else:
    print("No path found.")

ackerman_rrt.plot()