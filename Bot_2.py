import numpy as np
class Bot_2:



	def __init__(self, rows, cols, initial_memory):
		self.rows = rows
		self.cols = cols
		self.previous_action = ""
		self.next_action = "s"
		#action codes tell world what agent wants to do next
		#s = sense
		#m = move
		#r = rotate
		self.currentDestination = ()    #where agent wants to go next
		self.currentPath = []           #path to destination


		#example is 8 lines by 19 chars
		self.working_memory = np.empty((rows, cols), dtype=object)
		self.reference_memory = initial_memory
		(self.xpos, self.ypos) = self.get_position()

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

	def sweep_complete(self):
		#do a bfs starting at agent pos, stop when either have looked at everything or found unexplored space

		#do the bfs
		nodeQueue = [(self.xpos, self.ypos)]       #queue of unseen nodes
		viewedNodes = {()}                           #already viewed nodes

		while len(nodeQueue) > 0:
			current = nodeQueue.pop(0)

			if self.working_memory[current[0]][current[1]] == None:
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

	def get_next_action(self):
		#decide what to do next
		#flow should work like this in a loop:
			#1. sense surroundings
			#2. integrate sensor data
			#3. pick next thing to look at
			#4. get to that space
			#5. go to 1 unless finished sensing
		if (self.xpos, self.ypos) == self.currentDestination:
			self.nextAction = "s"

	def sense(self):
		self.world.get_sensor_data()

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

			self.grid[x][y] = content
