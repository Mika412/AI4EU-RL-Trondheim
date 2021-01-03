import numpy as np
import tensorflow as tf
from gym import spaces
from ray.rllib.agents.dqn.distributional_q_tf_model import DistributionalQTFModel
from ray.rllib.models.tf.fcnet import FullyConnectedNetwork
from ray.rllib.models.tf.misc import flatten, normc_initializer
from ray.rllib.models.tf.tf_modelv2 import TFModelV2
from ray.rllib.utils import try_import_tf
from ray.rllib.utils.framework import get_activation_fn

""" If `conv_filters` provided will generate CNN, otherwise MLP. """

class MaskedActionsCNN(DistributionalQTFModel, TFModelV2):
    def __init__(
        self, obs_space, action_space, num_outputs, model_config, name, **kwargs
    ):
        super().__init__(
            obs_space, action_space, num_outputs, model_config, name, **kwargs
        )

        conv_filters = model_config["conv_filters"]
        self.is_conv = bool(conv_filters)
        orig_shape = obs_space.original_space["obs"]
        extra_shape = obs_space.original_space["extra"]
        self.inputs = tf.keras.layers.Input(shape=orig_shape.shape, name="observations")
        self.extra_input = tf.keras.layers.Input(shape=extra_shape.shape, name="extra")
        last_layer = self.inputs

        if self.is_conv:
            conv_activation = get_activation_fn(model_config["conv_activation"])
            for i, (filters, kernel_size, stride) in enumerate(conv_filters, 1):
                last_layer = tf.keras.layers.Conv2D(
                    filters,
                    kernel_size,
                    stride,
                    name="conv{}".format(i),
                    activation=conv_activation,
                    padding="valid",
                )(last_layer)
                last_layer = tf.keras.layers.MaxPool2D(pool_size=[2, 2], strides=2)(
                    last_layer
                )
            last_layer = tf.keras.layers.Flatten()(last_layer)
        last_layer = tf.keras.layers.concatenate([last_layer, self.extra_input])
        fc_activation = get_activation_fn(model_config["fcnet_activation"])

        for i, size in enumerate(model_config["fcnet_hiddens"], 1):
            last_layer = tf.keras.layers.Dense(
                size,
                name="fc{}".format(i),
                activation=fc_activation,
                kernel_initializer=normc_initializer(1.0),
            )(last_layer)
            last_layer = tf.keras.layers.Dropout(
                rate=0.4,
            )(last_layer)

        layer_out = tf.keras.layers.Dense(
            num_outputs,
            name="my_out",
            activation=None,
            kernel_initializer=normc_initializer(0.01),
        )(last_layer)
        value_out = tf.keras.layers.Dense(
            1,
            name="value_out",
            activation=None,
            kernel_initializer=normc_initializer(0.01),
        )(last_layer)

        self.base_model = tf.keras.Model(
            [self.inputs, self.extra_input], [layer_out, value_out]
        )
        self.register_variables(self.base_model.variables)
        self._value_out = None

    def forward(self, input_dict, state, seq_lens):
        obs = input_dict["obs"]["obs"]
        extra_obs = input_dict["obs"]["extra"]
        action_mask = tf.maximum(
            tf.math.log(input_dict["obs"]["action_mask"]), tf.float32.min
        )
        model_out, self._value_out = self.base_model([obs, extra_obs])
        return model_out, state
        # return action_mask + model_out, state

    def value_function(self):
        return tf.reshape(self._value_out, [-1])
