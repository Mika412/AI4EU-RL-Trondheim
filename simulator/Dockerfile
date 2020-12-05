FROM ubuntu 

MAINTAINER Mykhaylo "mykhamarf17@gmail.com"

# RUN apk add --update g++ gcc libxslt-dev
ENV TZ=Europe/Lisbon
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN ln -s /usr/bin/python3 /usr/bin/python & ln -s /usr/bin/pip3 /usr/bin/pip

RUN apt update -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:sumo/stable
RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN apt-get install -y sumo
RUN pip3 install --upgrade pip

WORKDIR /

COPY ./requirements.txt ./

RUN pip3 install -r requirements.txt

ENV SUMO_HOME /usr/share/sumo

COPY src /src
COPY simulations /simulations
COPY sensors /sensors

COPY simulator_pb2.py simulator_pb2_grpc.py sim_manager.py sim_server.py generate_data.py config.json ./

ENTRYPOINT [ "python3","sim_server.py" ]
