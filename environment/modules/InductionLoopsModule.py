from abc import abstractmethod
import os
import sys
from .BaseModule import BaseModule
import xml.etree.ElementTree as ET
import csv

sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
#import libsumo as traci
import traci

class InductionLoopsModule(BaseModule):
	
	def __init__(self, output_dir, induction_file):
		super().__init__()

		self.traci = traci
		self.valid_induction_loops = []

		self.output_dir = output_dir

		# Load induction loops ids
		with open(induction_file, 'rb') as xml_file:
			tree = ET.parse(xml_file)
			root = tree.getroot()
			for loop in root.findall('inductionLoop'):
				inductionId = loop.attrib['id']
				self.valid_induction_loops.append(inductionId)

		self.emissions_output = self.output_dir + "inductiondetections.csv"

		with open(self.emissions_output, "w") as csv_file:
			writer = csv.writer(csv_file, delimiter=',')
			writer.writerow(["Detector", "Time", "qPKW"])

	@property
	@abstractmethod
	def variable_name(self):
		pass

	@abstractmethod
	def step(self, timestep):
		# Check if we are tracking any induction loop
		if len(self.valid_induction_loops) == 0:
			return
		

		with open(self.emissions_output, "a") as csv_file:
			writer = csv.writer(csv_file, delimiter=',')
			for loop in self.traci.inductionloop.getIDList():
				#print(loop)
				#print(self.valid_induction_loops)
				if loop in self.valid_induction_loops:
						count = self.traci.inductionloop.getLastStepVehicleNumber(loop)
						# Only write if there are any cars. Otherwise, skipping timesteps measn there were no cars
						if count > 0:
							writer.writerow([loop, int(timestep), self.traci.inductionloop.getLastStepVehicleNumber(loop)])

	@abstractmethod
	def reset(self):
		pass

	
