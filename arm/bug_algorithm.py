import numpy as np
from numpy.typing import NDArray

class robot_pos:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class goal_pos:
	def __init__(self, x, y):
		self.x = x
		self.y = y

def make_bug_move(maze: NDArray[np.int_]) -> str:
	"""
	Given a 2d array of integers representing a 
	maze where: 0 = empty space, 1 = obstacle, 
	2 = robot, 3 = goal, returns either "UP",
	"LEFT", "DOWN", "RIGHT" "STAY". The string signify 
	which direction the algorithm wants to move
	the robot.
	"""
	r_pos = None
	for y in range (maze.shape[0]):
		for x in range (maze.shape[1]):
			if maze[y, x] == 2:
				r_pos = robot_pos(x, y)
	if not r_pos:
		raise Exception("Cannot make_bug_move on board that does not have a robot")

	g_pos = None
	for y in range(maze.shape[0]):
		for x in range(maze.shape[1]):
			if maze[y, x] == 3:
				g_pos = goal_pos(x, y)
	if not g_pos:
		raise Exception("Cannot make_bug_move on board that does not have a goal square")

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

	return desired_direction

def test_make_bug_move():
	maze1 = np.array([
		[0, 0, 0],
		[2, 0, 3],
		[0, 0, 0],
	])
	m_maze1 = make_bug_move(maze1)
	if m_maze1 != "RIGHT":
		print(m_maze1)
		raise Exception("make_bug_move should have returned RIGHT")


	maze2 = np.array([
		[0, 0, 0],
		[3, 0, 2],
		[0, 0, 0],
	])
	m_maze2 = make_bug_move(maze2)
	if m_maze2 != "LEFT":
		raise Exception("make_bug_move should have returned LEFT")
	
	maze3 = np.array([
		[0, 3, 0],
		[0, 0, 0],
		[0, 2, 0],
	])
	m_maze3 = make_bug_move(maze3)
	if m_maze3 != "UP":
		raise Exception("make_bug_move should have returned UP")

	maze4 = np.array([
		[0, 2, 0],
		[0, 0, 0],
		[0, 3, 0],
	])
	m_maze4 = make_bug_move(maze4)
	if m_maze4!= "DOWN":
		raise Exception("make_bug_move should have returned DOWN")

if __name__ == "__main__":
	test_make_bug_move()
	print("Add make_bug_move tests passed")
