import json
import grpc
import time

import agent_pb2
import simulator_pb2
import agent_pb2_grpc
import simulator_pb2_grpc

configfile = "config.json"
config = json.load(open(configfile, "rt"))


def main():
    sim_channel = grpc.insecure_channel("localhost:50055")
    # sim_channel = grpc.insecure_channel('localhost:'+str(config['simulator-grpcport']))
    sim_request_stub = simulator_pb2_grpc.SimulatorStub(sim_channel)

    agent_channel = grpc.insecure_channel("localhost:50056")
    # agent_channel = grpc.insecure_channel('localhost:'+str(config['agent-grpcport']))
    agent_stub = agent_pb2_grpc.AgentStub(agent_channel)

    StartDate = "2020-02-01"
    EndDate = "2020-02-02"
    DensityPerc = 1.0

    # Start Simulation
    initRequest = simulator_pb2.InitRequest(
        StartDate=StartDate, EndDate=EndDate, DensityPerc=DensityPerc
    )
    emissionsState = sim_request_stub.start_simulation(initRequest)
    # guijob = gui_request_stub.requestSudokuEvaluation(initRequest)
    while not emissionsState.hasEnded:
        try:

            agent_actions = agent_stub.get_action(emissionsState)

            emissionsState = sim_request_stub.step(agent_actions)

        #
        except Exception as e:
            print("Got an exception " , str(e))
            # do not spam
            time.sleep(2)


main()
