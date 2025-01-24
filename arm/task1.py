import numpy as np
import cv2

SQUARE_LENGTH = 50

# (0 = empty space, 1 = obstacle, 2 = robot, 3 = goal)
maze = np.zeros((25, 25))

for i in range(3, 10):
    maze[15, i] = 1

for i in range(5, 15):
    maze[10, i] = 1

for i in range(5, 15):
    maze[5, i] = 1


robot_pos = (5, 20)
# Add robot in the last crop row
maze[robot_pos[1], robot_pos[0]] = 2

def display_maze(maze):
    maze_image = np.zeros((maze.shape[0]*SQUARE_LENGTH, maze.shape[1]*SQUARE_LENGTH, 3), dtype=np.uint8)
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i, j] == 0:
                color = (255, 255, 255) # Empty space should be white
            elif maze[i, j] == 1:
                color = (0, 0, 0) # Obstacle should be black
            elif maze[i, j] == 2:
                color = (0, 0, 255) # Robot should be red
            elif maze[i, j] == 3:
                color = (0, 255, 0)
            else:
                color = (191, 64, 191) # Fallback on purple color

            cv2.rectangle(maze_image, (j*SQUARE_LENGTH, i*SQUARE_LENGTH), ((j+1)*SQUARE_LENGTH, (i+1)*SQUARE_LENGTH), color, -1)
    return maze_image

def move_right():
    global robot_pos
    maze[robot_pos[1], robot_pos[0]] = 0
    robot_pos = (robot_pos[0] + 1, robot_pos[1])
    maze[robot_pos[1], robot_pos[0]] = 3

def move_up():
    global robot_pos
    if robot_pos[1] <= 0:
        return

    maze[robot_pos[1], robot_pos[0]] = 0
    robot_pos = (robot_pos[0], robot_pos[1] - 1)
    maze[robot_pos[1], robot_pos[0]] = 3


def bug_move_up():
    global robot_pos
    if maze[robot_pos[1] - 1, robot_pos[0]] != 0:
        move_right()
    else:
        move_up()
    

while True:
    maze_image = display_maze(maze)
    cv2.imshow("Maze", maze_image)
    key = cv2.waitKey(100)

    if key == 32:
        bug_move_up()
        maze_image = display_maze(maze)
        cv2.imshow("Maze", maze_image)
    elif key == 27:
        break

cv2.destroyAllWindows()
