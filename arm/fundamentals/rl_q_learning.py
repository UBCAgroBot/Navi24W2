import numpy as np
import re, time, os

class State:
	def __init__(self, s: str):
		if not re.match(r"\(\d+, \d+\)", s):
			raise Exception("Cannot create state with string: ", s)
		self.x, self.y = map(int, s.strip().strip("()").split(", "))
	def __str__(self) -> str:
		return f"State({self.x}, {self.y})"

class SARS:
	def __init__(self, s: State, a: int, r: int, s_prime: State):
		self.s = s
		self.a = a
		self.r = r
		self.s_prime = s_prime
	def __str__(self) -> str:
		return f"SARS({self.s}, {self.a}, {self.r}, {self.s_prime})"

def k_at(s: State, a: int) -> int:
	"""
	Converts our unit system to array indexes
	then returns the value of K
	"""
	return K[s.x - 1, 11 - s.y, a]

def inc_k(s: State, a: int):
	"""
	Increments K at s, a
	"""
	K[s.x - 1, 11 - s.y, a] += 1


def q_at(s: State, a: int) -> int:
	"""
	Converts our unit system to array indexes
	then returns the value of Q
	"""
	return Q[s.x - 1, 11 - s.y, a]
	
def set_q(s: State, a: int, val: float) -> None:
	"""
	Sets q at s, a to val
	"""
	Q[s.x - 1, 11 - s.y, a] = val

def get_file_contents(path: str) -> str:
	"""
	Returns the first line of the file at path	
	"""
	with open(path, "r") as file:
		return file.readline()

def parse_experiences(file_contents: str) -> list[SARS]:
	items = file_contents.split("; ")
	experiences = []

	# Uses the next 4 entires to create a
	# SARS object. Then pops the next 3
	# entries so the next iteration can
	# start with s' of the last iteration
	while len(items) > 3:
		experiences.append(SARS(
			State(items[0]),
			a = a_to_int(items[1]),
			r = int(items[2]),
			s_prime = State(items[3]),
		))
		items = items[3:]
	
	return experiences

def q_vals(s: State) -> list[int]:
	"""
	Returns a list of all the Q values
	for a given state.
	"""
	return Q[s.x - 1, 11 - s.y, :].tolist()

def a_to_int(a: str) -> int:
	"""
	Converts an action like "U", "D",
	"L", "R" to the corresponding int.
	"""
	if a == "U":
		return 0
	elif a == "D":
		return 1
	elif a == "L":
		return 2
	elif a == "R":
		return 3
	else:
		raise Exception("Invalid action received ", a)

def int_to_a(i: int) -> str:
	"""
	Converts the value for an action: 0, 1,
	2, 3 into its string: "UP", "DOWN", ...
	"""
	if i == 0:
		return "UP"
	elif i == 1:
		return "DOWN"
	elif i == 2:
		return "LEFT"
	elif i == 3:
		return "RIGHT"
	else:
		raise Exception("Invalid int received ", i)

def print_optimal_values(it: int):
	os.system('clear')
	print()
	print()
	print()
	print()
	print()
	for y in range(1, 12):
		for x in range(1, 12):
			s = State(f"({x}, {y})")
			q_values = q_vals(s)
			max_value = max(q_values)
			max_index = q_values.index(max_value)
			if int(max_value) >= 0:
				print(f" {int(max_value)} {int_to_a(max_index):<5}"[:8], end="")
			else:
				print(f"{int(max_value)} {int_to_a(max_index):<5}"[:8], end="")
		print()
	print()
	print(f"Iteration: {it}")
	print(flush=True)
	time.sleep(0.1)

def do_learning(experiences: list[SARS], Q, K, discount_factor: float):
	i = 0
	for ex in experiences:
		s = ex.s
		a = ex.a
		r = ex.r
		s_prime = ex.s_prime
		inc_k(s, a)
		
		# Q[s, a] = Q[s, a] + a_k(r + γ max_a'(Q[s', a']) - Q[s, a])
		a_k = 1/k_at(s, a)
		dc = discount_factor
		new_q_val = q_at(s, a) + a_k * (r + dc * max(q_vals(s_prime)) - q_at(s, a))
		set_q(s, a, new_q_val)

		if i % 100 == 0 or i < 50:
			print_optimal_values(i)
		i += 1


path_to_experiences = './experiences.txt'
discount_factor = 0.9
Q = np.zeros((11,11,4))
K = np.zeros((11,11,4))
experiences_file_contents = get_file_contents(path_to_experiences)

experiences = parse_experiences(experiences_file_contents)
do_learning(experiences, Q, K, discount_factor)
print_optimal_values(100000)

