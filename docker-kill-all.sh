#!/bin/bash

for component in simulator agent; do
	pushd $component
	./docker-kill.sh
	popd
done
