import numpy as np
from numpy.typing import NDArray
from models import Position, World
from bug_algorithm import get_bug_move
import cv2

SQUARE_LENGTH = 50

def display_maze(world: World):
	"""
	Returns a frame OpenCV can display
	"""
	maze = world.maze
	goal_pos = world.goal_pos
	robot_pos = world.robot_pos

	maze_image = np.zeros((maze.shape[0]*SQUARE_LENGTH, maze.shape[1]*SQUARE_LENGTH, 3), dtype=np.uint8)
	for y in range(maze.shape[0]):
		for x in range(maze.shape[1]):
			if maze[y, x] == 0:
				color = (255, 255, 255) # Empty space should be white
			elif maze[y, x] == 1:
				color = (0, 0, 0) # Obstacle should be black
			else:
				color = (191, 64, 191) # Fallback on purple color

			if x == goal_pos.x and y == goal_pos.y:
				color = (0, 255, 0) # Goal should be green
			if x == robot_pos.x and y == robot_pos.y:
				color = (0, 0, 255) # Robot should be red
			cv2.rectangle(maze_image, (x*SQUARE_LENGTH, y*SQUARE_LENGTH), ((x+1)*SQUARE_LENGTH, (y+1)*SQUARE_LENGTH), color, -1)
	return maze_image

world1 = World(
	np.array([
		[0, 0, 0, 0, 0],
		[1, 1, 1, 1, 0],
		[0, 0, 0, 1, 0],
		[0, 1, 1, 1, 0],
		[0, 0, 0, 0, 0]
	]),
	Position(0, 0),
	Position(2, 2)
)

world2 = World(
	np.array([
		[0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
		[0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
		[0, 0, 1, 1, 0, 1, 0, 0, 1, 1],
		[1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
		[0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
		[0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
		[1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
		[1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
		[1, 1, 0, 0, 0, 1, 0, 1, 0, 1],
		[0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
	]),
	Position(0, 0),
	Position(9, 9),
)

world3 = World(
	np.array([
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 1, 0, 0, 0, 1, 1, 0, 0],
		[0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
		[0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
		[0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
		[0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
		[0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	]),
	Position(0, 0),
	Position(9, 9),
)

while True:
	current_world = world3.copy()
	maze_image = display_maze(current_world)
	cv2.imshow("Maze", maze_image)
	key = cv2.waitKey(100)

	if key == 32:
		current_world.history.append(current_world.robot_pos.copy())
		move = get_bug_move(current_world)
		if move == "UP":
			current_world.robot_pos.y -= 1
		elif move == "LEFT":
			current_world.robot_pos.x -= 1
		elif move == "DOWN":
			current_world.robot_pos.y += 1
		elif move == "RIGHT":
			current_world.robot_pos.x += 1
		elif move == "STAY":
			pass
		else:
			raise Exception("Invalid string returned from get_bug_move")
	elif key == 27:
		break
