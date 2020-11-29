import time
from concurrent import futures

import grpc
import json

# import the generated classes :
import agent_pb2
import agent_pb2_grpc
from agent_actor import ActorManager

# import the function we made :
# create a class to define the server functions, derived from
class AgentServicer(agent_pb2_grpc.AgentServicer):
    actor = None

    def get_action(self, request, context):
        if not self.actor:
            self.actor = ActorManager()

        response = agent_pb2.StepRequest()

        new_cell_state, response.numSteps = self.actor.get_action(request.emissions, request.currentStep)

        for key, value in new_cell_state.items():
            response.cell_state[key] = value

        return response

config = json.load(open("config.json", 'rt'))
grpcport = config['grpcport']

# creat a grpc server :
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

agent_pb2_grpc.add_AgentServicer_to_server(AgentServicer(), server)

print("Starting server. Listening on port : " + str(grpcport))
server.add_insecure_port("[::]:{}".format(grpcport))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
