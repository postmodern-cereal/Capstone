import numpy as np
from heapq import *
import random
from Bot_2 import Bot_2
from bresenham  import bresenham
class World_2:
	#contains the agent object
	def __init__(self, rows, cols):
		#initialize everything the world needs to do its thing
		self.rows  = rows
		self.cols = cols
		self.grid = np.empty((rows, cols), dtype = object)
		(self.agentx, self.agenty) = self.fill_grid("Building.txt")

		self.agent = Bot_2(self.rows, self.cols, self)

	def get_agentx(self):
		return self.agentx

	def get_agenty(self):
		return self.agenty

	def set_agentx(self, xidx):
		self.agentx = xidx

	def set_agenty(self, yidx):
		self.agenty = yidx

	def is_obstacle(self, x, y):
		#returns true iff there is an obstacle at (x, y)
		return (self.grid[x][y] == "#")

	def fill_grid(self, fileName):
		#takes input from a file and interprets it as world data
		fo = open(fileName, "r")
		#now read the entire file to a string
		raw = fo.read()
		fo.close()
		xidx = 0;
		yidx = 0;
		ax = 0
		ay = 0
		for letter in raw:
			#print("Current letter: " + letter)
			#print("\t", letter == "A")
			if (letter == "A"):
				self.grid[xidx][yidx] = letter
				ax = xidx
				ay = yidx
				yidx+=1
			elif letter != '\n':
				self.grid[xidx][yidx] = letter
				yidx+=1
			else:
				xidx+=1
				yidx = 0
		return(ax, ay)
		#print(self.grid)

	def display_world(self):
		for i in range (0, self.rows):
			for j in range (0, self.cols):
				print(self.grid[i][j], end='')
			print()


	def is_obstructed(self, nodex, nodey):
		#node is the spot you are trying to see
		#step 1: make a straight line from agent to node
		#this is done using bresenham's straight line approximation algorithm
		#if any of the coordinates returned contain an obstacle, we return false. If not, we return true
		path = list(bresenham(self.agentx, self.agenty, nodex, nodey))
		for node in path:
			if self.is_obstacle(node[0], node[1]):
				if (node[0], node[1]) == (nodex, nodey):
					#we need this condition in case we are looking at an obstacle currently
					return False
				else:
					return True
		return False


	def get_sensor_data(self):
		#this time the agent can see differently
		#it looks around, and has its sight limited by obstacles
		#we use the is_obstructed method to see if a block is visible
		#returns data for a 3 block radius
		#the agent will get a list of lists as a result
		#each element of the list will contain an ordered pair and a character indicating what lives in the block

		data = []
		#check top left
		for i in range(0, (self.agentx - 10)):
			for j in range(0, (self.agenty - 10)):
				if not self.is_obstructed(i, j):
					data.append([(i, j), self.grid[i][j]])
				else:
					print(i + "," + j)

		#bottom left
		for i in range(0, (self.agentx - 10)):
			for j in range(0, (self.agenty + 10)):
				if not self.is_obstructed(i, j):
					data.append([(i, j), self.grid[i][j]])

		#top right
		for i in range(0, (self.agentx + 10)):
			for j in range(0, (self.agenty - 10)):
				if not self.is_obstructed(i, j):
					data.append([(i, j), self.grid[i][j]])

		#bottom right
		for i in range(0, (self.agentx + 10)):
			for j in range(0, (self.agenty + 10)):
				if not self.is_obstructed(i, j):
					data.append([(i, j), self.grid[i][j]])

		print(data)
		self.agent.add_data(data)


	def get_rel_pos(self, x, y):
		#gets position of coordinates relative to agent's start position
		#enables working with the agent's memory, which never knows its actual start positon
		return (x-self.offsetx, y-self.offsety)

world = World_2(8, 19)
print("Agent location:", world.agentx, ", ", world.agenty)
print("Actual world")
world.display_world()
print("Agent's knowledge")
world.agent.display_map()
print("Sensing now")
world.agent.sense()
print("Agent's new knowledge")
world.agent.display_map()
