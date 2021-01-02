#!/usr/bin/env python

class ActorManager:
    default_steps_perform = 10

    def __init__(self):
        pass

    def get_action(self, cell_map, emissions, vehicles, state, current_step=0):
        return {}, self.default_steps_perform
