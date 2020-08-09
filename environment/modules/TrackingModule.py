from .BaseModule import BaseModule
from environment.modules.LimitedEmissionsModule import EmissionType
import scipy.ndimage.filters as filters
import matplotlib.pyplot as plt
import os
import sys
import numpy as np
from enum import Enum
import csv

# if 'SUMO_HOME' in os.environ:
sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

import traci

class TrackingModule(BaseModule):
	def __init__(self, cell_module, emissions_module, output_dir, sample_every, plot_title, tracking_cells = []):
		super().__init__()

		self._traci = traci
		self._cells = cell_module
		self._emissions = emissions_module

		self.output_dir = output_dir
		
		self.sample_every_steps = sample_every
		self.plot_title = plot_title
		self.tracking_cells = tracking_cells
		
		self.total_emissions = 0
		self.closed_cells = 0
		self.travel_time = 0
		self.waiting_time = 0
		self.current_episode = -1
		
		self.sampled_timestep = []
		self.total_emissions_history = []
		self.closed_cells_history = []
		self.travel_time_history = []
		self.waiting_time_history = []
		self.highest_emission_cell_value_history = []

		self.cell_emissions_history = [[],[]]

	@property
	def variable_name(self):
		return "tracking"

	def step(self, timestep):
		is_sample_step = timestep % self.sample_every_steps == 0
		self.updateEmissions(is_sample_step)
		self.updateClosedCells(is_sample_step)
		self.updateTravelTime(is_sample_step)
		if is_sample_step:
			self.sampled_timestep.append(timestep/3600)
			self.closed_cells_history.append(len(self._cells.closed_cells))
			self.plot_data()

	def updateEmissions(self, sample_step):
		if sample_step:
			emissions_matrix = self._emissions.get_emissions_type_matrix(EmissionType.NOx)
			# Update emissions
			self.total_emissions_history.append(np.sum(emissions_matrix))
			
			self.highest_emission_cell_value_history.append(np.amax(emissions_matrix))

			# self.cell_emissions_history[0].append(self._emissions.get_cell_emissions(self.tracking_cells[0], EmissionType.NOx))
			# self.cell_emissions_history[1].append(self._emissions.get_cell_emissions(self.tracking_cells[1], EmissionType.NOx))

	def updateClosedCells(self, sample_step):
		# Update closed cells
		self.closed_cells += len(self._cells.closed_cells)

	def updateTravelTime(self, sample_step):
		# Update closed cells
		for edge in self._cells.edge_to_cells.keys():
			self.travel_time += self._traci.edge.getTraveltime(edge)
			self.waiting_time += self._traci.edge.getWaitingTime(edge)
		if sample_step:
			self.travel_time_history.append(self.travel_time)
			self.waiting_time_history.append(self.waiting_time)
			self.travel_time = 0
			self.waiting_time = 0

	def plot_data(self):
		fig, axs = plt.subplots(3,2)
		fig.tight_layout(pad=3.0)
		fig.suptitle(self.plot_title)
		# printing output 

		# ##### TOTAL EMISSIONS_REWARD

		# printing output 
		axs[0,0].plot(self.sampled_timestep, self.total_emissions_history, color='b')
		axs[0,0].set_xlabel('Hour')
		axs[0,0].set_ylabel('NOx Aggregated Pollution')
		axs[0,0].set_ylim(bottom=0, top=5000)


		# ##### HIGHEST CELL VALUE

		# # printing output 
		axs[0,1].plot(self.sampled_timestep, self.highest_emission_cell_value_history, color='b')
		axs[0,1].set_xlabel('Hour')
		axs[0,1].set_ylabel('Max Cell Value')
		axs[0,1].set_ylim(bottom=0, top=200)


		# ##### TOTAL HALTED REWARD
		# # printing output 
		axs[1, 0].plot(self.sampled_timestep, self.travel_time_history, color='b')
		axs[1, 0].set_xlabel('Hour')
		axs[1, 0].set_ylabel('Travel time')
		axs[1, 0].set_ylim(bottom=0, top=15e8)

		# ##### TOTAL HALTED REWARD
		# # printing output 
		axs[1, 1].plot(self.sampled_timestep, self.waiting_time_history, color='b')
		axs[1, 1].set_xlabel('Hour')
		axs[1, 1].set_ylabel('Waiting time')
		axs[1, 1].set_ylim(bottom=0, top=11e6)

		axs[2,0].plot(self.sampled_timestep, self.closed_cells_history, color='b')
		axs[2,0].set_xlabel('Hour')
		axs[2,0].set_ylabel('Closed cells')
		axs[2,0].set_ylim(bottom=0)


		###### CELL EMISSIONS #############

		##### TOTAL HALTED REWARD
		# # printing output 
		# axs[2, 0].plot(self.sampled_timestep, self.cell_emissions_history[0], color='b')
		# axs[2, 0].set_xlabel('Hour')
		# axs[2, 0].set_ylabel(self.tracking_cells[0] + ' NOx')
		# axs[2, 0].set_ylim(bottom=0, top=200)

		# axs[2, 1].plot(self.sampled_timestep, self.cell_emissions_history[1], color='b')
		# axs[2, 1].set_xlabel('Hour')
		# axs[2, 1].set_ylabel(self.tracking_cells[1] + ' NOx')
		# axs[2, 1].set_ylim(bottom=0, top=200)

		fig.savefig(self.output_dir+"tracking_scores.png")
		plt.close(fig)

		
	def reset(self):
		# if self.current_episode >= 0:
		# self.total_emissions_history.append(self.total_emissions)
		# self.closed_cells_history.append(self.closed_cells)
		# self.travel_time_history.append(self.travel_time/60)
		
		# self.plot_data()
		self.total_emissions_history = []
		self.travel_time = 0
		self.waiting_time = 0
		self.travel_time_history = []
		self.waiting_time_history = []
		self.current_episode +=1
		self.total_emissions = 0
		self.closed_cells = 0
		self.travel_time = 0

		