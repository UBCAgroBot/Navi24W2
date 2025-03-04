import numpy as np
from numpy.typing import NDArray

from models import Position, World

def _can_move_up(
	maze: NDArray[np.int_],
	history: list[Position],
	robot_pos: Position) -> bool:
	if robot_pos.y - 1 < 0:
		return False

	if maze[robot_pos.y - 1, robot_pos.x] == 1:
		return False

	if Position(robot_pos.x, robot_pos.y - 1) in history:
		return False

	return True

def _can_move_left(
	maze: NDArray[np.int_],
	history: list[Position],
	robot_pos: Position) -> bool:
	if robot_pos.x - 1 < 0:
		return False

	if maze[robot_pos.y, robot_pos.x - 1] == 1:
		return False

	if Position(robot_pos.x - 1, robot_pos.y) in history:
		return False

	return True

def _can_move_down(
	maze: NDArray[np.int_],
	history: list[Position],
	robot_pos: Position) -> bool:
	if robot_pos.y + 1 >= maze.shape[0]:
		return False

	if maze[robot_pos.y + 1, robot_pos.x] == 1:
		return False

	if Position(robot_pos.x, robot_pos.y + 1) in history:
		return False

	return True

def _can_move_right(
	maze: NDArray[np.int_],
	history: list[Position],
	robot_pos: Position
	) -> bool:
	if robot_pos.x + 1 >= maze.shape[1]:
		return False

	if maze[robot_pos.y, robot_pos.x + 1] == 1:
		return False

	if Position(robot_pos.x + 1, robot_pos.y) in history:
		return False

	return True

def get_bug_move(world: World) -> str:
	"""
	Parameters:
		maze: A 2d array of integers representing the obstacles in the maze.
		      0 represents empty space and 1 represents an obstacle
		history: An array of Position this robot has been to. Does not
		         include the current position.
		robot_pos: A tuple represeting the (x, y) coordinates of the robot.
		           The coordinates are zero indexed
		goal_pos: A tuple representing the (x, y) coordinates of the goal.
		          The coordinates are zero indexed

	This function will decide which direction the bug should move to get 
	to the goal node.

	Returns:
		One of: "UP", "LEFT", "DOWN", "RIGHT", "STAY"
	"""
	maze = world.maze
	robot_pos = world.robot_pos
	goal_pos = world.goal_pos
	history = world.history

	# Making sure the parameters are the correct types
	if not isinstance(maze, np.ndarray):
		raise Exception("maze must be a NumPy array.")
	if maze.dtype != np.int_:
		raise Exception("maze must contain integers (np.int_).")
	if maze.ndim != 2:
		raise Exception("maze must be a 2D array.")

	if not isinstance(robot_pos, Position):
		raise Exception("robot_pos must be an instance of Position.")
	if not isinstance(goal_pos, Position):
		raise Exception("goal_pos must be an instance of Position.")

	if not (0 <= robot_pos.x < maze.shape[1] and 0 <= robot_pos.y < maze.shape[0]):
		raise Exception("robot_pos is out of maze boundaries.")
	if not (0 <= goal_pos.x < maze.shape[1] and 0 <= goal_pos.y < maze.shape[0]):
		raise Exception("goal_pos is out of maze boundaries.")


	desired_direction = None

	x_dist = goal_pos.x - robot_pos.x
	y_dist = goal_pos.y - robot_pos.y

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

	if desired_direction == "UP" and not _can_move_up(maze, history, robot_pos):
		if _can_move_left(maze, history, robot_pos):
			desired_direction = "LEFT"
		elif _can_move_right(maze, history, robot_pos):
			desired_direction = "RIGHT"
		elif _can_move_down(maze, history, robot_pos):
			desired_direction = "DOWN"
		else:
			desired_direction = "STAY"

	if desired_direction == "LEFT" and not _can_move_left(maze, history, robot_pos):
		if _can_move_up(maze, history, robot_pos):
			desired_direction = "UP"
		elif _can_move_down(maze, history, robot_pos):
			desired_direction = "DOWN"
		elif _can_move_right(maze, history, robot_pos):
			desired_direction = "RIGHT"
		else:
			desired_direction = "STAY"

	if desired_direction == "DOWN" and not _can_move_down(maze, history, robot_pos):
		if _can_move_left(maze, history, robot_pos):
			desired_direction = "LEFT"
		elif _can_move_right(maze, history, robot_pos):
			desired_direction = "RIGHT"
		elif _can_move_up(maze, history, robot_pos):
			desired_direction = "UP"
		else:
			desired_direction = "STAY"

	if desired_direction == "RIGHT" and not _can_move_right(maze, history, robot_pos):
		if _can_move_up(maze, history, robot_pos):
			desired_direction = "UP"
		elif _can_move_down(maze, history, robot_pos):
			desired_direction = "DOWN"
		elif _can_move_left(maze, history, robot_pos):
			desired_direction = "LEFT"
		else:
			desired_direction = "STAY"

	return desired_direction

def test_get_bug_move():
	empty_3x3_world = World(
		np.array([
			[0, 0, 0],
			[0, 0, 0],
			[0, 0, 0],
		]),
		Position(0, 1),
		Position(2, 1)
	)
		
	m_maze1 = get_bug_move(empty_3x3_world)
	if m_maze1 != "RIGHT":
		print(m_maze1)
		raise Exception("get_bug_move should have returned RIGHT")

	empty_3x3_world_2 = World(
		np.array([
			[0, 0, 0],
			[0, 0, 0],
			[0, 0, 0],
		]),
		Position(2, 1),
		Position(0, 1)
	)

	m_maze2 = get_bug_move(empty_3x3_world_2)
	if m_maze2 != "LEFT":
		raise Exception("get_bug_move should have returned LEFT")

	empty_3x3_world_3 = World(
		np.array([
			[0, 0, 0],
			[0, 0, 0],
			[0, 0, 0],
		]),
		Position(1, 2),
		Position(1, 0)
	)
	m_maze3 = get_bug_move(empty_3x3_world_3)
	if m_maze3 != "UP":
		print(m_maze3)
		raise Exception("get_bug_move should have returned UP")

	empty_3x3_world_4 = World(
		np.array([
			[0, 0, 0],
			[0, 0, 0],
			[0, 0, 0],
		]),
		Position(1, 2),
		Position(1, 0)
	)
	m_maze4 = get_bug_move(empty_3x3_world_4)
	if m_maze4 != "DOWN":
		raise Exception("get_bug_move should have returned DOWN")

	obstacle_world = World(
		np.array([
			[0, 0, 0],
			[1, 1, 0],
			[0, 0, 0],
		]),
		Position(0, 0),
		Position(0, 2),
	)
	m_maze5 = get_bug_move(obstacle_world)
	if m_maze5 != "RIGHT":
		print(m_maze5)
		raise Exception("get_bug_move should have returned RIGHT")

	obstacle_world_2 = World(
		np.array([
			[0, 0, 0],
			[1, 1, 0],
			[0, 0, 0],
         ]),
		Position(2, 1),
		Position(0, 0),
	)
	m_maze6 = get_bug_move(obstacle_world_2)
	if m_maze6 != "UP":
		print(m_maze6)
		raise Exception("get_bug_move should have returnd UP")

	circle_word_3 = World(
		np.array([
		    [0, 0, 0],
		    [0, 1, 0],
		    [0, 0, 0],
		]),
		Position(2, 2),
		Position(0, 1),
	)
	m_maze7 = get_bug_move(circle_word_3)
	if m_maze7 != "LEFT":
		raise Exception("get_bug_move should have returned LEFT")

	alcove = World(
		np.array([
		    [0, 0, 0, 0],
		    [1, 1, 1, 0],
		    [0, 0, 1, 0],
		    [0, 1, 1, 0],
		    [0, 0, 0, 0],
		]),
		Position(1, 2),
		Position(3, 0),
	)
	m_maze8 = get_bug_move(alcove)
	if m_maze8 != "LEFT":
		raise Exception("get_bug_move should have returned LEFT")

	# Test that bug will not re-traverse an already traveled path
	bottle_neck = World(
		np.array([
			[0,1,0,0,0],
			[0,1,1,0,1],
			[0,0,0,0,1],
			[1,1,1,0,0],
			[0,0,0,0,0],
		]),
		Position(2, 0),
		Position(4, 0),
	)
	m_maze9 = get_bug_move(bottle_neck)
	if m_maze9 != "STAY":
		print(m_maze9)
		raise Exception("get_bug_move should have returned STAY")

if __name__ == "__main__":
	test_get_bug_move()
	print("Add get_bug_move tests passed")
