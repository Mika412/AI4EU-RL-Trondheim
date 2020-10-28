import datetime
import os
import xml.etree.ElementTree as ET
import time
import uuid
import sys
import configparser


if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
    # import traci
    import sumolib
    #import libsumo as traci
    import traci
else:
    raise Exception("Please declare environment variable 'SUMO_HOME'")


class SumoBaseEnvironment:
    def __init__(self,
                 env_dir,
                 out_dir,
                 use_gui=False,
                 num_seconds=20000, start_at=0, extra_modules=[]):

        # Unique simulation name
        self.simulationName = str(uuid.uuid4().hex[:6].upper())

        # Simulation files
        self._net = os.path.join(env_dir, 'osm.net.xml')
        self._route = os.path.join(env_dir, 'generated/routes.xml')
        self._flow = os.path.join(env_dir, 'generated/flows.xml')
        self._background = os.path.join(env_dir, 'osm.poly.add.xml')
        self._induction_loops = os.path.join(
            env_dir, 'data/induction_loops.add.xml')
        self._cell_shapes = os.path.join(env_dir, 'polys.add.xml')
        self._edges_in_cells = os.path.join(env_dir, 'districts.taz.xml')

        # Load configuration file

        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(env_dir, 'config.ini'))
        self.cell_height = int(self.config['DEFAULT']['cell_height'])
        self.cell_width = int(self.config['DEFAULT']['cell_width'])
        self.cell_max_height = int(self.config['DEFAULT']['cell_max_height'])
        self.cell_max_width = int(self.config['DEFAULT']['cell_max_width'])
        self.timestep_length_seconds = int(
            self.config['DEFAULT']['timestep_seconds'])

        # Modules
        self.extra_modules = extra_modules

        # Optional
        self.use_gui = use_gui

        self.sim_max_time = num_seconds
        print(start_at)
        self.start_at = start_at
        self.traci = traci

        self.is_connected = False
        if self.use_gui:
            self._sumo_binary = sumolib.checkBinary('sumo-gui')
        else:
            self._sumo_binary = sumolib.checkBinary('sumo')

        # Create output directory for logging and results
        if out_dir == False:
            self.output_dir = "./outputs/" + str(datetime.datetime.now()) + "/"
        else:
            self.output_dir = out_dir
        if not os.path.exists(self.output_dir):
            #self.output_dir = out_dir + str(datetime.datetime.now()) + "/"
            os.makedirs(self.output_dir)

    def reset(self):
        if self.is_connected:
            self.close()

        sumo_cmd = [self._sumo_binary,
                    '-n', self._net,
                    '--ignore-route-errors', 'True',
                    '--no-warnings',
                    '--step-length', str(self.timestep_length_seconds),
                    '--begin', str(self.start_at),
                    '--no-step-log',
                    '--duration-log.disable',
                    '--waiting-time-memory', '10000',
                    '--time-to-teleport', '-1',
                    '--device.rerouting.probability', '0.25',
                    '--device.rerouting.period', '1',
                    '--device.rerouting.synchronize','True',
                    '--device.rerouting.threads', '8']

        additionals = []
        if self._route and self._flow:
            sumo_cmd.append("-a")
            additionals.append(self._route)
            additionals.append(self._flow)
            if self.use_gui and os.path.exists(self._background):
                additionals.append(self._background)
        else:
            sumo_cmd.append("-r")
            additionals.append(self._route)

        if self._induction_loops:
            additionals.append(self._induction_loops)

        sumo_cmd.append(','.join(additionals))

        if self.use_gui:
            sumo_cmd.append('--start')
        self.traci.start(sumo_cmd)
        self.is_connected = True
        self.traci.simulationStep()

        # Modules
        for module in self.extra_modules:
            module.reset()

    def set_extra_modules(self, modules):
        self.extra_modules = modules

    def close(self):
        self.traci.close()

    @property
    def sim_step(self):
        return self.traci.simulation.getTime()

    @property
    def is_done(self):
        return self.sim_step > self.sim_max_time

    def step(self):
        self.traci.simulationStep()

        # Modules
        for module in self.extra_modules:
            module.step(self.sim_step)

    # def setActive(self):
    #           self.traci.switch(self.simulationName)
