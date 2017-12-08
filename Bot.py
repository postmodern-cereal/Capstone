import numpy as np
class Bot:

	def __init__(self, xpos, ypos, size, world):
		self.xpos = xpos
		self.ypos = ypos
		self.graph = {'(0, 0)': []}			#dictionary
		#the entries in the dictionary are lists
		#the first element of the list is the type of node: food, obstacle, etc
		#the remaining elements are the neighbors of the node
		self.food_reserves = 10	#can go 10 squares before starving
		self.world = world

	def get_neighbors(self, node):
		#node is an ordered pair
		#neighbors are only up, down, left, right because goat can't move diagonally
		neighbors = []
		x = node[0]
		y = node[1]
		#the value none indicates an unfilled square. Since we don't know whether it's an obstacle, we assume that it is
		if(x != 0 and (self.grid[x-1][y] != "#" or None)):
			#there is a left neighbor
			neighbors.append((x-1, y))
		if(y != 0 and (self.grid[x][y-1] != "#" or None)):
			#there is a top neighbor
			neighbors.append((x, y-1))
		if(x != len(self.grid) - 1 and (self.grid[x + 1][y] != "#" or None)):
			#there is a right neighbor
			neighbors.append((x + 1, y))
		if(y != len(self.grid) - 1 and (self.grid[x][y + 1] != "#" or None)):
			neighbors.append((x, y + 1))
		return neighbors

	def cost(self, current, neighbor):
		#currently just a place holder because all moves are the same cost, but i'll need this later if i implement difficult terrain
		return 1

	#def sense_area(self):
		#gets data from the agent's world
		#get data from world, and include a world function to give it

	def add_data(self, node, node_type, neighbors):
		#takes sensor data from the world and incorporates it
		#takes data for one node at a time
		if node in self.graph:
			#we will append to the existing entry in a way that overwrites all old data
			#it is possible that not all neighbors of this node were visible when it was first added to the graph, and its type may have changed due to being eaten
			self.graph[node] = [node_type]
			self.graph[node].extend[neighbors]

	def display_graph(self):
		
