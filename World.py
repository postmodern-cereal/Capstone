import numpy as np
from heapq import *

class World:
	def __init__(self, size):
		self.grid = np.empty((size, size), dtype = object)

	def get_neighbors(self, node):
		#node is an ordered pair
		#neighbors are only up, down, left, right because goat can't move diagonally
		neighbors = []
		x = node[0]
		y = node[1]
		if(x != 0 and self.grid[x-1][y] != "#"):
			#there is a left neighbor
			neighbors.append((x-1, y))
		if(y != 0 and self.grid[x][y-1] != "#"):
			#there is a top neighbor
			neighbors.append((x, y-1))
		if(x != len(self.grid) - 1 and self.grid[x + 1][y] != "#"):
			#there is a right neighbor
			neighbors.append((x + 1, y))
		if(y != len(self.grid) - 1 and self.grid[x][y + 1] != "#"):
			neighbors.append((x, y + 1))
		return neighbors

	def cost(self, current, neighbor):
		#currently just a place holder because all moves are the same cost, but i'll need this later if i implement difficult terrain
		return 1

	def fill_grid(self, fileName):
		#takes input from a file and interprets it as world data
		fo = open(fileName, "r")
		#now read the entire file to a string
		raw = fo.read()
		fo.close()
		xidx = 0;
		yidx = 0;
		for letter in raw:
			if (letter != '\n'):
				self.grid[xidx][yidx] = letter
				yidx+=1
			else:
				xidx+=1
				yidx = 0
		#print(self.grid)

	def display_world(self):
		for i in range (0, len(self.grid)):
			for point in self.grid[i]:
				print(point + " ", end = '')

			print()

	def heuristic(self, first, second):
		#heuristic based on manhattan distance
		(x1, y1) = first
		(x2, y2) = second
		return abs(x1 - x2) + abs(y1 - y2)

	def a_star(self, start, destination):
		#start and destination are coordinates
		frontier = []
		heappush(frontier, (0, start))	#add start to frontier
		#dictionary containing best ancestor to a given node
		parent = {}
		parent[start] = None
		#cost of start to a given node
		g_score = {}
		g_score[start] = 0

		while not len(frontier) == 0:
			#pop lowest priority point from queue, and seperate it from its priority
			current = heappop(frontier)[1]

			if current == destination:
				break

			for neighbor in self.get_neighbors(current):
				neighbor_cost = g_score[current] + self.cost(current, neighbor)
				if neighbor not in g_score or neighbor_cost < g_score[neighbor]:
					g_score[neighbor] = neighbor_cost
					heappush(frontier, (neighbor_cost + self.heuristic(destination, current), neighbor))
					parent[neighbor] = current
		if current != destination:
			path = "FAIL"
		return parent

	def create_path(self, parent, node):
		path = []
		path.append(node)
		while node in parent:
			node = parent[node]
			if node != None:
				path.append(node)
		#before returning, we need to reverse the list so that it's a path from start to goal
		path = list(reversed(path))
		return path

	def show_path(self, path):
		#left arrow: \u2190
		#right arrow: \u2192
		#up arrow: \u2191
		#down arrow: \u2193
		#shows the path on the grid for easy path visualization
		for i in range (0, len(self.grid)):
			for j in range (0, len(self.grid)):
				if((i, j) in path):
					print("~ ", end = '')
				else:
					print(self.grid[i][j] + " ", end = "")
			print()

a = World(20)
a.fill_grid("bar.txt")
print(a.get_neighbors((0, 0)))
print(a.grid[1][0])
a.display_world()
parent = a.a_star((0, 0), (0, 18))
a.show_path(a.create_path(parent, (0, 18)))
a.display_world()
