import numpy as np
from gym import spaces
import math

import sys
sys.path.append(".")

from environment.BaseRLEnv import SumoRLBaseEnvironment
from environment.modules.CellsModule import CellsModule
# from environment.modules.EmissionsModule import EmissionsModule, EmissionType
from environment.modules.LimitedEmissionsModule import LimitedEmissionsModule, EmissionType
from environment.modules.EmissionsRendererModule import EmissionsRendererModule
import configparser


class CustomEnv(SumoRLBaseEnvironment):

	def __init__(self, env_dir, use_gui=False, num_seconds=20000, action_every_steps=1, config_file=None):
	
		super().__init__(env_dir, use_gui, num_seconds,action_every_steps)

		# self.actionable_cells = ['poly_106', 'poly_79']
		self.actionable_cells = ['poly_106']
  
		# Defining used modules
		self.cells = CellsModule(self._cell_shapes, self._edges_in_cells, self.cell_max_height, self.cell_max_width, self.cell_height, self.cell_width)
		# self.emissions 	= EmissionsModule(self.cells, self.output_dir,[EmissionType.CO2], 1800,False)
		self.emissions = LimitedEmissionsModule(self.cells,self.output_dir,[EmissionType.CO2],1,False,self.actionable_cells)
		self.set_extra_modules([self.cells, self.emissions])


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


		# My test code
		self.obs_shape = (3)
		
	def step_actions(self, actions):
		self.action_number = int(actions)
		
		if self.action_number == 0:
			self.cells.close_cell(self.actionable_cells[0])
		else:
			self.cells.open_cell(self.actionable_cells[0])
	def episode_rewards(self):
		return self.total_reward, self.emissions_total_reward, self.halted_total_reward

	def update_reward(self):
		for targetPoly in self.actionable_cells:
			for edge in self.cells.cells_to_edges[targetPoly]:
				self.vehicles_reward += self.traci.edge.getLastStepVehicleNumber(edge)


	def compute_observations(self):

		board = np.zeros((3))
		board[0] = self.emissions.get_cell_emissions(self.actionable_cells[0], EmissionType.CO2)

		# Get number of vehicles
		
		for edge in self.cells.cells_to_edges[self.actionable_cells[0]]:
			board[1] += self.traci.edge.getLastStepVehicleNumber(edge)

		# Set closed cells
		for cell_id in self.cells.closed_cells:
			cell_obj = self.cells.cells[cell_id]

			board[2] = 1

		# self.action_mask = np.zeros(shape=(self.cells.xCount * self.cells.yCount,), dtype=np.uint8)
		# obs = {"agent_0": board}
		return board.tolist()

	def compute_rewards(self):
		# reward = 169 - math.fabs(np.argmax(self.emissions_board) - self.action_number) + int(np.argmax(self.emissions_board) == self.action_number)* 30000
		current_emissions = 0

		for cell_id in self.actionable_cells:
			current_emissions += self.emissions.get_cell_emissions(cell_id, EmissionType.CO2)

		current_emissions = current_emissions
		
		reward_emissions = - current_emissions
		# reward_vehicles = - (self.vehicles_reward - self.previous_vehicles_reward)

		reward = reward_emissions



		self.previous_emissions = current_emissions
		self.previous_vehicles_reward = self.vehicles_reward

		self.vehicles_reward = 0

		# if not self.action_cell_id in self.actionable_cells:
		# 	reward = -1000
		self.total_reward += reward
		self.emissions_total_reward = current_emissions
		print("Reward", reward)
		return reward

	@property
	def reward_range(self):
		return float('-inf'), float('inf')

	@property

	def action_space(self):
		return spaces.Discrete(2)

	@property
	def observation_space(self):
		return spaces.Box(low=0, high=1000000, shape=(3,))

	

	def _reset(self):
		self.total_reward = 0
		self.emissions_total_reward = 0
		self.halted_total_reward = 0
		self.action_number = 0
		self.previous_emissions = -10000
		self.vehicles_reward = 0
		self.previous_vehicles_reward = 0
