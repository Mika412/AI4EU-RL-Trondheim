from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json
import os
import pickle
import collections

import gym
import ray
from ray.rllib.agents.registry import get_agent_class
from ray.rllib.evaluation.sampler import clip_action
from ray.tune.utils import merge_dicts

from ray.rllib.evaluation.worker_set import WorkerSet
from ray.rllib.env import MultiAgentEnv

# from custom_env import CustomEnv
# from tf_models import MaskedActionsCNN
from ray.rllib.models import ModelCatalog
from ray.tune.registry import get_trainable_cls, _global_registry, ENV_CREATOR
from ray.rllib.env.env_context import EnvContext
from ray.rllib.utils.spaces.space_utils import flatten_to_single_ndarray


class ActorManager:
    default_steps_perform = 10
    EmissionsThreshold = 50

    # Change to a local file
    agent_loc = "/home/mmarfeychuk/ray_results/A3C_custom_env_2020-12-06_21-44-0940lfqj3b/checkpoint_129/checkpoint-129"

    def __init__(self):
        self.get_agent()

    def get_agent(self):
        print("making agent")
        config = {}
        # Load configuration from file
        config_dir = os.path.dirname(self.agent_loc)
        config_path = os.path.join(config_dir, "params.pkl")

        if not os.path.exists(config_path):
            config_path = os.path.join(config_dir, "../params.pkl")
        if not os.path.exists(config_path):
            if not args.config:
                raise ValueError(
                    "Could not find params.pkl in either the checkpoint dir or "
                    "its parent directory."
                )
        else:
            with open(config_path, "rb") as f:
                config = pickle.load(f)
        if "num_workers" in config:
            del config["num_workers"]
        if "num_gpus_per_worker" in config:
            del config["num_gpus_per_worker"]

        if "num_workers" in config:
            del config["num_workers"]

        if "num_gpus_per_worker" in config:
            del config["num_gpus_per_worker"]

        ray.init()

        cls = get_agent_class("A3C")
        self.agent = cls(env="custom_env", config=config)

        self.agent.restore(args.checkpoint)
        # rollout(agent, "custom_env", num_steps)

    def rollout(obs):
        policy_agent_mapping = agent.config["multiagent"]["policy_mapping_fn"]

        mapping_cache = {}  # in case policy_agent_mapping is stochastic

        action_dict = {}
        for agent_id, a_obs in obs.items():
            if a_obs is not None:
                policy_id = mapping_cache.setdefault(
                    agent_id, policy_agent_mapping(agent_id)
                )
                a_action = self.agent.compute_action(
                    a_obs,
                    # prev_action=prev_actions[agent_id],
                    # prev_reward=prev_rewards[agent_id],
                    policy_id=policy_id,
                )
                a_action = flatten_to_single_ndarray(a_action)
                action_dict[agent_id] = a_action

        return action_dict

    def get_action(self, emissions, current_step=0):

        cell_state = {}

        for key, value in emissions.items():
            cell_state[key] = value >= self.EmissionsThreshold

        return cell_state, self.default_steps_perform
