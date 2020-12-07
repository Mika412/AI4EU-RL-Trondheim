#!/bin/bash

# for component in simulator reactive-agent; do
for component in simulator rl-agent; do
	pushd $component
	./docker-kill.sh
	popd
done
