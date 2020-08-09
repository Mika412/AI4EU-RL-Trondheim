import json
import pandas as pd
import random
import copy
import configparser
import numpy as np
import gym
from gym import spaces
import math

import sys
sys.path.append(".")


class CustomEnv(gym.Env):
    valid_cells = [[5, 0], [4, 1], [5, 1], [3, 2], [4, 2], [5, 2], [3, 3], [4, 3], [5, 3], [6, 3], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [4, 5], [5, 5], [4, 6], [5, 6], [6, 6], [4, 7], [5, 7], [6, 7], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8], [2, 9], [3, 9], [4, 9], [5, 9], [6, 9], [8, 9], [0, 10], [1, 10], [2, 10], [3, 10], [4, 10], [5, 10], [6, 10], [7, 10], [8, 10], [9, 10], [0, 11], [1, 11], [3, 11], [4, 11], [5, 11], [6, 11], [7, 11], [8, 11], [9, 11], [1, 12], [2, 12], [3, 12], [4, 12], [5, 12], [6, 12], [7, 12], [8, 12], [9, 12], [10, 12], [11, 12], [5, 13], [6, 13], [7, 13], [8, 13], [9, 13], [10, 13], [11, 13], [6, 14], [7, 14], [8, 14], [9, 14], [7, 15], [8, 15], [9, 15], [10, 15], [7, 16], [8, 16], [9, 16]]

    def __init__(self, filename):
        self.data = pd.read_csv(filename)
        print("Max value is", self.data['wait_total'].max())

        self.row = self.data.sample()
        self.currentY = 0
        self.currentX = 0
        print(self.row)

        # My test code
        self.obs_shape = (16, 17, 4)

        self.action_mask = np.zeros(shape=(2,), dtype=np.uint8)

    def step(self, action):
        # Decode array from json
        observation = np.asarray(json.loads(
            self.row['new_observations'].values[0]))
        # Normalize observations
        observation[:, :, 0] = observation[:, :, 0]
        # print("Max value", observation[:,:,0].max())
        # Get sampled cell action
        action_mask = np.zeros(shape=(2,), dtype=np.uint8)

        # Set action mask
        action = int(observation[self.currentY, self.currentX, 3])
        # action = random.choice([0, 1])
        # action = 1
        action_mask[action] = 1
        # action_mask = np.ones(shape=(2,), dtype=np.uint8)

        # calculate the reward
        # print((float(self.row['travel_total'])/-100000), (float(self.row['total_emissions'])/-30))
        reward = (float(self.row['wait_total'])/-1000)
        # print(reward)
        # reward = (float(self.row['travel_total'])/-100000) + \
        #     (float(self.row['total_emissions'])/-30)
        # reward = float(self.row['emissions_dif']) * -1
        # reward = float(self.row['max_emissions']) + \
        #    float(self.row['travel_dif']) * 2
        # reward = float(self.row['total_emissions'])/-300.0
        # reward = float(self.row['max_emissions']) * -1
        # Set looking cell
        observation[:, :, 3] = 0
        observation[self.currentY, self.currentX, 3] = 100

        # Create observation
        observation_obj = {"real_obs": observation,
                           "action_mask":  action_mask}

        return observation_obj, reward, True, {}

    @ property
    def reward_range(self):
        return -500, 0

    @ property
    def action_space(self):
        return spaces.Discrete(2)

    @ property
    def observation_space(self):
        return spaces.Dict({
            'action_mask': spaces.Box(low=0, high=1, shape=(2,), dtype=np.uint8),
            "real_obs": spaces.Box(low=0.0, high=1000, shape=self.obs_shape)})

    def reset(self):
        # Get row
        self.row = self.data.sample()

        # Get sample cell
        selected_cell = random.choice(self.valid_cells)
        self.currentY = selected_cell[0]
        self.currentX = selected_cell[1]

        # Decode array from json
        decodedArrays = np.asarray(json.loads(
            self.row['observations'].values[0]))
        # Get sampled cell action
        action_mask = np.zeros(shape=(2,), dtype=np.uint8)
        # Set action mask
        action = int(decodedArrays[self.currentY, self.currentX, 3])
        action_mask[action] = 1
        # action = random.choice([0, 1])
        # print(action_mask)
        # Set looking cell
        decodedArrays[:, :, 3] = 0
        decodedArrays[self.currentY, self.currentX, 3] = 100

        # Create observation
        obs_agent_0 = {"real_obs": decodedArrays, "action_mask":  action_mask}
        return obs_agent_0
