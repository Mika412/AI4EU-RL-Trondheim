# Instructions

## Overview

## Adding new agent

## Training an agent

## Building

After changing any protobuf file, run these commands to populate the correct
directories and build the stubs:
```console
./populate-duplicate-protobufs.sh
./rebuild-all-protobufs.sh
```

To build the docker images, you can go to each directory, `rl-agent`,
`reactive-agent`, `simulator`, and run this command:

```console
./{folder}/docker-build.sh
```

Alternatively you can run the helper script that will trigger the build for all
the images:

```console
./docker-build.sh
```

## Running

To run the project locally, first you need to run the docker images and then the
orchestrator. Alternatevily you can upload the images to the Acumos platform and
deploy it to a Kubernetes cluster. 

### Docker images

There are two modes that you can run the images, in interactive or detached.
Interactive will block the terminal and print out what is happening in the
image. Detached is non-blocking and runs in the background.

To run the images, you can go to each directory, `rl-agent`,
`reactive-agent`, `simulator`, and run one of these commands:

* For interactive:
```console
./{folder}/docker-run-interactive.sh
```

* For detached:
```console
./{folder}/docker-run-detached.sh
```

Alternatevily, you can run all the images simultaneously. You'll have to change
the script if you want to change the agent that is being run.
```console
./docker-run-all-detached.sh
```

To kill all detached images, you can run:
```console
./docker-kill-all.sh
```
**_Note:_** Make sure not to run two agents simultaneously.

### Orchestrator

Orchestrator aims to emulate the Acumos connections. It has hardcoded
connections for the agent and the simulator. 

First run the agent and the simulator, and then you can start the orchestrator
by running:

```console
python ./orchestrator/orchestrator.py 
```
