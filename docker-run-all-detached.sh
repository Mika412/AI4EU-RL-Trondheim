#!/bin/bash

set -ex

for component in simulator agent; do
	pushd $component
	./docker-run-detached.sh
	popd
done
