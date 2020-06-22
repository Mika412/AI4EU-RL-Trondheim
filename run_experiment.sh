#!/bin/bash

#This script runs everything needed to setup a simulation, from downloading traffic data, running simulation and plotting outputs.

#It needs two input arguments, in the format yyyy-mm-dd
#   (1) start date
#   (2) end date - note, this one is always the next day from the desired end. E.g, if you want to simulate until 2020-01-15 (end of day) you need to give as input 2020-01-16

source ~/.bashrc
conda activate sumo

cwd=${PWD}

from_date=${1}
to_date=${2}

#n_days=$(dateutils.ddiff ${from_date} ${to_date})
n_days=$(( ($(date -d ${to_date} +%s) - $(date -d ${from_date} +%s)) / 86400))

echo "N days is ${n_days}"
echo "N hours is $((n_days*24))"
echo "N seconds is $((n_days*86400))"

rm ${cwd}/sensors/data/*.csv

cd ${cwd}/scripts
python download_sensors.py -i ../sensors/sensor_location.csv -o ../sensors/data -s ${from_date} -e ${to_date}

cd ${cwd}
python generate_data.py -m simulations/small_extended -s sensors -t $((n_days*24)) -pe 1 --poly-max-width 3600 --poly-max-height 2400 --poly-width 100 --poly-height 100 -p -r -d

python experiments/normal_simulation/CustomExperiment.py $((n_days*86400))

cd ${cwd}/analysis/nilu_data

wget "https://api.nilu.no/obs/historical/${from_date}%2000:00/${to_date}%2000:00/torvet?components=no2" -O torvet_${from_date}_${to_date}_no2.json
wget "https://api.nilu.no/obs/historical/${from_date}%2000:00/${to_date}%2000:00/elgeseter?components=nox" -O elgeseter_${from_date}_${to_date}_nox.json
wget "https://api.nilu.no/obs/historical/${from_date}%2000:00/${to_date}%2000:00/bakke kirke?components=nox" -O bakke_kirke_${from_date}_${to_date}_nox.json

cd ${cwd}/analysis

python plot_traffic.py ${from_date} ${to_date}
python plot_emissions.py ${from_date} ${to_date}
