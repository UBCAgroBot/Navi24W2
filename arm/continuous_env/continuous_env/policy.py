import numpy as np
import numpy.typing as npt
import random
from enum import Enum
from dataclasses import dataclass

class Direction(Enum):
	LEFT = [-0.5, 0, 0, 0]
	RIGHT = [0.5, 0, 0, 0]
	NO_ANGLE = [0, 0, 0, 0]

class Speed(Enum):
	FORWARD = [0, 0.01, 0, 0]
	BACKWARDS = [0, 0, 0, 0.01]

@dataclass
class Action:
	direction: Direction
	speed: Speed

	def get_action_as_open_ai_array(self):
		combined_arr = []
		for d, s in zip(self.direction.value, self.speed.value):
			combined_arr.append(float(d + s))
			
		return np.array(combined_arr, dtype=np.float32)

num_frames_not_moved = 0
prev_robot_pos = (0, 0)
straight_line_acceleration: Speed = Speed.FORWARD
straight_line_direction: Direction = Direction.LEFT

rand_direction = Direction.LEFT
rand_speed = Speed.FORWARD

def straight_line(internal_state: list[list[int]]|None) -> npt.NDArray[np.float32]:
	"""
	Drives in a straight line until the state has not changed for 100 frames.
	After 100 frames of no state change the car will change direction and
	pick a new angle of attack

	Params:
		internal_state (any) Internal state representation where 
		                     0 is floor, 1 is robot, 2 is target 
		                     and 3 is wall
	
	Returns:
		A numpy array [w, x, y, z] where:
			w [-1, 1]: Turning direction, -1 is left, 1 is right
			x [0, 1]: Acceleration amount
			y [0, 1]: Braking force
			z [0, 1]: Reverse amount
	"""
	global num_frames_not_moved
	global prev_robot_pos
	global straight_line_acceleration
	global straight_line_direction

	if internal_state == None:
		print("Internal state is none, returning early")
		return np.array([0.0, 0.0, 0.0, 0.0], dtype=float)

	robot_pos = None
	for y in range(len(internal_state)):
		for x in range(len(internal_state[y])):
			if internal_state[y][x] == 1:
				robot_pos = (x, y)

	if robot_pos == None:
		print("Cound not find robot in internal state, returning early")
		return np.array([0.0, 0.0, 0.0, 0.0], dtype=float)

	if robot_pos == prev_robot_pos:
		num_frames_not_moved += 1
	else:
		num_frames_not_moved = 0

	if num_frames_not_moved == 60:
		print("HIT WALL")
		if straight_line_acceleration == Speed.FORWARD:
			straight_line_acceleration = Speed.BACKWARDS
		else:
			straight_line_acceleration = Speed.FORWARD

		straight_line_direction = random.choice([Direction.LEFT, Direction.RIGHT])

		

	prev_robot_pos = robot_pos
	
	action = Action(direction=straight_line_direction, speed=straight_line_acceleration)
	return action.get_action_as_open_ai_array()
	


def random_move(internal_state: list[list[int]]|None) -> npt.NDArray[np.float32]:
	"""
	Returns a numpy array [w, x, y, z] where:
		w [-1, 1]: Turning direction, -1 is left, 1 is right
		x [0, 1]: Acceleration amount
		y [0, 1]: Braking force
		z [0, 1]: Reverse amount
	"""
	global num_frames_not_moved
	global prev_robot_pos
	global rand_direction
	global rand_speed

	if internal_state == None:
		print("Internal state is none, returning early")
		return np.array([0.0, 0.0, 0.0, 0.0], dtype=float)

	robot_pos = None
	for y in range(len(internal_state)):
		for x in range(len(internal_state[y])):
			if internal_state[y][x] == 1:
				robot_pos = (x, y)

	if robot_pos == None:
		print("Cound not find robot in internal state, returning early")
		return np.array([0.0, 0.0, 0.0, 0.0], dtype=float)

	if robot_pos == prev_robot_pos:
		num_frames_not_moved += 1
	else:
		num_frames_not_moved = 0

	# If we have not moved for 60 frames then we want to
	# generate a new action to take until we hit another wall
	if num_frames_not_moved == 120:
		rand_direction = random.choice(list(Direction))
		rand_speed = random.choice(list(Speed))
		num_frames_not_moved = 0

	rand_action = Action(direction=rand_direction, speed=rand_speed)

	prev_robot_pos = robot_pos

	return rand_action.get_action_as_open_ai_array()
