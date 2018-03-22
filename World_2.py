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
		#agent direction indicated by a single character and are relative to top of screen:
			#u= up(toward top of screen), d = down(bottom of screen), l = left of screen, r = right of screen
		self.agentdir = "u"

		self.agent = Bot_2(self.rows, self.cols, self)

		
	def get_agentx(self):
		return self.agentx

	def get_agenty(self):
		return self.agenty

	def set_agentx(self, xidx):
		self.agentx = xidx

	def set_agenty(self, yidx):
		self.agenty = yidx

	def get_agentdir(self):
		return self.agentdir

	def set_agentdir(self, dir):
		self.agentdir = dir

	def is_obstacle(self, x, y):
		#returns true iff there is an obstacle at (x, y)
		return (self.grid[x][y] == "#")

	def get_distance(start, end):
		#return distance between start and end
		#both arguments are ordered pairs
		return (abs(start[0] - end[0]) + abs(start[1] - end[1]))
	
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


	#cast 1 left, 1 right
	#stop when hit obstacle


	def cast_boundary_rays(self):
		#find start and end points for the left and right boundary rays
		#used to establish an absolute field of view, within which the bot can see
		#establish start points for right and left boundary rays
		(leftx, lefty) = (self.get_agentx, self.get_agenty)
		(rightx, righty) = (self.get_agentx, self.get_agenty)
		if self.get_agentdir == "u":
			#right ray found by starting at agent then moving upward with a slope of 1
			while (rightx >= 0) and (righty < self.cols):
				if grid[rightx][righty] == "#":
					break
				rightx -= 1
				righty += 1

			while (leftx >= 0) and (lefty >= 0):
				if grid[leftx][lefty] == "#":
					break
				leftx -= 1
				lefty -= 1

		elif self.get_agentdir = "d":
		#agent facing down, so get the proper endpoints
			while (rightx < self.rows) and (righty >= 0):
				if self.is_obstacle(rightx, righty):
					break
				rightx += 1
				righty -= 1

			while (leftx < self.rows) and (lefty < self.cols):
				if self.is_obstacle(leftx, lefty):
					break
				leftx += 1
				lefty += 1

		elif self.get_agentdir = "l":
		#agent facing left, so get the proper endpoints
			while (rightx >= 0) and (righty >= 0):
				if self.is_obstacle(rightx, righty):
					break
				rightx -= 1
				righty -= 1

			while (leftx < self.rows) and (lefty >= 0):
				if self.is_obstacle(leftx, lefty):
					break
				leftx += 1
				lefty -= 1

		elif self.get_agentdir = "r":
		#agent facing right, so get the proper endpoints
			while (rightx < self.rows) and (righty < self.cols):
				if self.is_obstacle(rightx, righty):
					break
				rightx += 1
				righty += 1

			while (leftx >= 0) and (lefty < self.rows):
				if self.is_obstacle(leftx, lefty):
					break
				leftx -= 1
				lefty += 1

		else:
			#in theory, this should never be reached, but it never hurts to be careful
			print('Invalid direction')

		return((leftx, lefty), (rightx, righty))

	def extend_ray(self, start, end):
		#used to trace helper arrays to their endpoints

		#calculate slope frome endpoints
		slope = ((end[1] - start[1])/(end[0] - start[0]))

		#now extend the line until either you reach an obstacle or go out of bounds
		nextx = end[0]
		nexty = end[1]
		while (nextx >= 0) and (nextx < self.cols) and (nexty >= 0) and (nexty < self.rows):
			#calculate next x, y
			nexty += slope
			nextx = start[0] + ((nexty - start[1])/slope)
			#make sure next point not obstacle

			#TODO: test this segment for out of bounds errors
			if self.is_obstacle(nextx, nexty):
				break

		return (nextx, nexty)

	def getting_farther(self, current, previous):
		#returns true iff current farther from agent than previous
		return (get_distance(current, (agentx, agenty)) > get_distance(previous, (agentx, agenty)))
		
		
	def sense(self):
		#a main/control method used to call all necessary subroutines
		#executing this method will provide the agent with a full set of sensor information in direction agent facing

		#first, we have to find the outer edges of the agent's field of view
		(leftEdge, rightEdge) = self.cast_boundary_rays()
		leftPath = list(bresenham(self.agentx, self.agenty, leftEdge[0], leftEdge[1]))
		rightPath = list(bresenham(self.agentx, self.agenty, rightEdge[0], rightEdge[1]))

		#now that the paths have been created, we must trace between cooresponding points on each line
		#since the FOV is bounded by two lines with a slope of 1, we can guarantee that there will
		#be exactly one point in the bounding line on either side of the FOV

		keepScanning = 1	#used in loop, set to 0 at start, only set to 1 if at least 1 non obstacle found
		pathIndex = 0		#used to access the elements in the paths, incremented in the loop
		while keepScanning == 1:
			keepScanning = 0
			#loop to manually stop when all characters on frontier are obstacles

			#pop x and y coords from left and right paths
			#if one of the paths is out of nodes, use the last one in the path
			#if both out of nodes, search is done from this angle
			if len(leftPath) > pathIndex:
				#have not reached end of left path
				left = leftPath.pop(pathIndex)
				
				#TODO: adjust the point to have correct x (or y) based on direction
					#if facing U, keep y, and subtract difference of len(leftpath) and pathIndex from x
			else:
				#path exhausted, so use last point in path as boundary
				left = leftPath.pop()
				#now ensure that right path still has nodes left
				if len(rightPath) <= pathIndex:
					#both paths exhausted, end scan
					break
					
			if len(rightPath) > pathIndex:
				#have not reached end of right path
				right = rightPath.pop(pathIndex)
			else:
				right = rightPath.pop()
			pathIndex += 1
			
			if self.get_agentdir == "u":
				#facing up, so all points in same row: all have same x, diff y
				#go from l to r
				for y in range(left[1], (right[1] + 1)):
					#add it if it's not an obstacle
					#if obstacle, need to check if at boundary
					if self.is_obstacle(left[0], y):
						#if at either edge, can ignore
						if (not y == left[1]) and (not y == right[1]):
							#the current cell is not at the edge of the FOV
							if not self.is_obstacle(left[0], (y + 1)):
								#the current cell marks the right corner of a wall
								if self.getting_farther((left[0],y), (left[0], (y - 1))):
									#current cell further than previous, so need helper ray
								
								#now log the presence of the obstacle, if it's visible
								
							elif not self.is_obstacle(left[0], (y - 1)):
								#current cell is next to left corner of a wall
								#if current is farther from agent than next block, generate a helper ray
						
					elif not self.is_obstructed(left[0], y):
						#found a visible non-obstacle, so must keep scanning
						keepScanning = 1


			elif (self.get_agentdir == "l") or (self.get_agentdir == "r"):

			else:
				#should REALLY never happen
				print("Invalid direction")






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