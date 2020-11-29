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

        # get the value of the response by calling the desired function :
        emissions = self.manager.initialize(request.StartDate, request.EndDate)

        for key, value in emissions.items():
            response.emissions[key] = value

        response.currentStep = self.manager.current_step()
        return response

    def step(self, request, context):
        # define the buffer of the response :
        response = simulator_pb2.StateResponse()

        # get the value of the response by calling the desired function :
        emissions = self.manager.step(request.cell_state, request.numSteps)

        for key, value in emissions.items():
            response.emissions[key] = value

        response.currentStep = self.manager.current_step()

        return response

# get the grpc port
config = json.load(open("config.json", 'rt'))
grpcport = config['grpcport']

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
