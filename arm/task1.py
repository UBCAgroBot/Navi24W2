import numpy as np
import cv2

SQUARE_LENGTH = 50

# (0 = empty space, 1 = obstacle, 2 = punishment zone, 3 = robot)
maze = np.zeros((100, 100))

# Add the "crop rows"
top_left_row_height= [12, 24, 36, 48, 60, 72, 84]
for h in top_left_row_height:
    ROW_LENGTH = 50
    ROW_HEIGHT = 4
    maze[h:h+ROW_HEIGHT, 25:75] = 1

# Add the punishment zones 😈
# This np notation is:
# maze[start_row:end_row, start_col:end_col]
maze[0:5, 0:100] = 2
maze[0:100, 0:5] = 2
maze[0:100, 95:100] = 2
maze[95:100, 0:100] = 2

robot_pos = (72 + 6, 40)
# Add robot in the last crop row
maze[robot_pos[0]:robot_pos[0]+4, robot_pos[1]:robot_pos[1]+4] = 3

def display_maze(maze):
    maze_image = np.zeros((maze.shape[0]*SQUARE_LENGTH, maze.shape[1]*SQUARE_LENGTH, 3), dtype=np.uint8)
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 0:
                color = (255, 255, 255) # Empty space should be white
            elif maze[i, j] == 1:
                color = (0, 0, 0) # Obstacle should be black
            elif maze[i, j] == 2:
                color = (203, 195, 227) # Punishment zone should be brown
            elif maze[i, j] == 3:
                color = (0, 0, 255) # Robot should be red
            else:
                color = (191, 64, 191) # Fallback on purple color

            cv2.rectangle(maze_image, (j*SQUARE_LENGTH, i*SQUARE_LENGTH), ((j+1)*SQUARE_LENGTH, (i+1)*SQUARE_LENGTH), color, -1)
    return maze_image

def move_right():
    global 

# Generate the maze image
maze_image = display_maze(maze)

# Display the maze
cv2.imshow("Maze", maze_image)
cv2.waitKey(0)

