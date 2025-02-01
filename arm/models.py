import numpy as np
from numpy.typing import NDArray

class Position:
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y

	def copy(self):
		return Position(self.x, self.y)
	def __eq__(self, other):
		if isinstance(other, Position):
			return self.x == other.x and self.y == other.y
		return False

	def __str__(self):
		return f"P(x={self.x}, y={self.y})"

class World:
	def __init__(
	    self,
	    maze: NDArray[np.int_],
		robot_pos: Position,
		goal_pos: Position,
	    history: list[Position] = [],
	):
		self.maze = maze
		self.robot_pos = robot_pos
		self.goal_pos = goal_pos
		self.history = history

	def copy(self):
		return World(self.maze, self.robot_pos, self.goal_pos, self.history)
