import numpy as np
import numpy.typing as npt
import random
from enum import Enum

class Action(Enum):
	LEFT = "LEFT"
	RIGHT = "RIGHT"
	ACCELERATE = "ACCELERATE"
	BRAKE = "BRAKE"
	REVERSE = "REVERSE"

def random_move(s, s_prime, reward) -> npt.NDArray[np.float32]:
	"""
	Returns a numpy array [w, x, y, z] where:
		w [-1, 1]: Turning direction, -1 is left, 1 is right
		x [0, 1]: Acceleration amount
		y [0, 1]: Braking force
		z [0, 1]: Reverse amount
	"""

	random_action = random.choice(list(Action))
	if random_action == Action.LEFT:
		return np.array([-1.0, 0.0, 0.0, 0.0], dtype=float)
	elif random_action == Action.RIGHT:
		return np.array([1.0, 0.0, 0.0, 0.0], dtype=float)
	elif random_action == Action.ACCELERATE:
		return np.array([0.0, 1.0, 0.0, 0.0], dtype=float)
	elif random_action == Action.BRAKE:
		return np.array([0.0, 0.0, 1.0, 0.0], dtype=float)
	elif random_action == Action.REVERSE:
		return np.array([0.0, 0.0, 0.0, 1.0], dtype=float)

	raise Exception("Fell through all action options")
