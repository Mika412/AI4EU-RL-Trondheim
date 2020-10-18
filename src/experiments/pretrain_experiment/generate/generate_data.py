
from custom_env import CustomEnv
from environment.modules.EmissionsModule import EmissionType

import time
import pprint
import os, sys
import numpy as np
import random
import csv
import json

if 'SUMO_HOME' in os.environ:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)

start_at = 21600
# num_seconds = 22500
num_seconds = 64800
action_every_steps = 900
# ray.init()
def create_env():
	return CustomEnv(env_dir="/home/mykhamarf/Documents/University/Trondheim-RL-Traffic-Optimization/simulations/small_extended/",
		use_gui=True,
		num_seconds=num_seconds,
		# num_seconds=32400,
		start_at=start_at,
		track_all_emissions = True,
		plot_emissions = False,
		action_every_steps=action_every_steps,
		episode_length=3600,
		random_start = False,
		plot_title = "Baseline (no action)")

travel_time_history = []
start = time.time()

# with open("simulated_results.csv", "w") as csv_file:
# 	writer = csv.writer(csv_file, delimiter=',')
# 	row = ["simulation", "timestep", "observations", "new_observations", "action", "total_emissions","emissions_dif", "max_emissions", "travel_dif", "travel_total", "wait_total"]
# 	writer.writerow(row)
for i in range(0, 1):
	custom_env = create_env()
	custom_env.reset()
	timestep = 0
	travel_time_history = []
	emissions_history = []
	with open("simulated_results.csv", "a") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')
		while not custom_env.is_done:
			print(f'Timestep: {int(timestep)}/{int((num_seconds-start_at)/action_every_steps)}\r', end="")
			action = 1
			# action = random.randint(0, 10)
			# print("Action", action)
			
			observation = custom_env.compute_observations()
			# print("action", action)
			custom_env.step(action)
			new_observation = custom_env.compute_observations()

			total_emissions = custom_env.compute_rewards_total_emissions()
			emissions_history.append(total_emissions)

			# print(total_emissions)
			max_emissions = custom_env.compute_rewards_max_emissions()
			emissions_difference = custom_env.compute_rewards_total_emissions_difference()
			travel_time_difference = custom_env.compute_rewards_travel_time_difference()
			custom_env.current_history_timestep +=1
			total_travel_time = custom_env.compute_rewards_total_travel_time()
			total_waiting_time = custom_env.compute_rewards_total_waiting_time()
			travel_time_history.append(total_travel_time)
			# obst = ', '.join(str(e) for e in observation)
			# new_obst = ', '.join(str(e) for e in new_observation)
			writer.writerow([i, timestep, json.dumps(observation.tolist()), json.dumps(new_observation.tolist()), action, total_emissions,emissions_difference, max_emissions, travel_time_difference, total_travel_time, total_waiting_time])
			timestep +=1

	print("Final timestep", timestep)
	print(travel_time_history)
	print()
	print()
	print("Emissions history")
	print(emissions_history)

end = time.time()
print("Took: ", end - start)
# print("### Baseline:")
# print("Final emissions", np.sum(custom_env.full_emissions.get_emissions_type_matrix(EmissionType.CO2)), "Closed cells", custom_env.tracking.closed_cells, "Travel time", custom_env.tracking.travel_time)
