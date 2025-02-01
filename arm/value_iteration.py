from collections.abc import Callable
from enum import Enum
from copy import deepcopy

class Action(Enum):
	UP = "UP"
	LEFT = "LEFT"
	DOWN = "DOWN"
	RIGHT = "RIGHT"

class State:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, other):
		if isinstance(other, State):
			return self.x == other.x and self.y == other.y
		return False

grid = [
	[0, 0, 0, 1],
	[0, None, 0, -1],
	[0, 0, 0, 0],
]

new_grid = [
	[0, 0, 0, 1],
	[0, None, 0, -1],
	[0, 0, 0, 0],
]

optimal_policy = [
	[Action.UP, Action.UP, Action.UP, Action.UP],
	[Action.UP, Action.UP, Action.UP, Action.UP],
	[Action.UP, Action.UP, Action.UP, Action.UP],
]

positive_terminal_state = State(3, 0)
negative_terminal_state = State(3, 1)


def update_value(s: State, reward_fn: Callable[[State], float], discount_factor) -> tuple[float, Action]:
	unadjusted_actions: dict[Action, float] = {}
	
	# Calculate the expected value of each action
	if s.y-1 < 0 or grid[s.y-1][s.x] == None:
		# If we bounce off wall or go out of bounds
		unadjusted_actions[Action.UP] = grid[s.y][s.x]
	else:
		unadjusted_actions[Action.UP] = grid[s.y - 1][s.x]

	if s.y + 1 >= len(grid) or grid[s.y+1][s.x] == None:
		# If we bounce off wall or go out of bounds
		unadjusted_actions[Action.DOWN] = grid[s.y][s.x]
	else:
		unadjusted_actions[Action.DOWN] = grid[s.y + 1][s.x]

	if s.x - 1 < 0 or grid[s.y][s.x - 1] == None:
		unadjusted_actions[Action.LEFT] = grid[s.y][s.x]
	else:
		unadjusted_actions[Action.LEFT] = grid[s.y][s.x - 1]

	if s.x + 1 >= len(grid[0]) or grid[s.y][s.x + 1] == None:
		unadjusted_actions[Action.RIGHT] = grid[s.y][s.x]
	else:
		unadjusted_actions[Action.RIGHT] = grid[s.y][s.x + 1]

	weighted_actions = {}
	weighted_actions[Action.UP]    = 0.8 * unadjusted_actions[Action.UP]    + 0.1 * unadjusted_actions[Action.LEFT] + 0.1 * unadjusted_actions[Action.RIGHT]
	weighted_actions[Action.LEFT]  = 0.8 * unadjusted_actions[Action.LEFT]  + 0.1 * unadjusted_actions[Action.UP]   + 0.1 * unadjusted_actions[Action.DOWN]
	weighted_actions[Action.DOWN]  = 0.8 * unadjusted_actions[Action.DOWN]  + 0.1 * unadjusted_actions[Action.LEFT] + 0.1 * unadjusted_actions[Action.RIGHT]
	weighted_actions[Action.RIGHT] = 0.8 * unadjusted_actions[Action.RIGHT] + 0.1 * unadjusted_actions[Action.UP]  + 0.1 * unadjusted_actions[Action.DOWN]
	best_action = max(weighted_actions, key=lambda action: unadjusted_actions[action])
	return (reward_fn(s) + discount_factor * weighted_actions[best_action], best_action)

def value_it(reward_fn: Callable[[State], float], discount_factor: float):
	for y in range(len(grid)):
		for x in range(len(grid[0])):
			if grid[y][x] == None:
				continue
			if grid[y][x] == 1 or grid[y][x] == -1:
				continue
			(val, action) = update_value(State(x, y), reward_fn, discount_factor)
			new_grid[y][x] = val
			optimal_policy[y][x] = action

	for y in range(len(grid)):
		for x in range(len(grid[0])):
			grid[y][x] = new_grid[y][x]

def print_grid(grid = grid):
	for y in range(len(grid)):
		for x in range(len(grid[0])):
			val = grid[y][x]
			if val == None:
				print("-------", end = "")
			elif val < 0:
				print(f"{val:.4f}", end="")
			else:
				print(f" {val:.4f}", end="")
			print("  ", end="")
		print()
	print()
	print()

def print_policy():
	for y in range(len(grid)):
		for x in range(len(grid[0])):
			# This prints the optimal policy and padds it to 5 characters
			print(f" {optimal_policy[y][x].name:<5} ", end="")
		print()
	print()
	print()


def reward_fn(s: State) -> float:
	if s == positive_terminal_state:
		return 0.997
	elif s == negative_terminal_state:
		return -0.8559
	
	return -0.1397

def has_grid_converged(old_grid, new_grid) -> bool:
	for y in range(len(old_grid)):
		for x in range(len(old_grid[0])):
			if old_grid[y][x] != None and int(old_grid[y][x] * 10000) != int(new_grid[y][x] * 10000):
				return False
	return True

if __name__ == "__main__":
	iteration = 1
	while (True):
		print_grid()
		old_grid = deepcopy(grid)
		value_it(reward_fn, 1)
		if has_grid_converged(old_grid, grid):
			break
		iteration += 1

	print_grid()
	print_policy()
	print("Converged on interation: ", iteration)

