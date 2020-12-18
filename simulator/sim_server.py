import time
from concurrent import futures

import json
import grpc

# import the generated classes :
import simulator_pb2
import simulator_pb2_grpc
from sim_manager import SimulationManager

# create a class to define the server functions, derived from
class SimulationServicer(simulator_pb2_grpc.SimulatorServicer):
    manager = None

    def start_simulation(self, request, context):
        print("received something")
        # define the buffer of the response :
        self.manager = SimulationManager()

        response = simulator_pb2.StateResponse()

        self.manager.initialize(request.StartDate, request.EndDate, request.DensityPerc)
        # get the value of the response by calling the desired function :
        emissions = self.manager.get_emissions()
        for key, value in emissions.items():
            response.emissions[key] = value

        vehicles = self.manager.get_vehicles()
        for key, value in vehicles.items():
            response.vehicles[key] = value

        cell_state = self.manager.get_cell_states()
        for key, value in cell_state.items():
            response.state[key] = value

        response.currentStep = self.manager.current_step()

        cell_map = self.manager.get_cells_map()
        for key, value in cell_map.items():
            response.cell_map[key].x = value['x']
            response.cell_map[key].y = value['y']

        response.hasEnded = self.manager.has_ended()
        return response

    
    def step(self, request, context):
        # define the buffer of the response :
        response = simulator_pb2.StateResponse()

        self.manager.step(request.cell_state, request.numSteps)

        # get the value of the response by calling the desired function :
        emissions = self.manager.get_emissions()
        for key, value in emissions.items():
            response.emissions[key] = value

        vehicles = self.manager.get_vehicles()
        for key, value in vehicles.items():
            response.vehicles[key] = value

        cell_state = self.manager.get_cell_states()
        for key, value in cell_state.items():
            response.state[key] = value

        response.currentStep = self.manager.current_step()
        response.hasEnded = self.manager.has_ended()

        cell_map = self.manager.get_cells_map()
        for key, value in cell_map.items():
            response.cell_map[key].x = value['x']
            response.cell_map[key].y = value['y']
        return response


# get the grpc port
config = json.load(open("config.json", "rt"))
grpcport = config["grpcport"]

# creat a grpc server :
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

simulator_pb2_grpc.add_SimulatorServicer_to_server(SimulationServicer(), server)

print("Starting server. Listening on port : " + str(grpcport))
server.add_insecure_port("[::]:{}".format(grpcport))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
