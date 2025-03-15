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
from dataclasses import dataclass
from enum import Enum

class Direction(Enum):
	LEFT = "LEFT"
	RIGHT = "RIGHT"

class Speed(Enum):
	FORWARD = "FORWARD"
	BACKWARDS = "BACKWARD"

@dataclass
class Action:
	direction: Direction
	speed: Speed

