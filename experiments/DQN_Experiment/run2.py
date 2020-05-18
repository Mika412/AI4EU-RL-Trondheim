import ray
from ray.tune.registry import register_env
from custom_env import CustomEnv
from ray.rllib.agents.a3c.a2c import A2CTrainer
from ray.rllib.agents.dqn import DQNTrainer
from ray.rllib.agents.ppo import PPOTrainer
from ray.rllib.models import ModelCatalog
from ray.tune.logger import pretty_print

import time
import pprint
import os, sys
import numpy as np

from ray import tune
from ray.tune.registry import register_env

if 'SUMO_HOME' in os.environ:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)

ray.init()
custom_env =  CustomEnv(env_dir="simulations/small/",
						use_gui=False,
						num_seconds=3600,
						action_every_steps=1800)
custom_env_evaluate =  CustomEnv(env_dir="simulations/small/",
						use_gui=False,
						num_seconds=3600,
						action_every_steps=1800)
register_env("small", lambda _: custom_env)


trainer = DQNTrainer(env="small", config={
	"num_workers": 0,
	"learning_starts": 0,
	"timesteps_per_iteration": 2,
	# "evaluation_interval": 1,
 	# "evaluation_num_episodes": 1,
	# "log_level": "INFO"    
	# "batch_mode": "complete_episodes",
})

start = time.time()
pp = pprint.PrettyPrinter(indent=4)

while True:
	trainer.train()
	# print(pretty_print(trainer.train()))
	# print("SIM?")
	checkpoint = trainer.save()
	# print("Last checkpoint", checkpoint)
	custom_env_evaluate.reset()
	while not custom_env.is_done:
		sampled_actions = trainer.compute_action(custom_env_evaluate.compute_observations())
		actions = sampled_actions

		obs, reward, done, _ = custom_env_evaluate.step(np.asarray(actions))
		print(reward)

# tune_config = {
# 			'num_workers': 1,
# 			'num_gpus': 1,
# 			'model':model_config,
# 			'env': 'small'
# 		}
# tune.run(DQNTrainer, config=tune_config)