#!/bin/bash

set -ex

for component in simulator reactive-agent rl-agent; do
  pushd $component
  ./docker-build.sh
  popd
done
