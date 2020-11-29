#!/bin/bash

set -ex

for component in simulator agent; do
  pushd $component
  ./docker-build.sh
  popd
done
