import random
import copy
import configparser
from environment.modules.TrackingModule import TrackingModule
from environment.modules.EmissionsRendererModule import EmissionsRendererModule
from environment.modules.LimitedEmissionsModule import LimitedEmissionsModule, EmissionType
from environment.modules.EmissionsModule import EmissionType as FullEmissionType
from environment.modules.EmissionsModule import EmissionsModule
from environment.modules.CellsModule import CellsModule
from environment.BaseRLEnv import SumoRLBaseEnvironment
import numpy as np
from gym import spaces
import math

import sys
sys.path.append(".")


class TestCustomEnv(SumoRLBaseEnvironment):

    def __init__(self, env_dir, use_gui=False, num_seconds=20000, start_at=0, track_all_emissions=False, action_every_steps=1, config_file=None, plot_emissions=False, episode_length=0, random_start=False, plot_title=""):

        super().__init__(env_dir, use_gui, num_seconds, start_at, action_every_steps)

        self.random_start = random_start
        self.episode_length = episode_length
        self.num_seconds = num_seconds

        # Defining used modules
        extra_modules = []
        self.cells = CellsModule(self._cell_shapes, self._edges_in_cells,
                                 self.cell_max_height, self.cell_max_width, self.cell_height, self.cell_width)
        extra_modules.append(self.cells)

        self.emissions = EmissionsModule(self.cells, self.output_dir, [
                                         FullEmissionType.NOx], 900, False)
        extra_modules.append(self.emissions)

        if plot_emissions:
            self.emissions_renderer = EmissionsRendererModule(
                self.emissions, [EmissionType.NOx], False) / 100
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

        self.current_closed_cells = np.zeros(
            (self.cells.yCount, self.cells.xCount))
        self.closed_cells = []
        # My test code
        self.obs_shape = (16, 17, 4)

        # self.obs_shape = 1 + len(self.actionable_cells) * (3 + 8*2)

        self.current_history_timestep = 0

    def step_actions(self, actions):
        return
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
        cells_to_act = np.random.choice(
            list(self.cells.cells_to_edges), self.action_number)
        for cell_id in cells_to_act:
            self.cells.close_cell(cell_id)
            if not cell_id in self.closed_cells:
                self.closed_cells.append(cell_id)

        # Update the closed cells matrix
        self.current_closed_cells = np.zeros(
            (self.cells.yCount, self.cells.xCount))
        for cell_id in self.closed_cells:
            cell = self.cells.cells[cell_id]
            self.current_closed_cells[cell.matrixPosY, cell.matrixPosX] = 1
        # print(self.closed_cells)
        # print(self.current_closed_cells)

    def change_cell_state_by_pos(self, yPos, xPos, close):
        for cell_id in self.cells.cells:
            cell = self.cells.cells[cell_id]
            if cell.matrixPosY == yPos and cell.matrixPosX == xPos:
                # print(cell_id)
                if close:
                    self.cells.close_cell(cell_id)
                else:
                    self.cells.open_cell(cell_id)

    def change_cell_state_by_id(self, cell_id, close):
        if close:
            self.cells.close_cell(cell_id)
        else:
            self.cells.open_cell(cell_id)

    def episode_rewards(self):
        return self.total_reward, self.emissions_total_reward, self.halted_total_reward

    def update_reward(self):
        for cell_id in self.cells.cells_to_edges:
            for edge in self.cells.cells_to_edges[cell_id]:
                self.vehicles_reward += self.traci.edge.getLastStepVehicleNumber(
                    edge)

    def compute_observations(self):
        # [:, :, 0] = Emissions
        # [:, :, 1] = Number of cars
        # [:, :, 2] = Timestep
        # [:, :, 3] = Current closed cells

        board = np.zeros((self.cells.yCount, self.cells.xCount, 4))

        # Get emissions
        board[:, :, 0] = self.emissions.get_emissions_type_matrix(
            EmissionType.NOx)

        # Get car count
        for cell_id in self.cells.cells:
            car_num = 0
            #
            if cell_id in self.cells.cells_to_edges:
                for edge in self.cells.cells_to_edges[cell_id]:
                    car_num += self.traci.edge.getLastStepVehicleNumber(edge)
            board[self.cells.cells[cell_id].matrixPosY,
                  self.cells.cells[cell_id].matrixPosX, 1] = car_num

        # Set current step
        board[:, :, 2] = int(self.sim_step/self.action_every_steps)

        # Closed cells
        board[:, :, 3] = self.current_closed_cells
        return board

    @property
    def reward_range(self):
        return -50000, 500

    @property
    def action_space(self):
        return spaces.Discrete(2)

    @property
    def observation_space(self):
        return spaces.Dict({
            'action_mask': spaces.Box(low=0, high=1, shape=(2,), dtype=np.uint8),
            "real_obs": spaces.Box(low=0.0, high=1000000, shape=self.obs_shape)})

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

        self.current_closed_cells = np.zeros(
            (self.cells.yCount, self.cells.xCount))

        print("reset")
        if self.random_start:
            possible_starting_positions = int(
                self.num_seconds/self.episode_length)
            # self.sim_max_time =
            start_ml = random.randint(0, possible_starting_positions - 1)
            self.start_at = start_ml * self.episode_length
            self.sim_max_time = (start_ml + 1) * self.episode_length
            print(self.start_at, self.sim_max_time)
