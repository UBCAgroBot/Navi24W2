"""
Uses Q Learning to generate an optimal policy for the state

State (s):
	The state is a 40x40 2D array where 0 us the floor,
	1 is the robot, 2 is the target, and 3 is the wall
Action (a):
	We predefine values for Direction and Speed. The
	action class has both. We can then map these
	simplified directions to Open AI's more realistic
	control scheme of:

	A numpy array [w, x, y, z] where:
		w [-1, 1]: Turning direction, -1 is left, 1 is right
		x [0, 1]: Acceleration amount
		y [0, 1]: Braking force
		z [0, 1]: Reverse amount
State prime (s_prime):
	This is the state again but after took the action
"""
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
import re
import os


@dataclass(frozen=True)
class State:
	x: int
	y: int

	@classmethod
	def from_string(cls, s: str) -> "State":
		"""
		Create a State from a string in the format '(x, y);'
		"""
		s = s.strip().rstrip(';').strip('()')
		try:
			x_str, y_str = map(str.strip, s.split(','))
			x, y = int(x_str), int(y_str)
		except Exception as e:
			raise ValueError(f"Cannot create state with string: {s}") from e
		return cls(x, y)

	def __str__(self) -> str:
		return f"State({self.x}, {self.y})"

class Direction(Enum):
	LEFT = "LEFT"
	RIGHT = "RIGHT"

class Speed(Enum):
	FORWARD = "FORWARD"
	BACKWARDS = "BACKWARDS"


@dataclass(frozen=True)
class Action:
	direction: Direction
	speed: Speed

	@classmethod
	def from_string(cls, s: str) -> "Action":
		"""
		Create an Action from a string in the format '(DIRECTION, SPEED);'
		"""
		s = s.strip().rstrip(';').strip('()')
		direction_str, speed_str = [part.strip() for part in s.split(',')]

		try:
			direction = Direction[direction_str]
			speed = Speed[speed_str]
		except KeyError as e:
			raise ValueError(f"Invalid direction or speed in string: {s}, direction_str {direction_str}, speed_str: {speed_str}") from e

		return cls(direction, speed)


@dataclass(frozen=True)
class SARS:
	s: State
	a: Action
	r: float
	s_prime: State

	def __str__(self) -> str:
		return f"SARS({self.s}, {self.a}, {self.r}, {self.s_prime})"


def inc_k(state: State, action: Action):
	global K
	K[(state, action)] += 1


def set_q(state: State, action: Action, new_val: float):
	global Q
	Q[(state, action)] = new_val


def get_k(state: State, action: Action) -> int:
	global K
	return K[(state, action)]


def get_q(state: State, action: Action) -> float:
	global Q
	return Q[(state, action)]


def q_vals(state: State) -> list[float]:
	"""
	Returns a list of all the q values in a given state,
	defaulting to 0 if not initialized yet
	"""
	all_actions = [
		Action(Direction.LEFT, Speed.FORWARD),
		Action(Direction.LEFT, Speed.BACKWARDS),
		Action(Direction.RIGHT, Speed.FORWARD),
		Action(Direction.RIGHT, Speed.BACKWARDS),
	]
	return [Q.get((state, a), 0.0) for a in all_actions]

def do_learning(experiences: list[SARS], discount_factor: float):
	for ex in experiences:
		s = ex.s
		a = ex.a
		r = ex.r
		s_prime = ex.s_prime
		
		inc_k(s, a)

		# Q[s, a] = Q[s, a] + a_k(r + γ max_a'(Q[s', a']) - Q[s, a])
		a_k = 1/get_k(s, a)
		dc = discount_factor
		new_q_val = get_q(s, a) + a_k * (r + dc * max(q_vals(s_prime)) - get_q(s, a))
		set_q(s, a, new_q_val)



def get_file_contents(base_path: str) -> str:
	"""
	Returns the first line of the file at path	
	"""
	LOG_DIR = "logs"
	pattern = re.compile(rf"{re.escape(base_path)}_(\d+)\.log$")
	matched_files = []
	for filename in os.listdir(LOG_DIR):
		match = pattern.match(filename)
		if match:
			index = int(match.group(1))
			matched_files.append((index, filename))

	matched_files.sort()

	all_contents: str = ""

	for _, filename in matched_files:
		path = os.path.join(LOG_DIR, filename)
		with open(path, "r") as file:
			all_contents += file.readline().strip()
	
	return all_contents


def parse_experiences(file_contents: str) -> list[SARS]:
	items = file_contents.split("; ")
	experiences = []

	# Reads the first 4 entries from items
	# removing them from the array after 
	# saving them to experiences
	while len(items) >= 4:
		experiences.append(SARS(
			s = State.from_string(items[0]),
			a = Action.from_string(items[1]),
			r = float(items[2]),
			s_prime = State.from_string(items[3]),
		))
		items = items[4:]
	
	return experiences

def print_optimal_values():
	"""
	Iterates through all (x, y) states in a 40x40 grid,
	and prints the maximum Q value for each state.
	"""
	for x in range(30):
		for y in range(30):
			state = State(x, y)
			values = q_vals(state)
			max_q = max(values)
			print(f"{max_q:.2f} \t", end="")
		print()


log_base_name = 'mb_pro_apr_5'
discount_factor = 0.9
Q = defaultdict(float)
K = defaultdict(int)
experiences_file_contents = get_file_contents(log_base_name)

experiences = parse_experiences(experiences_file_contents)
do_learning(experiences, discount_factor)
print_optimal_values()