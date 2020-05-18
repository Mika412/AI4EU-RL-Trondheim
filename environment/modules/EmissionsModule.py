from .BaseModule import BaseModule
import scipy.ndimage.filters as filters
import os
import sys
import numpy as np
from enum import Enum
import csv

# if 'SUMO_HOME' in os.environ:
sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci

class EmissionType(Enum):
	CO 	= 0
	CO2 = 1
	NOx = 2
	HC 	= 3
	PMx = 4

	def __str__(self):
		return self.name

class EmissionConst:
	# Percentage decay per step
	decay = {'CO':0.9999, 'CO2': 0.99, 'NOx': 0.8, 'HC': 0.999914, 'PMx': 0.99991}

	# Percentage effect per step
	# effect = {'CO': 0.1, 'CO2': 0.05, 'NOx': 0.1, 'HC': 0.4, 'PMx': 0.1}

	# Percentage effect on neighboring cells per step
	# neighbour_effect = {'CO': 0.001, 'CO2': 0.005, 'NOx': 0.001, 'HC': 0.004, 'PMx': 0.001}

	# Percentage effect on neighboring cells per step
	neighbour_decay = {'CO':0.3, 'CO2': 0.3, 'NOx': 10, 'HC': 0.3, 'PMx': 0.3}

class EmissionsModule(BaseModule):
        mg_to_ug_scaler = 1000
        def __init__(self, cell_module, output_dir, emission_types = [], update_every = 10, save_every = 10, save_to_file=False):
                super().__init__()

                self._traci = traci
                self._cells = cell_module
		
                self.emission_types = emission_types
                self.update_every = update_every
                self.save_every = save_every

		# Create emissions matrix
                self.emissions_state = np.zeros(shape=(self._cells.xCount, self._cells.yCount, len(EmissionType)))
		
                self.output_dir = output_dir

                self.save_to_file = save_to_file
                if self.save_to_file:
                        self.emissions_output = output_dir + "emissions.csv"

                        with open(self.emissions_output, "w") as csv_file:
                                writer = csv.writer(csv_file, delimiter=',')
                                row = ["Timestep", "Cell"]
                                for emission_type in self.emission_types:
                                        row.append(str(emission_type))
                                writer.writerow(row)

        @property
        def variable_name(self):
                return "emissions"
	
        def step(self, timestep):
                self.updateEmissions(timestep)
                if self.save_to_file:
                        self.write_emissions(timestep)

        def normalize_emission(self, value):
                return (self.mg_to_ug_scaler * value) / (self._cells.cell_height * self._cells.cell_width)
        
        def get_emissions_type_matrix(self, emission_type):
                return self.emissions_state[:, :, emission_type.value]
	
        def get_cell_emissions(self, cell_id, emission_type):
                cell_obj = self._cells.cells[cell_id]
                return self.emissions_state[cell_obj.matrixPosY, cell_obj.matrixPosX, emission_type.value]

        def get_type_edge_emission(self, emission_type, edge):
                emissions_switcher = {
                        EmissionType.CO: 	self._traci.edge.getCOEmission(edge),
                        EmissionType.CO2: 	self._traci.edge.getCO2Emission(edge),
                        EmissionType.NOx: 	self._traci.edge.getNOxEmission(edge),
                        EmissionType.HC: 	self._traci.edge.getHCEmission(edge),
                        EmissionType.PMx: 	self._traci.edge.getPMxEmission(edge)
                }
                get_emissions = emissions_switcher.get(emission_type, lambda: 0)
                return get_emissions

        def updateEmissions(self, currentTimestep):
                if currentTimestep % self.update_every != 0:
                        return
                for emission_type in self.emission_types:
                        # Get new emission values for the last step
                        for edge, polyIds in self._cells.edge_to_cells.items():
                                emission_value = self.normalize_emission(self.get_type_edge_emission(emission_type, edge) * self.update_every) #Multiply by step length
                                for polyId in polyIds:
                                        x = self._cells.cells[polyId].matrixPosX
                                        y = self._cells.cells[polyId].matrixPosY
                                        self.emissions_state[x, y, emission_type.value] += emission_value
			
			# Apply decay neighbors (Gaussian Filter)
			# TODO(MM): Use const values
                        self.emissions_state[:,:, emission_type.value] = filters.gaussian_filter(self.emissions_state[:,:, emission_type.value], EmissionConst.neighbour_decay[str(emission_type)])
			#
			# Apply decay
                        self.emissions_state[:,:, emission_type.value] = self.emissions_state[:,:, emission_type.value] * EmissionConst.decay[str(emission_type)] 
			
                if self.save_to_file and currentTimestep % self.save_every == 0:
                        self.write_emissions(currentTimestep)

        def write_emissions(self, currentTimestep):
                with open(self.emissions_output, "a") as csv_file:
                        writer = csv.writer(csv_file, delimiter=',')

                        for polyId in self._cells.cells:
                                x = self._cells.cells[polyId].matrixPosX
                                y = self._cells.cells[polyId].matrixPosY
                                row = [currentTimestep, polyId]

                                for emission_type in self.emission_types:
                                        row.append(self.emissions_state[x, y, emission_type.value])
                                writer.writerow(row)


        def reset(self):
		# Create emissions matrix
                self.emissions_state = np.zeros(shape=(self._cells.xCount, self._cells.yCount, len(EmissionType)))
