FROM ubuntu:18.04

MAINTAINER Mykhaylo "mykhamarf17@gmail.com"

# RUN apk add --update g++ gcc libxslt-dev
ENV TZ=Europe/Lisbon
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN ln -s /usr/bin/python3 /usr/bin/python & ln -s /usr/bin/pip3 /usr/bin/pip

RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN apt-get install cmake -y
RUN pip3 install --upgrade pip

WORKDIR /

COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt

RUN apt-get install libglib2.0-0 -y
copy model /model
COPY tf_models.py agent_pb2.py agent_pb2_grpc.py agent_actor.py agent_server.py config.json ./

ENTRYPOINT [ "python3","agent_server.py" ]
