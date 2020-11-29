import json
import grpc

import agent_pb2
import simulator_pb2
import agent_pb2_grpc
import simulator_pb2_grpc

configfile = "config.json"
config = json.load(open(configfile, 'rt'))

def main():
    sim_channel = grpc.insecure_channel('localhost:50055')
    # sim_channel = grpc.insecure_channel('localhost:'+str(config['simulator-grpcport']))
    sim_request_stub = simulator_pb2_grpc.SimulatorStub(sim_channel)

    agent_channel = grpc.insecure_channel('localhost:50056')
    # agent_channel = grpc.insecure_channel('localhost:'+str(config['agent-grpcport']))
    agent_stub = agent_pb2_grpc.AgentStub(agent_channel)


    StartDate = "2020-02-01"
    EndDate = "2020-02-02"
    EmissionsThreshold = 50

    # Start Simulation
    initRequest = simulator_pb2.InitRequest(StartDate=StartDate, EndDate=EndDate)
    emissionsState = sim_request_stub.start_simulation(initRequest)
    # guijob = gui_request_stub.requestSudokuEvaluation(initRequest)
    while True:
      try:

        agent_actions = agent_stub.get_action(emissionsState)

        emissionsState = sim_request_stub.step(agent_actions)
    #     logging.info("calling SudokuDesignEvaluationRequestDataBroker.requestSudokuEvaluation() with empty dummy")
    #     dummy1 = sudoku_gui_pb2.SudokuDesignEvaluationRequest()
    #     guijob = gui_request_stub.requestSudokuEvaluation(dummy1)
    #
    #     logging.info("calling SudokuDesignEvaluationProblemEncoder.evaluateSudokuDesign() with guijob")
    #     solverjob = evaluator_program_encoder_stub.evaluateSudokuDesign(guijob)
    #
    #     logging.info("calling OneshotSolver.solve() with parameters %s", solverjob.parameters)
    #     aspresult = aspsolver_stub.solve(solverjob)
    #
    #     logging.info("calling SudokuDesignEvaluationResultDecoder.processEvaluationResult() with %d answer sets and description %s",
    #       len(aspresult.answers), aspresult.description)
    #     evalresult = evaluator_result_decoder_stub.processEvaluationResult(aspresult)
    #
    #     logging.info("calling SudokuDesignEvaluationResultProcessor.processEvaluationResult() with status %d, len(solution)=%d, len(minimal_unsolvable)=%s",
    #       evalresult.status, len(evalresult.solution), len(evalresult.inconsistency_involved))
    #     dummy2 = gui_result_stub.processEvaluationResult(evalresult)
    #
      except Exception:
        logging.error("exception (retrying after 2 seconds): %s", traceback.format_exc())
        # do not spam
        time.sleep(2)

main()
