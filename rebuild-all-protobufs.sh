#!/usr/bin/env bash

pushd simulator
  python3 -m grpc_tools.protoc --python_out=. --proto_path=. --grpc_python_out=. *.proto
popd


pushd agent
  python3 -m grpc_tools.protoc --python_out=. --proto_path=. --grpc_python_out=. *.proto
popd


pushd orchestrator
  python3 -m grpc_tools.protoc --python_out=. --proto_path=. --grpc_python_out=. *.proto
popd
