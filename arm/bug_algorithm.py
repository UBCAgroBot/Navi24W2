import numpy as np
from numpy.typing import NDArray

class Node:
	def __init__(self, x, y):
		self.x = x
		self.y = y

def _can_move_up(maze: NDArray[np.int_], robot_pos: Node) -> bool:
	if robot_pos.y - 1 < 0:
		return False

	return maze[robot_pos.y - 1, robot_pos.x] == 0

def _can_move_left(maze: NDArray[np.int_], robot_pos: Node) -> bool:
	if robot_pos.x - 1 < 0:
		return False

	return maze[robot_pos.y, robot_pos.x - 1] == 0

def _can_move_down(maze: NDArray[np.int_], robot_pos: Node) -> bool:
	if robot_pos.y + 1 >= maze.shape[0]:
		return False

	return maze[robot_pos.y + 1, robot_pos.x] == 0

def _can_move_right(maze: NDArray[np.int_], robot_pos: Node) -> bool:
	if robot_pos.x + 1 >= maze.shape[1]:
		return False

	return maze[robot_pos.y, robot_pos.x + 1] == 0

def get_bug_move(maze: NDArray[np.int_], robot_pos: tuple[int, int], goal_pos: tuple[int, int]) -> str:
	"""
	Parameters:
		maze: A 2d array of integers representing the obstacles in the maze.
		      0 represents empty space and 1 represents an obstacle
		robot_pos: A tuple represeting the (x, y) coordinates of the robot.
		           The coordinates are zero indexed
		goal_pos: A tuple representing the (x, y) coordinates of the goal.
		          The coordinates are zero indexed

	This function will decide which direction the bug should move to get 
	to the goal node.

	Returns:
		One of: "UP", "LEFT", "DOWN", "RIGHT", "STAY"
	"""

	r_pos = Node(robot_pos[0], robot_pos[1])
	g_pos = Node(goal_pos[0], goal_pos[1])

	desired_direction = None
	x_dist = g_pos.x - r_pos.x
	y_dist = g_pos.y - r_pos.y

	if x_dist == 0 and y_dist == 0:
		desired_direction = "STAY"

	elif abs(x_dist) > abs(y_dist):
		# We are further away horizontally
		if x_dist > 0:
			desired_direction = "RIGHT"
		else:
			desired_direction = "LEFT"
	else:
		# We are further away vertically
		if y_dist > 0:
			desired_direction = "DOWN"
		else:
			desired_direction = "UP"

	if desired_direction == "UP" and not _can_move_up(maze, r_pos):
		if _can_move_left(maze, r_pos):
			desired_direction = "LEFT"
		if _can_move_right(maze, r_pos):
			desired_direction = "RIGHT"
		if _can_move_down(maze, r_pos):
			desired_direction = "DOWN"

	if desired_direction == "LEFT" and not _can_move_left(maze, r_pos):
		if _can_move_up(maze, r_pos):
			desired_direction = "UP"
		if _can_move_down(maze, r_pos):
			desired_direction = "DOWN"
		if _can_move_right(maze, r_pos):
			desired_direction = "RIGHT"

	if desired_direction == "DOWN" and not _can_move_down(maze, r_pos):
		if _can_move_left(maze, r_pos):
			desired_direction = "LEFT"
		if _can_move_right(maze,r_pos):
			desired_direction = "RIGHT"
		if _can_move_up(maze,r_pos):
			desired_direction = "UP"

	if desired_direction == "RIGHT" and not _can_move_right(maze, r_pos):
		if _can_move_up(maze, r_pos):
			desired_direction = "UP"
		if _can_move_down(maze, r_pos):
			desired_direction = "DOWN"
		if _can_move_left(maze, r_pos):
			desired_direction = "LEFT"

	return desired_direction

def test_get_bug_move():
	empty_3x3_maze = np.array([
		[0, 0, 0],
		[0, 0, 0],
		[0, 0, 0],
	])
	m_maze1 = get_bug_move(empty_3x3_maze, (0, 1), (2, 1))
	if m_maze1 != "RIGHT":
		print(m_maze1)
		raise Exception("get_bug_move should have returned RIGHT")

	m_maze2 = get_bug_move(empty_3x3_maze, (2, 1), (0, 1))
	if m_maze2 != "LEFT":
		raise Exception("get_bug_move should have returned LEFT")

	m_maze3 = get_bug_move(empty_3x3_maze, (1, 2), (1, 0))
	if m_maze3 != "UP":
		print(m_maze3)
		raise Exception("get_bug_move should have returned UP")

	m_maze4 = get_bug_move(empty_3x3_maze, (1, 0), (1, 2))
	if m_maze4 != "DOWN":
		raise Exception("get_bug_move should have returned DOWN")

	obstacle_maze = np.array([
		[0, 0, 0],
		[1, 1, 0],
		[0, 0, 0],
	])
	m_maze5 = get_bug_move(obstacle_maze, (0, 0), (0, 2))
	if m_maze5 != "RIGHT":
		print(m_maze5)
		raise Exception("get_bug_move should have returned RIGHT")

	m_maze6 = get_bug_move(obstacle_maze, (2, 1), (0, 0))
	if m_maze6 != "UP":
		print(m_maze6)
		raise Exception("get_bug_move should have returnd UP")

	circle_maze = np.array([
	    [0, 0, 0],
	    [0, 1, 0],
	    [0, 0, 0],
	])
	m_maze7 = get_bug_move(circle_maze, (2, 2), (0, 1))
	if m_maze7 != "LEFT":
		raise Exception("get_bug_move should have returned LEFT")

	alcove = np.array([
	    [0, 0, 0, 0],
	    [1, 1, 1, 0],
	    [0, 0, 1, 0],
	    [0, 1, 1, 0],
	    [0, 0, 0, 0],
	])
	m_maze8 = get_bug_move(alcove, (1, 2), (3, 0))
	if m_maze8 != "LEFT":
		raise Exception("get_bug_move should have returned LEFT")

if __name__ == "__main__":
	test_get_bug_move()
	print("Add get_bug_move tests passed")
