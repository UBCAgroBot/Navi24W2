import numpy as np
import cv2

SQUARE_LENGTH = 50

# (0 = empty space, 1 = obstacle, 2 = weed)
maze = np.zeros((100, 100))

# Add the border around the grid
maze[0:100, 0:1] = 1 # Left wall
maze[0:100, 99:100] = 1 # Right wall
maze[0:1, 0:100] = 1 # Top wall
maze[99:100, 0:100] = 1 # Bottom wall

def display_maze(maze):
    maze_image = np.zeros((maze.shape[0]*SQUARE_LENGTH, maze.shape[1]*SQUARE_LENGTH, 3), dtype=np.uint8)
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 0:
                color = (255, 255, 255)
            else:
                color = (0, 0, 0)
            cv2.rectangle(maze_image, (j*SQUARE_LENGTH, i*SQUARE_LENGTH), ((j+1)*SQUARE_LENGTH, (i+1)*SQUARE_LENGTH), color, -1)
    return maze_image

# Generate the maze image
maze_image = display_maze(maze)

# Display the maze
cv2.imshow("Maze", maze_image)
cv2.waitKey(0)


