#!/bin/bash

docker container kill $(docker container ls -q --filter name=trondheim-sumo-agent)
