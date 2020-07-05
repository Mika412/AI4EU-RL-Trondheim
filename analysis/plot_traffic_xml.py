import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import os
import sys
import xml.etree.ElementTree as ET

class SensorData:
    def __init__(self,sensor_id):
        self.id = sensor_id
        self.directions = []
        self.real_traff = []
        self.simul_traff = []
        
    def add_direction(self,direction,real,simul):
        self.directions.append(direction)
        self.real_traff.append(real)
        self.simul_traff.append(simul)
	
map = sys.argv[1]
from_date = sys.argv[2]
to_date = sys.argv[3]
print(from_date)
print(to_date)
	
simul_period = from_date.replace('-','') + 'T0000_' + to_date.replace('-','') + 'T0000'
print(simul_period)

sensor_loc = pd.read_csv('../sensors/sensor_location.csv',delimiter=';')

# Load from the generated induction file
# data_simul = pd.read_csv('../simulations/'+ map + '/data/inductiondetections.csv', delimiter=',', engine='python', na_values=['-'])
root = ET.parse('../simulations/'+ map + '/data/inductiondetections.tmp.xml').getroot()

rows = []
for elem in root:
    tag = {}
    tag["Detector"] = elem.attrib['id']
    tag["Time"] = int(float(elem.attrib['begin']))
    tag["qPKW"] = int(float(elem.attrib['nVehContrib']))
    rows.append(tag)

data_simul = pd.DataFrame(rows)
print(data_simul)
#sensors_in_map =[]
#for s in data_simul['Detector'].unique():
#    sensors_in_map.append(s.split(sep='_')[0])
sensors_in_map=data_simul['Detector'].str.split(pat='_',n=1).str[0].unique()

#Start by creating a dict to index all sensors in map
all_sensor = {}
#Iterate over all sensors
for sens in sensors_in_map:
    print(sens)
    #For each sensor add a new entry in the dict
    all_sensor[sens]=SensorData(sens)
    #And read real traffic data (sensor id helps to get the correct file)
    data_real=pd.read_csv('../sensors/data/'+sens+'_hour_'+ simul_period +'.csv', delimiter=';', engine='python', na_values=['-'])
    
    #Then, for each sensor, loop through both directions. Final goal is to sum up the traffic in both directions
    for direct in sensor_loc[sensor_loc['Detector ID']==sens]['Direction'].unique():
        #print(direct)
        #Get all lanes in given direction
        lanes = sensor_loc[(sensor_loc['Detector ID']==sens) & (sensor_loc['Direction']==direct)]['Detector Lane']
        #Initialize array for traffic in this direction (number of entries equal to number of hours in the csv)
        n_hours = len(data_real[data_real['Felt']=='Totalt'])
        real_traff_direction = np.zeros(n_hours)
        simul_traff_direction = np.zeros(n_hours)
        #Loop over all lanes in this direction, and sum traffic ammount on lane to direction total
        for lane in lanes:
            #print(lane)
            #Read real traffic data for lane and add it to direction count
            #print('size = {}'.format(data_real[data_real['Felt']==str(lane)]['Volum'].values.size))
            if data_real[data_real['Felt']==str(lane)]['Volum'].values.size != 0:
                #print('real_traff_direction = {}'.format(real_traff_direction))
                #print('new_val = {}'.format(data_real[data_real['Felt']==str(lane)]['Volum'].values))
                real_traff_direction += data_real[data_real['Felt']==str(lane)]['Volum'].values
            
            #Now read simulated data, and parse it according to its format (is not yet aggregated per hour)
            simul_data_lane = data_simul[data_simul.Detector == str(sens+'_'+str(lane))]
            h=0
            simul_traff_lane = np.zeros(n_hours)
            for index, row in simul_data_lane.iterrows():
                # print(row)
                if row.Time > n_hours*3600 or h >= 24:
                    continue
                if row.Time < h*3600:
                    simul_traff_lane[h-1] += row.qPKW
                else:
                    h+=1
                    simul_traff_lane[h-1] += row.qPKW
            
            simul_traff_direction += simul_traff_lane
            #print(simul_traff_lane)
            
        #Save result in data structure
        #print(direct)
        #print(all_sensor[sens].directions)
        all_sensor[sens].add_direction(direction=direct,real=real_traff_direction,simul=simul_traff_direction)
        
print(os.getcwd())
if not os.path.exists('figs/from_'+ from_date + '_to_' + to_date):
        os.mkdir('figs/from_'+ from_date + '_to_' + to_date)
    
for sens in all_sensor:
    for idx, direct in enumerate(all_sensor[sens].directions):
        plt.plot(all_sensor[sens].real_traff[idx],label='real traffic')
        plt.plot(all_sensor[sens].simul_traff[idx],label='simul traffic')
        plt.xlabel("Hour")
        plt.ylabel("Traffic")
        plt.legend()
        plt.savefig('figs/from_'+ from_date + '_to_' + to_date + '/'+str(sens)+'_to_'+str(direct)+'.png',format='png',dpi=200)
        plt.clf()
