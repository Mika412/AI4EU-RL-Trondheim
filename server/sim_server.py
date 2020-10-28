import time
from concurrent import futures

import grpc

# import the generated classes :
import simulator_pb2
import simulator_pb2_grpc
from sim_manager import SimulationManager

# import the function we made :
port = 50055
# create a class to define the server functions, derived from
class SimulationServicer(simulator_pb2_grpc.SimulateServicer):
    manager = None

    def start_simulation(self, request, context):
        # define the buffer of the response :
        self.manager = SimulationManager()

        response = simulator_pb2.InitResponse()

        # get the value of the response by calling the desired function :
        response.isRunning = self.manager.initialize(request.StartDate, request.EndDate)
        return response

    def step(self, request, context):
        # define the buffer of the response :
        response = simulator_pb2.StepResponse()
        # get the value of the response by calling the desired function :
        response.isDone = self.manager.step(request.numSteps)
        return response

    def get_emissions(self, request, context):
        response = simulator_pb2.EmissionsResponse()

        emissions = self.manager.get_emissions()

        for key, value in emissions.items():
            response.emissions[key] = value

        return response

    def change_cell_state(self, request, context):
        response = simulator_pb2.ChangeCellStateResponse()
        self.manager.change_cell_state(request.cell_state)

        return response


# creat a grpc server :
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

simulator_pb2_grpc.add_SimulateServicer_to_server(SimulationServicer(), server)

print("Starting server. Listening on port : " + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
