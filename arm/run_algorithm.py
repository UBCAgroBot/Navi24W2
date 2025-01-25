from enum import EnumCheck
import numpy as np
from numpy.typing import NDArray
from models import Position
from bug_algorithm import get_bug_move
import cv2

SQUARE_LENGTH = 50

def display_maze(maze: NDArray[np.int_], robot_pos: Position, goal_pos: Position):
	"""
	Returns a frame OpenCV can display
	"""
	maze_image = np.zeros((maze.shape[0]*SQUARE_LENGTH, maze.shape[1]*SQUARE_LENGTH, 3), dtype=np.uint8)
	for y in range(maze.shape[0]):
		for x in range(maze.shape[1]):
			if maze[y, x] == 0:
				color = (255, 255, 255) # Empty space should be white
			elif maze[y, x] == 1:
				color = (0, 0, 0) # Obstacle should be black
			else:
				color = (191, 64, 191) # Fallback on purple color

			if x == robot_pos.x and y == robot_pos.y:
				color = (0, 0, 255)
			if x == goal_pos.x and y == goal_pos.y:
				color = (0, 255, 0)
			cv2.rectangle(maze_image, (x*SQUARE_LENGTH, y*SQUARE_LENGTH), ((x+1)*SQUARE_LENGTH, (y+1)*SQUARE_LENGTH), color, -1)
	return maze_image

example_maze = np.array([
	[0, 0, 0, 0, 0],
	[1, 1, 1, 1, 0],
	[0, 0, 0, 1, 0],
	[0, 1, 1, 1, 0],
	[0, 0, 0, 0, 0]
])

maze_image = display_maze(example_maze, Position(0, 0), Position(2, 2))
move = get_bug_move(example_maze, Position(0,0), Position(2,2))
print(move)

cv2.imshow("Maze", maze_image)
cv2.waitKey()

robot_pos = Position(0, 0)
goal_pos = Position(2, 2)
while True:
	maze_image = display_maze(example_maze, robot_pos, goal_pos)
	cv2.imshow("Maze", maze_image)
	key = cv2.waitKey(100)

	if key == 32:
		move = get_bug_move(example_maze, robot_pos, goal_pos)
		if move == "UP":
			robot_pos.y -= 1
		elif move == "LEFT":
			robot_pos.x -= 1
		elif move == "DOWN":
			robot_pos.y += 1
		elif move == "RIGHT":
			robot_pos.x += 1
		else:
			raise Exception("Invalid string returned from get_bug_move")
		maze_image = display_maze(example_maze, robot_pos, goal_pos)
		cv2.imshow("Maze", maze_image)
	elif key == 27:
		break
