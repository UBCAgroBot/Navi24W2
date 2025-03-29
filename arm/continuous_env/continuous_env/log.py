from pydantic import BaseModel
from typing import Any
import os

class sars(BaseModel):
	s: Any
	a: Any
	r: Any
	s_prime: Any

entries:list[tuple[int,int]]=  []

def save_sars(s, a, r, s_prime, log_file_name, batch_size = 10):
	"""
	Saves the s, a, r, s_prime value to a file in the log
	folder under the same log_file_name
	s,a,r,s_prime;...;s,a,r,s_prime;
	ie. Commas seperate the values and a semicolon seperates
	entries
	"""
	# global entries
	# for nested_arr in s:
	# 	for val in nested_arr:
	# 		print(val, end = "")
	# 		if val 

	global entries
	for i, nested_arr in enumerate(s):
		for j, val in enumerate(nested_arr):
			print(val, end = "")
		print()

	global entries
	x = None
	y = None

	for i, nested_arr in enumerate(s):
		for j, val in enumerate(nested_arr):
			print(val, end = "")
			if(val == 1):
				x = i
				y = j
		print(f" (width of {len(nested_arr)})")	


	print(f"(length of s {len(s)})")

	if x == None or y == None:
		print("Could not find robot position")
	else:
		print("robot position (x,y): ", x, y)
		
	# entries.append(sars(s=s, a=a, r=r, s_prime=s_prime))

	entries.append((x,y))
	# print(len(entries))
	if len(entries) > batch_size:
		log_file_path = os.path.join("logs", log_file_name)
		with open(log_file_path, "a") as f:
			# f.write(x , y)
			for entry in entries:
				f.write(f"({entry[0]}, {entry[1]}) ")
			
			# f.write(";".join(f"{e.s},{e.a},{e.r},{e.s_prime}" for e in entries) + ";")
		entries.clear()
