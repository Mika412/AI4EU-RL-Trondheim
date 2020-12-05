#!/bin/bash

for component in simulator reactive-agent; do
	pushd $component
	./docker-kill.sh
	popd
done
