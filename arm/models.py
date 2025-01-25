class Position:
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y

	def __eq__(self, other):
		if isinstance(other, Position):
			return self.x == other.x and self.y == other.y
		return False

	def __str__(self):
		return f"P(x={self.x}, y={self.y})"

