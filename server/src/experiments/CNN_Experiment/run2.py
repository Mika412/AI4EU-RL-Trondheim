import ray
from ray.tune.registry import register_env
from custom_env import CustomEnv
from ray.rllib.agents.a3c.a2c import A2CTrainer
from ray.rllib.agents.dqn import DQNTrainer
from ray.rllib.agents.ppo import PPOTrainer
from ray.rllib.models import ModelCatalog

import time
import pprint
import os, sys

from tf_models import MaskedActionsCNN

from ray import tune
from ray.tune.registry import register_env

if 'SUMO_HOME' in os.environ:
	tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
	sys.path.append(tools)

ray.init()
# ModelCatalog.register_custom_model('masked_actions_model', MaskedActionsMLP)
# model_config = {
#     'custom_model': 'masked_actions_model',
#     'fcnet_hiddens': [169, 169],
#     'fcnet_activation': 'leaky_relu',
# }
ModelCatalog.register_custom_model('masked_actions_model', MaskedActionsCNN)
model_config = {
	'custom_model': 'masked_actions_model',
	'conv_filters': [[16, [2, 2], 1], [32, [2, 2], 1], [64, [3, 3], 2]],
	'conv_activation': 'leaky_relu',
	'fcnet_hiddens': [144, 144],
	'fcnet_activation': 'leaky_relu',
}

custom_env =  CustomEnv(env_dir="simulations/small/",
						use_gui=False,
						num_seconds=14400,
						action_every_steps=3600)

register_env("small", lambda _: custom_env)


trainer = DQNTrainer(env="small", config={
	"num_workers": 0,
	# "model": model_config,
	"learning_starts": 0,
    "batch_mode": "complete_episodes",
})

start = time.time()
pp = pprint.PrettyPrinter(indent=4)

while True:
	rest = trainer.train()


# tune_config = {
# 			'num_workers': 1,
# 			'num_gpus': 1,
# 			'model':model_config,
# 			'env': 'small'
# 		}
# tune.run(DQNTrainer, config=tune_config)