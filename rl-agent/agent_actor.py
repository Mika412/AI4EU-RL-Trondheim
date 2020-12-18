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

from ray.rllib.env.multi_agent_env import MultiAgentEnv

from tf_models import MaskedActionsCNN

import gym

class DefaultMapping(collections.defaultdict):
    """default_factory now takes as an argument the missing key."""

    def __missing__(self, key):
        self[key] = value = self.default_factory(key)
        return value

class MockEnv(MultiAgentEnv):
    policy_1_cells = [
        "poly_5",
        "poly_21",
        "poly_20",
        "poly_37",
        "poly_36",
        "poly_35",
        "poly_54",
        "poly_53",
        "poly_52",
        "poly_51",
        "poly_70",
        "poly_69",
        "poly_68",
        "poly_67",
        "poly_86",
        "poly_85",
        "poly_85",
        "poly_102",
        "poly_101",
        "poly_100",
        "poly_118",
        "poly_135",
        "poly_152",
        "poly_168",
        "poly_169",
        "poly_185",
    ]
    policy_2_cells = [
        "poly_160",
        "poly_176",
        "poly_161",
        "poly_177",
        "poly_193",
        "poly_162",
        "poly_112",
        "poly_146",
        "poly_112",
        "poly_131",
        "poly_147",
        "poly_163",
    ]
    policy_3_cells = [
        "poly_263",
        "poly_264",
        "poly_265",
        "poly_266",
        "poly_250",
        "poly_249",
        "poly_248",
        "poly_247",
        "poly_230",
        "poly_231",
        "poly_232",
        "poly_233",
        "poly_234",
        "poly_214",
        "poly_216",
        "poly_269",
        "poly_184",
        "poly_217",
        "poly_233",
        "poly_232",
        "poly_217",
        "poly_218",
        "poly_201",
        "poly_185",
        "poly_186",
        "poly_202",
        "poly_203",
        "poly_219",
        "poly_218",
        "poly_217",
    ]
    policy_default_cells = []

    def policy_mapping(self, agent_id):
        if agent_id in self.policy_1_cells:
            return "policy_1"
        elif agent_id in self.policy_2_cells:
            return "policy_2"
        elif agent_id in self.policy_3_cells:
            return "policy_3"
        else:
            return "default"

sys.modules["train"] = MockEnv()
import train

class ActorManager:
    default_steps_perform = 10
    EmissionsThreshold = 50

    # Change to a local file
    agent_loc = "./model/checkpoint_13/checkpoint-13"

    def __init__(self):
        self.get_agent()
        
        # self.prev_actions = DefaultMapping(lambda agent_id: action_init[mapping_cache[agent_id]])
    def get_agent(self):

        register_env("custom_env", lambda x: MockEnv())

        ModelCatalog.register_custom_model("masked_actions_model", MaskedActionsCNN)

        config = {}
        # Load configuration from file
        config_dir = os.path.dirname(self.agent_loc)
        config_path = os.path.join(config_dir, "params.pkl")
        print("Theres a param.pkl", config_dir, config_path)
        if not os.path.exists(config_path):
            config_path = os.path.join(config_dir, "../params.pkl")
        if not os.path.exists(config_path):
            if not config:
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

    def predict_action(self, obs):
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
                    # prev_action=self.prev_actions[agent_id],
                    policy_id=policy_id,
                )
                a_action = flatten_to_single_ndarray(a_action)
                # self.prev_actions[agent_id] = a_action
                action_dict[agent_id] = a_action
        return action_dict

    def compute_observations(self, cell_map, emissions, vehicles, state, currentStep):
        current_obs = {}
        # Same board
        same_board = np.zeros((16,17,2))

        for cell_id in emissions:
            posY = cell_map[cell_id].y
            posX = cell_map[cell_id].x
            # Emissions
            same_board[posY, posX, 0] = emissions[cell_id]
            same_board[:, :, 0] /= 200
            same_board[same_board[:, :, 0] > 1.0] = 1.0

            # Vehicles
            same_board[posY, posX, 1] = emissions[cell_id]

        for cell_id in emissions:
            posY = cell_map[cell_id].y

            posX = cell_map[cell_id].x
            board = np.zeros((16, 17, 3))
            board[:,:,0] = same_board[:,:,0]
            board[:,:,1] = same_board[:,:,1]
            board[posY, posX, 2] = 10.0

            current_action_timestep = int(currentStep / 900) % 36
            timestamp_one_hot = np.zeros(shape=(36,), dtype=np.uint8)
            timestamp_one_hot[current_action_timestep] = 1.0
            # timestamp_one_hot[current_action_timestep] = 1.0
            action_mask = np.ones(shape=(2,), dtype=np.uint8)
            extra = np.array(timestamp_one_hot)

            obs = {"obs": board, "action_mask": action_mask, "extra": extra}
            current_obs[cell_id] = obs

        return current_obs

    def get_action(self, cell_map, emissions, vehicles, state, current_step=0):
        obs = self.compute_observations(cell_map, emissions, vehicles, state, current_step)
        action_dict = self.predict_action(obs)

        closed_cells = 0

        cell_state = {}
        for cell_id in action_dict:
            action = action_dict[cell_id]
            cell_state[cell_id] = action
            closed_cells += action
            
        print("Step {}: Closed Cells: {}".format(current_step, closed_cells))
        return cell_state, self.default_steps_perform
