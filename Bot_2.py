import numpy as np
class Bot_2:

	def __init__(self, rows, cols, world):
		self.rows = rows
		self.cols = cols
		#this time, we'll use a grid again
		#the assumption is that the bot has some world knowledge going in
		#it would make sense to give it the basic building layout

		#example is 8 lines by 19 chars
		self.working_memory = np.empty((rows, cols), dtype=object)
		self.reference_memory = np.empty((rows, cols), dtype=object)
		(self.xpos, self.ypos) = self.get_floorplan("Building_Bot.txt")
		self.world = world

	def get_floorplan(self, fileName):
		#this function reads the floorplan from file Building.txt and puts it in the agent's memory
		fo = open(fileName, "r")
		#now read the entire file to a string

		raw = fo.read()
		fo.close()
		xidx = 0
		yidx = 0
		xpos = 0
		ypos = 0
		for letter in raw:
			if (letter != '\n'):
				self.working_memory[xidx][yidx] = letter
				yidx+=1
			elif letter == 'A':
				xpos = xidx
				ypos = yidx
			else:
				xidx+=1
				yidx = 0
		return (xpos, ypos)

	def display_map(self):
		for i in range (0, self.rows):
			for j in range (0, self.cols):
				print(self.working_memory[i][j], end='')
			print()

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