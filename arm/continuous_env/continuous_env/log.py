from pydantic import BaseModel
from continuous_env.policy import Action as PolicyAction
from continuous_env.policy import policy_direction_to_str, policy_speed_to_str
from typing import Any
import os

class sars(BaseModel):
	s: tuple[int, int]
	a: tuple[str, str]
	r: Any
	s_prime :tuple[int, int]

entries: list[sars] = []

MAX_FILE_SIZE = 10 * 1024 * 1024
LOG_DIR = "logs"

def get_log_file_path(base_name: str, index: int) -> str:
	return os.path.join(LOG_DIR, f"{base_name}_{index}.log")

def save_sars(s, a: PolicyAction, r, s_prime, base_log_name, batch_size = 1000):
	"""
	Saves the s, a, r, s_prime value to a file in the log
	folder under the same log_file_name
	s,a,r,s_prime;...;s,a,r,s_prime;
	ie. Commas seperate the values and a semicolon seperates
	entries
	"""
	global entries
	x = None
	y = None

	for i, nested_arr in enumerate(s):
		for j, val in enumerate(nested_arr):
			# print(val, end = "")
			if(val == 1):
				x = i
				y = j

	x_prime = None
	y_prime = None

	for i, nested_arr in enumerate(s_prime):
		for j, val in enumerate(nested_arr):
			if (val == 1):
				x_prime = i
				y_prime = j


	instance = sars(s = (x,y), a = (policy_direction_to_str(a.direction), policy_speed_to_str(a.speed)), r = r, s_prime = (x_prime, y_prime))
	entries.append(instance)

	if len(entries) > batch_size:
		file_index = 0
		log_file_path = get_log_file_path(base_log_name, file_index)
		while os.path.exists(log_file_path) and os.path.getsize(log_file_path) > MAX_FILE_SIZE:
			file_index += 1
			log_file_path = get_log_file_path(base_log_name, file_index)

		with open(log_file_path, "a") as f:
			for entry in entries:
				formatted_entry = f"({entry.s[0]}, {entry.s[1]}); ({entry.a[0]}, {entry.a[1]}); {entry.r}; ({entry.s_prime[0]}, {entry.s_prime[1]});"
				f.write(formatted_entry + " ")
				if f.tell() > MAX_FILE_SIZE:
					f.close()
					file_index += 1
					log_file_path = get_log_file_path(base_log_name, file_index)
					f = open(log_file_path, "a")
		entries.clear()