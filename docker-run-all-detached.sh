#!/bin/bash

set -ex

for component in simulator reactive-agent; do
	pushd $component
	./docker-run-detached.sh
	popd
done
