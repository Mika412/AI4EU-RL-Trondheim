import numpy as np
from gym import spaces
import math

import sys
sys.path.append(".")

from environment.BaseRLEnv import SumoRLBaseEnvironment
from environment.modules.CellsModule import CellsModule
from environment.modules.EmissionsModule import EmissionsModule, EmissionType
from environment.modules.EmissionsRendererModule import EmissionsRendererModule
import configparser


class CustomEnv(SumoRLBaseEnvironment):

	def __init__(self, env_dir, use_gui=False, num_seconds=20000, action_every_steps=1, config_file=None):
	
		super().__init__(env_dir, use_gui, num_seconds,action_every_steps)

		# Defining used modules
		self.cells 		= CellsModule(self._cell_shapes, self._edges_in_cells, self.cell_max_height, self.cell_max_width, self.cell_height, self.cell_width)
		self.emissions 	= EmissionsModule(self.cells, self.output_dir,[EmissionType.CO2], 1800,False)
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


		self.actionable_cells = ['poly_106', 'poly_79']


		# My test code
		self.obs_shape = (self.cells.xCount, self.cells.yCount, 3)
		self.action_mask = np.ones(shape=(self.cells.xCount * self.cells.yCount,), dtype=np.uint8)
		
	def step_actions(self, actions):
		self.action_number = int(actions['agent_0']/2)
		self.action_type = (actions['agent_0'] % 2) == 0
		
		# self.action_cell_id = self
		print(actions['agent_0'], self.action_number, self.action_type)
		if self.action_type:
			self.cells.close_cell(self.actionable_cells[self.action_number])
		else:
			self.cells.open_cell(self.actionable_cells[self.action_number])
	def episode_rewards(self):
		return self.total_reward, self.emissions_total_reward, self.halted_total_reward

	def update_reward(self):
		for targetPoly in self.actionable_cells:
			for edge in self.cells.cells_to_edges[targetPoly]:
				self.vehicles_reward += self.traci.edge.getLastStepVehicleNumber(edge)


	def compute_observations(self):

		board = np.zeros((self.cells.xCount, self.cells.yCount, 3))
		board[:,:, 0] = self.emissions.get_emissions_type_matrix(EmissionType.CO2)

		# Get number of vehicles

		for edge in self.cells.edge_to_cells:
			carCount = self.traci.edge.getLastStepVehicleNumber(edge)
			for cell_id in self.cells.edge_to_cells[edge]:
				cell_obj = self.cells.cells[cell_id]
				board[cell_obj.matrixPosY,cell_obj.matrixPosX,1] += carCount

		# Set closed cells
		for cell_id in self.cells.closed_cells:
			cell_obj = self.cells.cells[cell_id]

			board[cell_obj.matrixPosY,cell_obj.matrixPosX,2] = 1

		# self.action_mask = np.zeros(shape=(self.cells.xCount * self.cells.yCount,), dtype=np.uint8)
		obs_agent_0 = {"real_obs": board, "action_mask":  self.action_mask}
		obs = {"agent_0": obs_agent_0}
		return obs

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
		return {'agent_0': reward}

	@property
	def reward_range(self):
		return float('-inf'), float('inf')

	@property

	def action_space(self):
		return spaces.Discrete(len(self.actionable_cells) * 2)

	@property
	def observation_space(self):
		return spaces.Dict({
			'action_mask': spaces.Box(low=0, high=1, shape=(self.cells.xCount * self.cells.yCount,), dtype=np.uint8),
			"real_obs": spaces.Box(low=0, high=1000000, shape=(self.cells.xCount,self.cells.yCount, 3))})

	

	def _reset(self):
		print("Total reward: %10s" % (self.total_reward))
		self.total_reward = 0
		self.emissions_total_reward = 0
		self.halted_total_reward = 0
		self.action_number = 0
		self.previous_emissions = -10000
		self.vehicles_reward = 0
		self.previous_vehicles_reward = 0