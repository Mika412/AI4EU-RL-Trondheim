from abc import abstractmethod

from ray.rllib import ExternalEnv

from .BaseEnv import SumoBaseEnvironment
import matplotlib.pyplot as plt
from statistics import mean 
import math
from itertools import islice 

import gym
class SumoRLBaseEnvironment(gym.Env, SumoBaseEnvironment):

	def __init__(self, env_dir, use_gui=False, num_seconds=20000, start_at = 0, action_every_steps=1):
		print(start_at)
		super().__init__(env_dir, False, use_gui, num_seconds, start_at)

		self.action_every_steps = action_every_steps
		self.epoch_actions = []
		self.epoch_total_rewards = []
		self.epoch_rewards = []
		self.epoch_rewards2 = []
		self.reward_baseline = 0
		self.travel_time = 0

	def reset(self):
		if self.is_connected:
			(total_reward, emissions_reward, halted_reward) = self.episode_rewards()
			self.epoch_total_rewards.append(total_reward)
			self.epoch_rewards.append(emissions_reward)
			self.epoch_rewards2.append(halted_reward)

			fig, axs = plt.subplots(3)


			##### TOTAL REWARD
			plot_average = 10
			# Finding average of each segment 
			average = []
			for i in range(0, int(math.floor(len(self.epoch_total_rewards)/plot_average))*plot_average, plot_average):
				average.append(mean(self.epoch_total_rewards[i:i + plot_average]))

			average.insert(0, self.epoch_total_rewards[0])
			# printing output 
			axs[0].plot(range(len(self.epoch_total_rewards)), self.epoch_total_rewards, color='b')
			axs[0].plot(range(0, len(average)*plot_average, plot_average), average, color='r')
			axs[0].set_xlabel('Episode')
			axs[0].set_ylabel('Episode Reward')
			# axs[0].set_ylim(top=0)

			##### TOTAL EMISSIONS_REWARD

			# printing output 
			axs[1].plot(range(len(self.epoch_rewards)), self.epoch_rewards, color='b')
			axs[1].set_xlabel('Episode')
			axs[1].set_ylabel('CO2 Pollution')
			axs[1].set_ylim(bottom=0)

			##### TOTAL HALTED REWARD

			# printing output 
			axs[2].plot(range(len(self.epoch_rewards2)), self.epoch_rewards2, color='b')
			axs[2].set_xlabel('Episode')
			axs[2].set_ylabel('Halted cars')
			axs[2].set_ylim(bottom=0)

			fig.savefig(self.output_dir+"scores.png")
			plt.close(fig)
		SumoBaseEnvironment.reset(self)
		self._reset()
		# print("Reset everything")
		return self.compute_observations()

	@property
	@abstractmethod
	def reward_range(self):
		pass

	@property
	@abstractmethod
	def action_space(self):
		pass

	@property
	@abstractmethod
	def observation_space(self):
		pass

	@abstractmethod
	def episode_rewards(self):
		pass

	@property
	def done(self):
		return {'__all__': self.is_done}


	def step(self, actions):
		self.travel_time = 0
		self.step_actions(actions)
		
		for i in range(int(max(self.action_every_steps,1)/self.timestep_length_seconds)):
			SumoBaseEnvironment.step(self)
			for edge in self.cells.edge_to_cells.keys():
				self.travel_time += self.traci.edge.getTraveltime(edge)
		self.update_reward()
		observation = self.compute_observations()
  
		reward = self.compute_rewards()
  
		return observation, reward, self.is_done, {}

	@abstractmethod
	def step_actions(self, action):
		pass

	@abstractmethod
	def update_reward(self):
		pass

	@abstractmethod
	def compute_observations(self):
		pass

	@abstractmethod
	def compute_rewards(self):
		pass
	
	@abstractmethod
	def _reset(self):
		pass