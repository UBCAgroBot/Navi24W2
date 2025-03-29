from pydantic import BaseModel
from typing import Any
import os

class sars(BaseModel):
	s: Any
	a: Any
	r: Any
	s_prime: Any

entries:list[sars]=  []

def save_sars(s, a, r, s_prime, log_file_name, batch_size = 10000):
	"""
	Saves the s, a, r, s_prime value to a file in the log
	folder under the same log_file_name
	s,a,r,s_prime;...;s,a,r,s_prime;
	ie. Commas seperate the values and a semicolon seperates
	entries
	"""
	global entries
	entries.append(sars(s=s, a=a, r=r, s_prime=s_prime))
	if len(entries) > batch_size:
		log_file_path = os.path.join("logs", log_file_name)
		with open(log_file_path, "a") as f:
			f.write(";".join(f"{e.s},{e.a},{e.r},{e.s_prime}" for e in entries) + ";")
		entries.clear()
