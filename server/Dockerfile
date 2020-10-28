FROM ubuntu 

MAINTAINER Mykhaylo "mykhamarf17@gmail.com"

# RUN apk add --update g++ gcc libxslt-dev
ENV TZ=Europe/Lisbon
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN apt-get install -y sumo
RUN pip3 install --upgrade pip
COPY ./requirements.txt /requirements.txt
COPY src /src
COPY simulations /simulations
COPY sensors /sensors

COPY model_pb2.py model_pb2_grpc.py sim_manager.py sim_server.py generate_data.py ./

WORKDIR /

RUN pip3 install -r requirements.txt

ENV SUMO_HOME /usr/share/sumo

#ENTRYPOINT [ "python3","sim_server.py" ]
