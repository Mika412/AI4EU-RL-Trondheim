import numpy as np
from gym import spaces
import math

import sys
sys.path.append(".")

from environment.BaseRLEnv import SumoRLBaseEnvironment
from environment.modules.CellsModule import CellsModule
from environment.modules.EmissionsModule import EmissionsModule
from environment.modules.EmissionsModule import EmissionType as FullEmissionType
from environment.modules.LimitedEmissionsModule import LimitedEmissionsModule, EmissionType
from environment.modules.EmissionsRendererModule import EmissionsRendererModule
from environment.modules.TrackingModule import TrackingModule
import configparser
import copy
import random


class CustomEnv(SumoRLBaseEnvironment):

	def __init__(self, env_dir, use_gui=False, num_seconds=20000, start_at=0, track_all_emissions = False, action_every_steps=1, config_file=None, plot_emissions=False,episode_length=0, random_start=False, plot_title=""):
	
		super().__init__(env_dir, use_gui, num_seconds,start_at,action_every_steps)

		self.random_start = random_start
		self.episode_length = episode_length
		self.num_seconds = num_seconds


		self.travel_time_history = [2054587.1871717058, 3555595.500306866, 1984876.896835179, 2517827.174602762, 3458101.372358129, 3316529.014743211, 4182516.3922181944, 3969996.895818954, 1701148.7220201176, 1737662.4286923357, 1649858.6338100622, 2305774.127347317, 2307503.613308023, 2182816.025304108, 1876438.128627825, 1744754.7846755886, 2247724.1188210575, 3377741.077724242, 2997162.455520544, 3227768.442770195, 3878664.5135084423, 3829612.1301868553, 4713802.825072531, 3945289.5512103867, 5210840.275065945, 6100472.202681262, 5729011.116324227, 5105856.537032605, 6315521.285211369, 6646136.8713971665, 5741114.540310603, 5397807.571050934, 5745816.805735783, 5807043.397078307, 5241214.243733117, 6928146.058149018, 6923834.730927782, 5167293.075530278, 6583437.07147686, 5173422.079977288, 7333198.331944417, 5040516.479415921, 5294587.3920802325, 4436111.720131444, 5495130.395251669, 5006622.7519599125, 4861697.560205057, 5484598.666730846]
		self.emissions_history = [102.43208470897736, 234.64838066159155, 328.2047071592441, 386.32204049975223, 488.12566510539216, 564.9355935810355, 627.2759325333463, 662.6714050178985, 631.197451337309, 553.9135099137369, 510.2242049033067, 474.6289315756265, 464.59680002995015, 452.9031677247802, 446.86553183797037, 428.47148978374827, 449.71830958026186, 498.8830567618996, 535.5541605684339, 549.8816810718376, 676.864219790829, 831.981315873547, 949.9252319193963, 1061.5503693010226, 1215.1405196245091, 1394.1634602712625, 1554.6173631235424, 1709.978474356482, 1822.0606973320105, 1803.1377322966391, 1781.2857729237048, 1779.9512977607108, 1814.8064198238262, 1857.0210447582112, 1868.181710044295, 1906.7279480186676, 2084.698648699058, 2266.9630668765294, 2395.2426834082758, 2465.90539324122, 2473.8789190611596, 2454.4176344363505, 2423.5016327786475, 2373.0132895666607, 2257.9772453745964, 2153.272808096533, 2094.415324577073, 2054.839851563759]
		
		self.forbidden_close_edges = ['-190309447','431246785#0','-26813482','-270122698#5','5106153#0','165221455','-33718247#1','-16189585#1','-16189585#1','290003280','718188324','-308284426#1','308284427#0','60673434','-759460659']

		# Defining used modules
		extra_modules = []
		self.cells = CellsModule(self._cell_shapes, self._edges_in_cells, self.cell_max_height, self.cell_max_width, self.cell_height, self.cell_width)
		extra_modules.append(self.cells)
  

		self.emissions 	= EmissionsModule(self.cells, self.output_dir,[FullEmissionType.NOx], 900,False)
		extra_modules.append(self.emissions)
			
		if plot_emissions:
			self.emissions_renderer = EmissionsRendererModule(self.emissions, [EmissionType.NOx], False)
			extra_modules.append(self.emissions_renderer)
	
		self.tracking = TrackingModule(self.cells, self.emissions, self.output_dir, self.action_every_steps, plot_title)
		extra_modules.append(self.tracking)

		self.set_extra_modules(extra_modules)


		self.previous_vehicles_reward = 0
		self.vehicles_reward = 0
		
		self.total_reward = 0
		self.emissions_total_reward = 0
		self.halted_total_reward = 0
		
		self.previous_emissions = -10000

		self.halted_cars = 0
		self.last_action = 0
		self.action_number = 0
		self.action_cell_id = ''
	
		self.current_closed_cells = np.zeros((self.cells.yCount, self.cells.xCount))
		self.closed_cells = []
		# My test code
		self.obs_shape = 1 + 2
		# self.obs_shape = 1 + len(self.actionable_cells) * (3 + 8*2)

		self.current_history_timestep = 0
		
	def step_actions(self, actions):
		# return	
		self.action_number = int(actions)
		
		# Reclose or open old cells
		new_closed_cells = []
		for cell_id in self.closed_cells:
			# if close
			if random.choice([True, False]):
				self.cells.close_cell(cell_id)
				new_closed_cells.append(cell_id)
			else:
				self.cells.open_cell(cell_id)
		self.closed_cells = new_closed_cells

		# Close new cells
		cells_to_act = np.random.choice(list(self.cells.cells_to_edges), self.action_number)
		for cell_id in cells_to_act:
			unclosable = False
			for edge in self.cells.cells_to_edges[cell_id]:
				if edge in self.forbidden_close_edges:
					# print("Cant close this cell")
					unclosable = True
			if unclosable:
				continue
			self.cells.close_cell(cell_id)
			if not cell_id in self.closed_cells:
				self.closed_cells.append(cell_id)
		
		# Update the closed cells matrix
		self.current_closed_cells = np.zeros((self.cells.yCount, self.cells.xCount))
		for cell_id in self.closed_cells:
			cell = self.cells.cells[cell_id]
			self.current_closed_cells[cell.matrixPosY, cell.matrixPosX] = 1
		# print(self.closed_cells)
		# print(self.current_closed_cells)
		
	def episode_rewards(self):
		return self.total_reward, self.emissions_total_reward, self.halted_total_reward

	def update_reward(self):
		for cell_id in self.cells.cells_to_edges:
			for edge in self.cells.cells_to_edges[cell_id]:
				self.vehicles_reward += self.traci.edge.getLastStepVehicleNumber(edge)


	def compute_observations(self):
		# [:, :, 0] = Emissions
		# [:, :, 1] = Number of cars
		# [:, :, 2] = Timestep
		# [:, :, 3] = Current looking cell
		
		board = np.zeros((self.cells.yCount, self.cells.xCount, 4))
		
		# Get emissions
		board[:,:,0] = self.emissions.get_emissions_type_matrix(EmissionType.NOx) # / 10

		# Get car count
		for cell_id in self.cells.cells:
			car_num = 0
			# 
			if cell_id in self.cells.cells_to_edges:
				for edge in self.cells.cells_to_edges[cell_id]:
					car_num += self.traci.edge.getLastStepVehicleNumber(edge)
			board[self.cells.cells[cell_id].matrixPosY, self.cells.cells[cell_id].matrixPosX, 1] = car_num

		# Set current step
		board[:,:,2] = int(self.sim_step/self.action_every_steps)

		# Closed cells
		board[:,:,3] = self.current_closed_cells
		return board

	def compute_rewards(self):
		return 0

	def compute_rewards_total_emissions(self):
		return np.sum(self.emissions.get_emissions_type_matrix(FullEmissionType.NOx))

	def compute_rewards_max_emissions(self):
		reward = np.amax(self.emissions.get_emissions_type_matrix(FullEmissionType.NOx))
		return reward

	# Track travel time difference
	def compute_rewards_travel_time_difference(self):
		travel_time = (self.travel_time - self.travel_time_history[self.current_history_timestep])
		# self.current_history_timestep += 1
		# print("Travel time difference", travel_time)
		return travel_time


	# Track emission time difference
	def compute_rewards_total_emissions_difference(self):
		emissions = (np.sum(self.emissions.get_emissions_type_matrix(FullEmissionType.NOx)) - self.emissions_history[self.current_history_timestep])
		# self.current_history_timestep += 1
		# print("Emissions difference", emissions , "Total emissions: ", np.sum(self.emissions.get_emissions_type_matrix(FullEmissionType.NOx)), "Default emissions", self.emissions_history[self.current_history_timestep])
		return emissions


	# Track travel time
	def compute_rewards_total_travel_time(self):
		current_travel_time = 0
				
		for edge in self.cells.edge_to_cells.keys():
			current_travel_time += self.traci.edge.getTraveltime(edge)		
		return current_travel_time


	# Track travel time
	def compute_rewards_total_waiting_time(self):
		current_waiting_time = 0
				
		for edge in self.cells.edge_to_cells.keys():
			current_waiting_time += self.traci.edge.getWaitingTime(edge)		
		return current_waiting_time

	@property
	def reward_range(self):
		return -300,300 

	@property

	def action_space(self):
		return spaces.Discrete(2**len(self.actionable_cells))

	@property
	def observation_space(self):
		return spaces.Box(low=0, high=10000, shape=(self.obs_shape,))

	

	def _reset(self):
		self.total_reward = 0
		self.emissions_total_reward = 0
		self.halted_total_reward = 0
		self.action_number = 0
		self.previous_emissions = -10000
		self.vehicles_reward = 0
		self.previous_vehicles_reward = 0
		self.current_history_timestep = 0
		self.travel_time = 0

		self.current_closed_cells = np.zeros((self.cells.yCount, self.cells.xCount))

		# print("reset")
		if self.random_start:
			possible_starting_positions = int(self.num_seconds/self.episode_length)
			# self.sim_max_time = 
			start_ml = random.randint(0,possible_starting_positions - 1)
			self.start_at = start_ml * self.episode_length
			self.sim_max_time = (start_ml + 1) * self.episode_length 
			# print(self.start_at, self.sim_max_time)
			
