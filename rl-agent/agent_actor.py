#!/usr/bin/env python

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

from ray.rllib.models import ModelCatalog
from ray.tune.registry import get_trainable_cls, _global_registry, ENV_CREATOR
from ray.rllib.env.env_context import EnvContext
from ray.rllib.utils.spaces.space_utils import flatten_to_single_ndarray

from ray.tune.registry import register_env
import numpy as np
import sys
import mock

sys.modules["train"] = mock.Mock()
import train

from ray.rllib.env.multi_agent_env import MultiAgentEnv

from tf_models import MaskedActionsCNN

import gym


class MockEnv(MultiAgentEnv):
    pass


class ActorManager:
    default_steps_perform = 10
    EmissionsThreshold = 50

    # Change to a local file
    agent_loc = "/home/mmarfeychuk/ray_results/DQN_custom_env_2020-12-15_21-02-357m4uwdf4/checkpoint_17/checkpoint-17"

    def __init__(self):
        self.get_agent()

    def get_agent(self):

        register_env("custom_env", lambda x: MockEnv())

        ModelCatalog.register_custom_model("masked_actions_model", MaskedActionsCNN)

        print("making agent")
        config = {}
        # Load configuration from file
        config_dir = os.path.dirname(self.agent_loc)
        config_path = os.path.join(config_dir, "params.pkl")
        print("Theres a param.pkl", config_dir, config_path)
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

        cls = get_agent_class("DQN")
        self.agent = cls(env="custom_env", config=config)

        self.agent.restore(self.agent_loc)
        # rollout(agent, "custom_env", num_steps)

    def predict_action(obs):
        print("hello")
        policy_agent_mapping = self.agent.config["multiagent"]["policy_mapping_fn"]

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

    def compute_observations(self, emissions, vehicles, state, currentStep):
        current_obs = {}

        for cell_id in emissions:
            print(cell_id)

            board = np.zeros((16, 17, 3))

            current_action_timestep = int(currentStep / 900) % 96
            print("stuck one", current_action_timestep)
            timestamp_one_hot = np.zeros(shape=(96,), dtype=np.uint8)
            timestamp_one_hot[current_action_timestep] = 1.0
            # current_action_timestep = min((self.sim_step-self.start_at)/(self.sim_max_time-self.start_at), 1.0)
            action_mask = np.ones(shape=(2,), dtype=np.uint8)
            print("stuck 2")
            # print("Extra", (self.sim_step-self.start_at)/(self.sim_max_time-self.start_at))
            extra = np.array(timestamp_one_hot)

            obs = {"obs": board, "action_mask": action_mask, "extra": extra}
            print("stuck 3")
            current_obs[cell_id] = obs

        return current_obs

    def get_action(self, emissions, vehicles, state, current_step=0):
        obs = self.compute_observations(emissions, vehicles, state, current_step)
        print("got out")
        action_dict = self.predict_action(obs)

        print(action_dict)

        cell_state = {}

        for key, value in emissions.items():
            cell_state[key] = value >= self.EmissionsThreshold

        return cell_state, self.default_steps_perform
