import os
import string
import sys
from collections import Counter
from os import listdir
from os.path import isfile, join
from xml.etree import ElementTree
from xml.sax.saxutils import escape
from lxml import etree

import pandas as pd

outer_template = string.Template("""<detectors>
${document_list}
</detectors>
""")
inner_template = string.Template(
    '    <detectorDefinition id="${id}" lane="${lane}" pos="${position}" type="${type}"></detectorDefinition>')

detections_file = "detections.csv"
detectors_file = "detectors.xml"

induction_loops_file = "induction_loops.add.xml"
induction_outer_template = string.Template("""<additional>
${document_list}
</additional>
""")
induction_inner_template = string.Template(
    '<inductionLoop id="${id}" lane="${lane}" pos="${position}" type="${type}" freq="1" file="inductiondetections.tmp.xml"/>')


class Detector:
    def __init__(self, name, lane, pos, speed_limit, sType):
        self.name = name
        self.lane = lane
        self.pos = pos
        self.speed_limit = speed_limit
        self.timestep_count_dict = {}
        self.type = sType


def get_unique_lanes(map_location):
    parser = etree.XMLParser(recover=True)
    tree = ElementTree.parse(map_location, parser=parser)
    root = tree.getroot()
    lanes = []
    for edge in root.findall("edge"):
        for lane in edge.findall("lane"):
            lane = lane.attrib['id']
            lanes.append(lane)
    return list(set(lanes))


def processSensorData(map_location, sensor_file_location, sensors_directory, output_location, start_offset=0,
                      max_steps=1, percentage_to_use=1):
    map_lanes = get_unique_lanes(map_location)
    detectors_output = pd.DataFrame(columns=['Detector', 'Time', 'qPKW', 'vPKW'])

    # Get the sensor locations
    sensor_location_dt = pd.read_csv(sensor_file_location, sep=';', header=0, encoding='unicode_escape')

    detectors = {}
    sensor_files = [f for f in listdir(sensors_directory) if isfile(join(sensors_directory, f))]
    # Get the sensor details
    for sensor_file in sensor_files:

        name = sensor_file.split("_hour_")[0]
        file_location = sensors_directory + sensor_file
        # For each sensor create a dictionary
        sensors = sensor_location_dt.loc[sensor_location_dt['Detector ID'] == name]
        for index, sensor in sensors.iterrows():
            sensor_id = sensor['Detector ID'] + '_' + str(sensor['Detector Lane'])
            if sensor['SUMO Lane ID'] in map_lanes:
                detectors[sensor_id] = Detector(sensor_id, sensor['SUMO Lane ID'], str(sensor['Position']),
                                                sensor['Speed Limit'], sensor['Type'])
        data = pd.read_csv(file_location, sep=';', header=0, encoding='unicode_escape', na_values=["-"])
        data.head()
        data = data.dropna()
        # For each entry append to list
        for index, row in data.iterrows():
            if not row['Felt'].isdigit():
                # print(row['Felt'])
                continue
            lane = row['Felt']
            current_timestep = row['Fra']
            if not name + '_' + lane in detectors:
                continue
            prev_elem = detectors[name + '_' + lane].timestep_count_dict.get(current_timestep)
            if prev_elem == None:
                prev_elem = 0
            # prev_elem += row["< 5,6m"] + row[">= 5,6m"] + row["5,6m - 7,6m"] + row["7,6m - 12,5m"] + row["12,5m - 16,0m"] + row["16,0m - 24,0m"] + row[">= 24,0m"]
            # print(row["< 5,6m"])
            prev_elem += int(row["< 5,6m"] * percentage_to_use)
            detectors[name + '_' + lane].timestep_count_dict[current_timestep] = prev_elem
    
    currentDetector = 1
    # Create detectors output
    for k, dt in detectors.items():
        counter = 0
        print("Detector: " + str(currentDetector) + "/" + str(len(detectors)))
        for key in sorted(dt.timestep_count_dict.keys()):
            if dt.timestep_count_dict.get(key) == 0:
                continue
            if max_steps > 0 and counter >= max_steps:
                break
            detectors_output = detectors_output.append(
            {'Detector': dt.name, 'Time': int(counter * 60) + start_offset, 'qPKW': dt.timestep_count_dict.get(key),
                'vPKW': dt.speed_limit}, ignore_index=True)
            
            counter += 1

        currentDetector += 1
    
    # sys.exit()
    if not os.path.exists(output_location):
        os.makedirs(output_location)
    detectors_output = detectors_output.sort_values('Time')

    # Write the detectors
    detectors_output.to_csv(output_location + detections_file, sep=';', index=False)

    # Create the detections object
    inner_contents = []
    for k, dt in detectors.items():
        inner_contents.append(
            inner_template.substitute(id=dt.name, lane=dt.lane, position=escape(dt.pos), type=dt.type))

    result = outer_template.substitute(document_list='\n'.join(inner_contents))

    file1 = open(output_location + detectors_file, "w")
    file1.write(result)
    file1.close()

    # Create the induction loop objects
    inner_contents = []
    for k, dt in detectors.items():
        inner_contents.append(
            induction_inner_template.substitute(id=dt.name, lane=dt.lane, position=escape(dt.pos), type=dt.type))

    result = induction_outer_template.substitute(document_list='\n'.join(inner_contents))

    file1 = open(output_location + induction_loops_file, "w")
    file1.write(result)
    file1.close()