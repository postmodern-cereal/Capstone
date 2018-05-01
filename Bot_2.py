import numpy as np
from heapq import *
class Bot_2:



	def __init__(self, rows, cols, initial_memory):
		self.rows = rows
		self.cols = cols
		self.previous_action = ""
		self.next_action = "s"
		#action codes tell world what agent wants to do next
		#s = sense
		#m = move
		#c = check for unseen
		#n = done, ready to start new sweep
		self.destination = ()    #where agent wants to go next
		self.currentPath = []           #path to destination


		#example is 8 lines by 19 chars
		self.working_memory = np.empty((rows, cols), dtype=object)
		self.reference_memory = initial_memory
		(self.xpos, self.ypos) = self.get_position()

	def set_xpos(self, x):
		self.xpos = x

	def set_ypos(self, y):
		self.ypos = y

	def set_position(self, position):
		self.working_memory[self.xpos][self.ypos] = "_"
		self.set_xpos(position[0])
		self.set_ypos(position[1])
		self.working_memory[self.xpos][self.ypos] = "A"

	def display_ref_memory(self):

		for x in range (0, self.rows):
			if(x < 10):
				print(x, end="  ")
			else:
				print(x, end=" ")
			for y in range (0, self.cols):
				if self.reference_memory[x][y] == None:
					print("~", end='')
				else:
					print(self.reference_memory[x][y], end='')
			print()

	def display_memory(self):

		for x in range (0, self.rows):
			if(x < 10):
				print(x, end="  ")
			else:
				print(x, end=" ")
			for y in range (0, self.cols):
				if self.working_memory[x][y] == None:
					print("~", end='')
				else:
					print(self.working_memory[x][y], end='')
			print()

	def reset(self):
		#resets agent for another sweep
		#set working mem as ref mem
		#set next action as s
		#reset prev action, destination, path
		self.reference_memory = self.working_memory
		self.working_memory = np.empty((self.rows, self.cols), dtype=object)
		self.previous_action = ""
		self.next_action = "s"
		self.destination = ()
		self.currentPath = []

	def get_position(self):
		#searches its memory for its current location (will have an A)
		for x in range(0, self.rows):
			for y in range(0, self.cols):
				if self.reference_memory[x][y] == "A":
					return (x, y)

	def display_map(self):
		for i in range (0, self.rows):
			for j in range (0, self.cols):
				print(self.working_memory[i][j], end='')
			print()

	def get_children(self, node, viewed):
		#return neighors of node
		#if a given child has already been added to the queue, it is ignored
		#note that this ignores whether a cell would be visible from the agent's location
		#this means we have to deal with situations where a neighbor is some sort of void that can never be seen by the agent (e.g. space outside building)
		children = []

		#top row
		if node[0] > 0:
			#add top middle child
			if not (node[0]-1, node[1]) in viewed:
				children.append((node[0]-1, node[1]))

			if node[1] > 0:
				#top left exists
				if not (node[0]-1, node[1]-1) in viewed:
					children.append((node[0]-1, node[1]-1))

			if node[1]+1 < self.cols:
				#top right exists
				if not (node[0]-1, node[1]+1) in viewed:
					children.append((node[0]-1, node[1]+1))

		#right middle
		if node[1]+1 < self.cols:
			#add right middle child
			if not (node[0], node[1]+1) in viewed:
				children.append((node[0], node[1]+1))

		#left middle
		if node[1] > 0:
			#add left middle child
			if not (node[0], node[1]-1) in viewed:
				children.append((node[0], node[1]-1))

		#bottom row
		if node[0]+1 < self.rows:
			#add bottom middle
			if not (node[0]+1, node[1]) in viewed:
				children.append((node[0]+1, node[1]))

			if node[1] > 0:
				#add bottom left child
				if not (node[0]+1, node[1]-1) in viewed:
					children.append((node[0]+1, node[1]-1))

			if node[1]+1 < self.cols:
				#add bottom right child
				if not (node[0]+1, node[1]+1) in viewed:
					children.append((node[0]+1, node[1]+1))

		return children

	def check_for_unseen(self):
		#do a bfs starting at agent pos, stop when either have looked at everything or found unexplored space

		#do the bfs
		nodeQueue = [(self.xpos, self.ypos)]       #queue of unseen nodes
		viewedNodes = {()}                           #already viewed nodes

		while len(nodeQueue) > 0:
			current = nodeQueue.pop(0)
			#print("Current: ", current)
			if self.working_memory[current[0]][current[1]] == None:
				if self.reference_memory[current[0]][current[1]] == "+":
					#the current cell is a void space in the original and should be ignored
					#add it to working memory so it's copied over later
					self.working_memory[current[0]][current[1]] = "+"
					continue
				return current

			else:
				#add next vertices to queue
				currentChildren = self.get_children(current, viewedNodes)
				nodeQueue.extend(currentChildren)
				for node in currentChildren:
					viewedNodes.add(node)

			viewedNodes.add(current)

		#if we reach this, the while loop completed without finding anything
		return (-1, -1)

	def cost(self, start, neighbor):
		#get cost of going from current node to selected neighbor
		return 1

	def heuristic(self, first, second):
		#heuristic based on manhattan distance
		(x1, y1) = first
		(x2, y2) = second
		return abs(x1 - x2) + abs(y1 - y2)

	def is_available(self, cell):
        #returns true iff cell does not contain obstacle or unreachable space
		if cell == self.destination:
			return True
		return (not self.reference_memory[cell[0]][cell[1]] == "#") and (not self.reference_memory[cell[0]][cell[1]] == "+")

	def get_neighbors(self, current):
        #a separate method just for A* that ignores spaces outside the building
		x = current[0]
		y = current[1]
		neighbors = []  #holds neighboring nodes
        #top row
		if x > 0:
			#add top middle child
			if self.is_available((x-1, y)):
				#top middle is neither wall or void
				neighbors.append((x-1, y))

			# if y > 0:
			# 	#top left exists
			# 	if self.is_available((x-1, y-1)):
			# 	    #top left available
			# 	    neighbors.append((x-1, y-1))
			#
			# if y+1 < self.cols:
			# 	#top right exists
			# 	if self.is_available((x-1, y+1)):
			# 	    neighbors.append((x-1, y+1))

		#right middle
		if y+1 < self.cols:
			#add right middle child
			if self.is_available((x, y+1)):
			    neighbors.append((x, y+1))

		#left middle
		if y > 0:
			#add left middle child
			if self.is_available((x, y-1)):
			    neighbors.append((x, y-1))

		#bottom row
		if x+1 < self.rows:
			#add bottom middle
			if self.is_available((x+1, y)):
			    neighbors.append((x+1, y))

			# if y > 0:
			# 	#add bottom left child
			# 	if self.is_available((x+1, y-1)):
			# 	    neighbors.append((x+1, y-1))
			#
			# if y+1 < self.cols:
			# 	#add bottom right child
			# 	if self.is_available((x+1, y+1)):
			# 	    neighbors.append((x+1, y+1))

		return neighbors


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


	def get_next_action(self):
		#decide what to do next
		#flow should work like this in a loop:
			#1. sense surroundings
			#2. integrate sensor data
			#3. pick next thing to look at
			#4. get to that space
			#5. go to 1 unless finished sensing

		if self.next_action == "s" or (self.destination == (self.xpos, self.ypos) and not self.next_action =="c"):
			#need to tell world that want to sense
			#need to set next action to be check unseen
			toReturn = "s"		#tells world to sense stuff
			self.next_action = "c"  #next action: check for unseen
			self.previous_action = "s"  #just finished sensing
			return toReturn

		elif self.next_action == "c":
			#see if anything is left unseen
			print("Checking for unseen...")
			tmpDestination = self.check_for_unseen()
			if tmpDestination == (-1, -1):
				#sweep complete. ask world to verify and reset
				self.next_action = "n"
				return "n"

			else:
				#set destination
				print("Unseen node detected at ", tmpDestination, ". Plotting a path...")
				self.destination = tmpDestination
				#calculate path to destination




				parent = self.a_star((self.xpos, self.ypos), self.destination)

				self.currentPath = self.create_path(parent, self.destination)
				print("Path found: ", self.currentPath)
				self.previous_action = "c"  #just did a check
				self.next_action = "m"      #need to move next
				return "m"

		elif self.next_action == "m":
			#still need to move
			#the world class will determine where we want to go next by taking the first node of the path directly
			#if the move is not valid, the world will set the agent's next action to "s"
			self.previous_action = "m"
			if self.currentPath[0] == (self.xpos, self.ypos):
				currentPath.pop(0)
			return "m"


	def add_data(self, data):
		#data comes in as list of lists
		for entry in data:
			x = entry[0][0]
			y = entry[0][1]
			content = ""
			if entry[1] != " ":
				content = entry[1]
			else:
				content = "_"

			self.working_memory[x][y] = content
