import numpy as np
import cv2

SQUARE_LENGTH = 50

# (0 = empty space, 1 = obstacle)
maze = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

# Define the start and goal
start = (0, 0)
goal = (2, 2)

# Function to display the maze
def display_maze(maze):
    maze_image = np.zeros((maze.shape[0]*SQUARE_LENGTH, maze.shape[1]*SQUARE_LENGTH, 3), dtype=np.uint8)
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            color = (255, 255, 255) if maze[i, j] == 0 else (0, 0, 0)
            cv2.rectangle(maze_image, (j*SQUARE_LENGTH, i*SQUARE_LENGTH), ((j+1)*SQUARE_LENGTH, (i+1)*SQUARE_LENGTH), color, -1)
    return maze_image

# Generate the maze image
maze_image = display_maze(maze)

# Display the maze
cv2.imshow("Maze", maze_image)
cv2.waitKey(0)

# Here we return the path we want to display
path = [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]  # Example path

# Mark the path on the maze image
for (x, y) in path:
    cv2.rectangle(maze_image, (y*SQUARE_LENGTH, x*SQUARE_LENGTH), ((y+1)*SQUARE_LENGTH, (x+1)*SQUARE_LENGTH), (0, 255, 0), -1)

# Display the maze with the path
cv2.imshow("Maze with Path", maze_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

