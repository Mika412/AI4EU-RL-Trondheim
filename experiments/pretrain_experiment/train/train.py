import ray
from ray.tune.registry import register_env
from sim_custom_env import CustomEnv
from ray.rllib.agents.a3c.a2c import A2CTrainer
from ray.rllib.agents.dqn import DQNTrainer
from ray.rllib.models import ModelCatalog
from ray.tune.logger import pretty_print

from ray.rllib.models import ModelCatalog
from ray.rllib.models.tf.misc import normc_initializer
from ray.rllib.agents.dqn.distributional_q_tf_model import DistributionalQTFModel
from ray.rllib.utils import try_import_tf

from test_custom_env import TestCustomEnv

import time
import pprint
import os
import sys
import numpy as np

from ray import tune
from ray.tune.registry import register_env

if 'SUMO_HOME' in os.environ:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)
# Custom Model
from gym.spaces import Box, Discrete, Dict

from ray.rllib.models.modelv2 import ModelV2
from ray.rllib.models.tf.fcnet_v2 import FullyConnectedNetwork
from ray.rllib.models.tf.misc import normc_initializer
from ray.rllib.utils.annotations import override, DeveloperAPI
from ray.rllib.utils import try_import_tf

from tf_models import MaskedActionsCNN

# ray.init(num_cpus=1, num_gpus=0)
ray.init()


def env_creator(env_config):
	return CustomEnv("/home/mykhamarf/Documents/University/Trondheim-RL-Traffic-Optimization/experiments/pretrain_experiment/train/simulated_results.csv")


register_env("custom_env", lambda config: env_creator(config))
# ModelCatalog.register_custom_model("mask_model", MaskedActions)
ModelCatalog.register_custom_model('masked_actions_model', MaskedActionsCNN)
model_config = {
	'custom_model': 'masked_actions_model',
	# 'conv_filters': [[16, [2, 2], 1], [32, [2, 2], 1], [64, [3, 3], 2]],
	'conv_filters': [[16, [2, 2], 1], [32, [2, 2], 1], [64, [3, 3], 2]],
	'conv_activation': 'relu',
	'fcnet_hiddens': [144,64],
	'fcnet_activation': 'relu',
}


a2c_trainer = DQNTrainer(
	env="custom_env",
	config={
		# "replay_buffer_size": 0,
		"learning_starts": 0,
		"prioritized_replay": False,
		# "lr": 0.001,
		"dueling": False,
		"double_q": False,
		'hiddens': [],
		"evaluation_config": {
		        # Example: overriding env_config, exploration, etc:
		        # "env_config": {...},
		    "explore": False
		},
		"model": model_config,
		"exploration_config": {
			# The Exploration class to use.
			"type": "EpsilonGreedy",
					# Config for the Exploration class' constructor:
			"initial_epsilon": 0,
			"final_epsilon": 0,
			# Timesteps over which to anneal epsilon.
			"epsilon_timesteps": 0,
		},
	})
# a2c_trainer = A2CTrainer(
#     env="custom_env",
#     config={
#         # "evaluation_config": {
#         #     "explore": False
#         # },
#         "model": model_config,
#         # "exploration_config": {
#         #     # The Exploration class to use.
#         #     "type": "EpsilonGreedy",
#         #             # Config for the Exploration class' constructor:
#         #     "initial_epsilon": 0.0,
#         #     "final_epsilon": 0.0,
#         #     # Timesteps over which to anneal epsilon.
#         #     "epsilon_timesteps": 0,
#         # },
#     })

for i in range(100):
	print(pretty_print(a2c_trainer.train()))

	# checkpoint = a2c_trainer.save()
	# print("checkpoint saved at", checkpoint)


test_custom_env = TestCustomEnv(env_dir="/home/mykhamarf/Documents/University/Trondheim-RL-Traffic-Optimization/simulations/small_extended/",
								use_gui=True,
								num_seconds=64800,
								# num_seconds=32400,
								start_at=21600,
								track_all_emissions=True,
								plot_emissions=False,
								action_every_steps=900,
								episode_length=3600,
								random_start=False,
								# plot_title="Highest cell emission")
								plot_title="Wait time")
# plot_title="Max cell emissions + 2 * Travel Diff")


test_custom_env.reset()
forbidden_close_edges = ['-190309447','431246785#0','-26813482','-270122698#5','5106153#0','165221455','-33718247#1','-16189585#1','-16189585#1','290003280','718188324','-308284426#1','308284427#0','60673434','-759460659']

while not test_custom_env.is_done:
	observation = test_custom_env.compute_observations()
	print(observation.shape)
	count_zeros = 0
	count_ones = 0

	for cell_id in test_custom_env.cells.cells:
		# Check if cell has any edges
		if cell_id in test_custom_env.cells.cells_to_edges:
			unclosable = False
			for edge in test_custom_env.cells.cells_to_edges[cell_id]:
				if edge in forbidden_close_edges:
					# print("Cant close this cell")
					unclosable = True
			if unclosable:
				continue
			# Set the last matrix
			new_observation = observation.copy()
			new_observation[:, :, 3] = 0
			new_observation[test_custom_env.cells.cells[cell_id].matrixPosY,
							test_custom_env.cells.cells[cell_id].matrixPosX, 3] = 100

			obs_agent_0 = {"real_obs": new_observation,
						   "action_mask":  np.ones(shape=(2,), dtype=np.uint8)}
			a_action = a2c_trainer.compute_action(obs_agent_0)
			# print(a_action, y, x)
			if a_action == 0:
				count_zeros += 1
			else:
				count_ones += 1
			# test_custom_env.change_cell_state_by_pos(test_custom_env.cells.cells[cell_id].matrixPosY, test_custom_env.cells.cells[cell_id].matrixPosX, a_action == 1)
                        test_custom_env.change_cell_state_by_id(cell_id, a_action == 1)
                        print(test_custom_env)

	print("Zeros: ", count_zeros, " Ones: ", count_ones)
	# obs_agent_0 = {"real_obs": test_custom_env.compute_observations(), "action_mask":  np.ones(shape=(2,), dtype=np.uint8)}
	# a_action = a2c_trainer.compute_action(obs_agent_0)
	# print(a_action)
	test_custom_env.step(None)
