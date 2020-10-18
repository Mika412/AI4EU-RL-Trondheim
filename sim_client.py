from random import randint
from timeit import default_timer as timer

import grpc

# import the generated classes
import model_pb2
import model_pb2_grpc

start_ch = timer()
port_addr = "localhost:50055"

# open a gRPC channel
channel = grpc.insecure_channel(port_addr)

# create a stub (client)
stub = model_pb2_grpc.SimulateStub(channel)

StartDate = "2020-02-01"
EndDate = "2020-02-02"
EmissionsThreshold = 50

# Start Simulation
requestStartSimulation = model_pb2.InitRequest(StartDate=StartDate, EndDate=EndDate)
stub.start_simulation(requestStartSimulation)

requestStep = model_pb2.StepRequest(numSteps=1)
requestEmissions = model_pb2.EmissionsRequest()
is_done = False
while not is_done:
    is_done = stub.step(requestStep).isDone

    emissions = stub.get_emissions(requestEmissions).emissions
    requestCellChangeState = model_pb2.ChangeCellStateRequest()

    # Check all cell emissions values and close the ones that are over the threshold
    for key, value in emissions.items():
        requestCellChangeState.cell_state[key] = value >= EmissionsThreshold

    stub.change_cell_state(requestCellChangeState)
