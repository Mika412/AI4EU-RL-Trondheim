from .BaseModule import BaseModule
from xml.etree import ElementTree
from lxml import etree
import os
import sys
import numpy as np
import math
# if 'SUMO_HOME' in os.environ:
sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
#import libsumo as traci
import traci

class Cell:
	def __init__(self, cell_id, bottom_X, bottom_Y, top_X, top_Y, matrixPosX, matrixPosY):
		self.cell_id = cell_id

		self.bottomX = bottom_X
		self.bottomY = bottom_Y

		self.topX = top_X
		self.topY = top_Y

		self.matrixPosX = matrixPosX
		self.matrixPosY = matrixPosY

		self.corners = [[self.bottomX, self.bottomY], [self.bottomX, self.topY], [self.topX, self.bottomY],
						[self.topX, self.topY]]


	def belongsTo(self, x, y):
		return (x > self.bottomX) and (x < self.topX) and (y > self.bottomY) and (y < self.topY)


class CellsModule(BaseModule):
	def __init__(self, cells_file, cells_edge_file, cell_max_height, cell_max_width, cell_height, cell_width, unmutable_edges = []):
		super().__init__()

		self._traci = traci
		self._cells_file = cells_file
		self._cells_edge_file = cells_edge_file


		# Cells details
		self.cell_height = cell_height
		self.cell_width  = cell_width
		self.xCount = int(cell_max_width/self.cell_width)
		self.yCount = int(cell_max_height/self.cell_height)
		self.cells = {}
		self.cells_to_edges = {}
		self.edge_to_cells = {}
		self.cells_id_matrix = np.empty(shape=(self.yCount, self.xCount), dtype="S10")

		# Edges
		self.unmutable_edges = unmutable_edges
		self.closed_cells   = []
		self.closed_edges   = []


		self.load_cells()
		self.load_cell_edges()

		valid_cells = []
		for cell_id in self.cells:
			if cell_id in self.cells_to_edges:
				valid_cells.append([self.cells[cell_id].matrixPosY,self.cells[cell_id].matrixPosX])
		print(self.xCount, self.yCount)
		print(valid_cells)

	def load_cells(self):
		parser = etree.XMLParser(recover=True)
		tree = ElementTree.parse(self._cells_file, parser=parser )
		root = tree.getroot()

		for poly in root.findall('poly'):
			cellId = poly.attrib['id']
			shape = poly.attrib['shape'].split()
			bottomX, bottomY    = [float(x) for x in shape[0].split(',')]
			topX, topY          = [float(x) for x in shape[2].split(',')]
			xPos = int(math.floor(bottomX/self.cell_width))
			yPos = int(math.floor(bottomY/self.cell_height))
			self.cells[cellId] = Cell(cellId, bottomX, bottomY, topX, topY, xPos, yPos)
			self.cells_id_matrix[yPos, xPos] = cellId

	def load_cell_edges(self):
		parser = etree.XMLParser(recover=True)
		tree = ElementTree.parse(self._cells_edge_file, parser=parser)
		root = tree.getroot()

		for cell in root.findall('taz'):
			cellId = cell.attrib['id']
			edges  = cell.attrib['edges'].split()

			self.cells_to_edges[cellId] = edges
			for edge in edges:
				if not edge in self.edge_to_cells:
					self.edge_to_cells[edge] = []

				self.edge_to_cells[edge].append(cellId)

	def get_cell_edges(self, cellId):
		return self.cells_to_edges[cellId]


	def get_neighbors_ids(self, cellId):
		_cell = self.cells[cellId]
		neighbors = []
		neighbors.append(self.cells_id_matrix[_cell.matrixPosY-1,_cell.matrixPosX-1])
		neighbors.append(self.cells_id_matrix[_cell.matrixPosY-1,_cell.matrixPosX])
		neighbors.append(self.cells_id_matrix[_cell.matrixPosY-1,_cell.matrixPosX+1])
		neighbors.append(self.cells_id_matrix[_cell.matrixPosY,_cell.matrixPosX-1])
		neighbors.append(self.cells_id_matrix[_cell.matrixPosY,_cell.matrixPosX+1])
		neighbors.append(self.cells_id_matrix[_cell.matrixPosY+1,_cell.matrixPosX-1])
		neighbors.append(self.cells_id_matrix[_cell.matrixPosY+1,_cell.matrixPosX])
		neighbors.append(self.cells_id_matrix[_cell.matrixPosY+1,_cell.matrixPosX+1])
		neighbors = [i.decode("utf-8") for i in neighbors]
		return neighbors
		
	def close_cell(self, cell_id):
		if cell_id in self.closed_cells or not cell_id in self.cells or not cell_id in self.cells_to_edges :
			return
		
		for edge in self.cells_to_edges[cell_id]:
			if not edge in self.unmutable_edges and not edge in self.closed_edges:
				for n in range(self._traci.edge.getLaneNumber(edge)):
					self._traci.lane.setAllowed(edge + "_" + str(n), [])
				self.closed_edges.append(edge)

		self.closed_cells.append(cell_id)
	def open_cell(self, cell_id):
		if not cell_id in self.closed_cells or not cell_id in self.cells or not cell_id in self.cells_to_edges:
			return

		for edge in self.cells_to_edges[cell_id]:
			if not edge in self.unmutable_edges and edge in self.closed_edges:
				for n in range(self._traci.edge.getLaneNumber(edge)):
					self._traci.lane.setAllowed(edge + "_" + str(n), ['passenger'])
				self.closed_edges.remove(edge)
		self.closed_cells.remove(cell_id)

	def cell_ids(self):
		pass

	@property
	def variable_name(self):
		return "cells"
	
	def step(self, timestep):
		pass
	
	def reset(self):
		pass
