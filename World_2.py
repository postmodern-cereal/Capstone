import time
import numpy as np
from heapq import *
from math import *
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
		self.movesMade = 0
		self.rotationsMade = 0
		self.moveCost = 0.373
		self.rotationCost = 0.25
		#agent direction indicated by a single character and are relative to top of screen:
			#u= up(toward top of screen), d = down(bottom of screen), l = left of screen, r = right of screen
		self.agentdir = "u"

		self.agent = Bot_2(self.rows, self.cols, self.grid)


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

	def rotate(self):
		#rotates agent clockwise. this is arbitrary and doesn't effect anything in a major way
		if self.agentdir == "u":
			self.set_agentdir("r")

		elif self.agentdir == "r":
			self.set_agentdir("d")

		elif self.agentdir == "d":
			self.set_agentdir("l")

		else:
			self.set_agentdir("u")

		self.rotationsMade += 1

	def set_agentdir(self, dir):
		self.agentdir = dir

	def is_obstacle(self, node):
		#returns true iff there is an obstacle at (x, y)
		x = node[0]
		y = node[1]
		return (self.grid[x][y] == "#")

	def get_distance(self, start, end):
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

	def is_obstructed(self, node):
        #node is the spot yok2u are trying to see
        #step 1: make a straight line from agent to node
        #this is done using bresenham's straight line approximation algorithm
        #if any of the coordinates returned contain an obstacle, we return false. If not, we return true
		path = list(bresenham(self.agentx, self.agenty, node[0], node[1]))
		for cell in path:
			if self.is_obstacle((cell[0], cell[1])):
				if (cell[0], cell[1]) == (node[0], node[1]):
					#we need this condition in case we are looking at an obstacle currently
					return False
				else:
					return True

		return False

	def cast_boundary_rays(self):
		#find start and end points for the left and right boundary rays
		#used to establish an absolute field of view, within which the bot can see
		#establish start points for right and left boundary rays
		(leftx, lefty) = (self.get_agentx(), self.get_agenty())
		(rightx, righty) = (self.get_agentx(), self.get_agenty())
		if self.get_agentdir() == "u":
			#in this orientation, left ray is left of screen, right ray is right of screen
			#right ray found by starting at agent then moving upward with a slope of 1
			while (rightx >= 0) and (righty < self.cols):
				if self.is_obstacle((rightx, righty)):
					break

				else:
					rightx -= 1
					righty += 1

			while (leftx >= 0) and (lefty >= 0):
				if self.grid[leftx][lefty] == "#":
					break

				else:
					leftx -= 1
					lefty -= 1

		elif self.get_agentdir() == "d":
			#agent facing down, so get the proper endpoints
			#right ray to left of screen
			#left ray to right of screen
			#note that right is agent's right (left of screen) in this orientation
			while (rightx < self.rows) and (righty >= 0):
				if self.is_obstacle((rightx, righty)) :
					break
				else:
					rightx += 1
					righty -= 1

			while (leftx < self.rows) and (lefty < self.cols):
				if self.is_obstacle((leftx, lefty)):
					break
				else:
					leftx += 1
					lefty += 1

		elif self.get_agentdir() == "l":
			#agent facing left of screen
			#left ray is closest to bottom of screen
			#right ray closest to top of screen
			while (rightx >= 0) and (righty >= 0):
				if self.is_obstacle((rightx, righty)):
					break
				else:
					rightx -= 1
					righty -= 1

			while (leftx < self.rows) and (lefty >= 0):
				if self.is_obstacle((leftx, lefty)):
					break
				else:
					leftx += 1
					lefty -= 1

		elif self.get_agentdir() == "r":
			#agent facing right of screen
			#right ray closest to bottom of screen
			#left ray closest to top of screen
			while (rightx < self.rows) and (righty < self.cols):
				if self.is_obstacle((rightx, righty)):
					break
				else:
					rightx += 1
					righty += 1

			while (leftx >= 0) and (lefty < self.rows):
				if self.is_obstacle((leftx, lefty)):
					break
				else:
					leftx -= 1
					lefty += 1

		else:
			#in theory, this should never be reached, but it never hurts to be careful
			print('Invalid direction')

		return[(leftx, lefty), (rightx, righty)]

	def adjust_coords(self, node, pathLength, pathIndex):
		#This method is used to resolve situations in which one side of the field of view is longer than the other.
		#Depending on the side of the viewfield it's on and the orientation of the agent, either the x or the y coordinate is adjusted to remain horizontally(or vertically) in line with the other side
		#node: ordered pair, to be adjusted
		#path length: length of the path the node belongs to
		#path index: how many nodes we are away from the agent
		x = node[0]
		y = node[1]
		#have to subtract 1 from path length so it works when path same as path index: even in this case, we still need to add a node
		offset = pathIndex - (pathLength-1)         #how much to add/subtract to/from the cordinate

		if self.get_agentdir() == 'u':
			#need to subtract from x coordinate
			x -= offset
			return (x, y)

		elif self.get_agentdir() == 'd':
			#need to add to x coordinate
			x += offset
			return (x, y)

		elif self.get_agentdir() == 'l':
			#need to subtract from y coordinate
			y -= offset
			return (x, y)

		elif self.get_agentdir() == 'r':
			#need to add to y coodinate
			y += offset
			return (x, y)

	def extend_ray(self, start, end):

		#used to trace helper arrays to their endpoints
		#calculate slope from endpoints

		slope = ((end[1] - start[1])/(end[0] - start[0]))
		path = [(end[0], end[1])]
		nextx = end[0]
		nexty = end[1]
		while (nextx >= 0) and (nextx < self.cols) and (nexty >= 0) and (nexty < self.rows):
			#calculate next x, y
			nextx += 1
			nexty = nextx + slope
			nexty = int(round(nexty, 0))

			#ensure (nextx, nexty) in bounds
			if (nextx < 0) or (nextx >= self.rows) or (nexty < 0) or (nexty >= self.cols):
				#(nextx, nexty) out of bounds, should not be added to path
				#probably redundant, but better to be safe than sorry
				break

			#add them to the path, even if they are obstacles
			path.append((nextx, nexty))

			#determine whether to stop extending ray
			node = (nextx, nexty)

			if self.grid[int(nextx)][int(nexty)] == "#":
				break


		return path


	def boundary_in_corner(self, node, side):
		#node: current node in path
		#side: "l" or "r"
		#return true iff node in corner

		if node[0] == 0 or node[1] == 0 or node[1] == self.cols-1 or node[1] == self.rows-1:
			if (node[0] == 0 and node[1] == 0) or (node[0] == self.rows-1 and node[1] == self.cols-1):
				return True
			else:
				return False

		#can lump some cases together due to symetry
		if (self.get_agentdir() == "r" and side == "l") or (self.get_agentdir() == "u" and side == "r"):
			#left ray, facing right, or right ray, facing up
			#top right corner
			if node[0] == 0:
				if node[1] >= self.cols:
					return True
				return False
			if self.is_obstacle((node[0], node[1] + 1)) and self.is_obstacle((node[0] - 1, node[1])) and self.is_obstacle((node[0] - 1, node[1] + 1)):
				return True

			else:
				return False

		elif (self.get_agentdir() == "r" and side == "r") or (self.get_agentdir() == "d" and side == "l"):
			#right ray facing right or left ray facing down
			#bottom right corner
			if node[0] == self.rows:
				if node[1] >= self.cols:
					return True
				return False
			if self.is_obstacle((node[0], node[1] + 1)) and self.is_obstructed((node[0] + 1, node[1] + 1)) and self.is_obstructed((node[0] + 1, node[1])):
				return True

			else:
				return False

		elif (self.get_agentdir() == "l" and side == "l") or (self.get_agentdir() == "d" and side == "r"):
			#left ray facing left or right ray facing down
			#bottom left corner
			if node[0] == self.rows:
				if node[1] <= 0:
					return True
				return False
			if self.is_obstacle((node[0], node[1] - 1)) and self.is_obstructed((node[0] + 1, node[1])) and self.is_obstructed((node[0] + 1, node[1] - 1)):
				return True

			else:
				return False

		elif (self.get_agentdir() == "l" and side == "r") or (self.get_agentdir() == "u" and side == "l"):
			#right ray facing left or left ray facing up
			#top right corner
			if node[0] == 0:
				if node[1] <= 0:
					return True
				return False
			if self.is_obstacle((node[0], node[1] - 1)) and self.is_obstructed((node[0] - 1, node[1] - 1)) and self.is_obstructed((node[0] - 1, node[1])):
				return True

			else:
				return False

		else:
			print("Error")
			return False

	def helper_ray(self, corner):
		#corner is ordered pair coordinates of corner through which ray passes
		return self.extend_ray((self.agentx, self.agenty), corner)

	def farther_from_agent(self, current, previous):
		#returns true iff current farther from agent than previous
		#used to check for visual obstruction: if current closer or same distance to agent, no obstruction occurs
		foo = self.get_agentx()
		bar = self.get_agenty()
		bas = (foo, bar)
		return (self.get_distance(current, bas)) > (self.get_distance(previous, bas))

	def needs_ray(self, current, previous):
		return False	#turns out i don't need this
		#it is assumed that this will not be called on the first cell in a row
		#takes current and previous spaces and determines if a helper ray is needed
		#returns False if no action needed
		#returns True if need helper ray
		# if self.is_obstacle(current):
		# 	if self.is_obstacle(previous):
		# 		return False
		# 	else:
		# 		#if current same distance to agent or closer, no obstruction occurs
		# 		if self.farther_from_agent(current, previous):
		# 			#blockage happens
		# 			return True
		# 		else:
		# 			#no blockage
		# 			return False
		#
		# elif not self.is_obstacle(current):
		# 	if not self.is_obstacle(previous):
		# 		return False
		# 	else:
		# 		if self.farther_from_agent(current, previous):
		# 			return True
		# 		else:
		# 			return False

	def package_data(self, cell):
	    #takes an ordered pair and pakcages it for addition to sensor data list
	    #will return a list of form ((x, y), fill), where fill is the fill char
	    return [(cell[0], cell[1]), self.grid[cell[0]][cell[1]]]

	def sense_init(self):
		#a main/control method used to call all necessary subroutines
		#executing this method will provide the agent with a full set of sensor information in direction agent facing

		#first, we have to find the outer edges of the agent's field of view
		(leftEdge, rightEdge) = self.cast_boundary_rays()
		#print("Left Edge: ", leftEdge)
		leftPath = list(bresenham(self.get_agentx(), self.get_agenty(), leftEdge[0], leftEdge[1]))
		rightPath = list(bresenham(self.get_agentx(), self.get_agenty(), rightEdge[0], rightEdge[1]))

		print("Boundary Rays: ")
		for i in range (0, self.rows):
			for j in range(0, self.cols):
				if (i,j) in leftPath or (i, j) in rightPath:
					print(".", end='')
				else:
					print(self.grid[i][j], end='')
			print()

		#print("Initial left path ", leftPath)

		#now that the paths have been created, we must trace between cooresponding points on each line
		#since the FOV is bounded by two lines with a slope of 1, we can guarantee that there will
		#be exactly one point in the bounding line on either side of the FOV
		return self.sense(leftPath, rightPath)

	def sense(self, leftPath, rightPath):
		#the recursive method
		#leftPath is path farthest to agent left
		#rightPath is path farthest to agent right

		pathIndex = 0		#used to access the elements in the paths, incremented in the loop
		left = (self.get_agentx(), self.get_agenty)
		right = (self.get_agentx(), self.get_agenty)
		sensorData = []
		while True:
			#the loop will end under two circumstances:
			#	1. Both the left and right paths are in a corner
			#	2. All of the characters seen on the current lefel have been obstacles
			#	To clarify, if the left is at (5, 5) and the right is at (5, 10), and every character between those two points is a wall, the sweep is over




			#pop x and y coords from left and right paths
			#if one of the paths is out of nodes, use the last one in the path
			#if both out of nodes, search is done from this angle
			if len(leftPath) > pathIndex:
				#print("Normal")
				#have not reached end of left path
				left = leftPath[pathIndex]

			else:
				if self.boundary_in_corner(leftPath[-1], "l"):
					#print("Corner")
					#can keep scanning iff right not in corner

					if len(rightPath) > pathIndex:
						#in this case, the right path still has nodes left in it
						#this means that we can recalibrate the left bound so that we can continue to scan the visible area, but without scanning spaces that should not be scannable
						#first, move left path down to current row with adjust_coords
						left = self.adjust_coords(leftPath[-1], len(leftPath), pathIndex)
						#print("Adjusted left: ", left)
						#now check if left now inside a wall. If so, iterate forward until it's not
						if self.is_obstacle(left):
							#left bound is inside a wall. Move it to right until clear.
							#find next right & use as tmp boundary
							tmp = rightPath[pathIndex]

							#make path from left to right
							pathToRight = list(bresenham(left[0], left[1], tmp[0], tmp[1]))

							#iterate along path until hit clear space
							for point in pathToRight:
								if self.is_obstacle(point):
									#print(point)
									if not self.is_obstructed(point):
										sensorData.append(self.package_data(point))
								elif not self.is_obstacle(point):
									left = point
									break
						leftPath.append(left)

					#note: rightPath[-1] gets last element of rightPath
					elif not self.boundary_in_corner(rightPath[-1], "r"):
						#need to fix both paths, but can still scan
						#will do the work of fixing right path, but stores correct value temporarily, allowing it to be fixed by the specific code dealing with the right side

						#move left, right to current row
						left = self.adjust_coords(left, len(leftPath), pathIndex)
						#print("Adjusted left: ", left)
						#print("Last part of right path: ", rightPath[-1])

						#tmp is temp right bound
						tmp = self.adjust_coords(rightPath[-1], len(rightPath), pathIndex)

						if self.is_obstacle(left):
							pathToRight = list(bresenham(left[0], left[1], tmp[0], tmp[1]))

							for point in pathToRight:
								if self.is_obstacle(point) and not self.is_obstructed(point):
									sensorData.append(self.package_data(point))

								elif not self.is_obstacle(point):
									left = point
									break

						leftPath.append(left)
						#if self.is_obstacle(tmp):
						#	pathToLeft = list(bresenham(right[0], right[1], left[0], left[1]))
						#
						#	for point in pathToLeft:
						#		if not self.is_obstacle(point):
						#			right = point
						#			break

					else:
						#both paths in a corner: stop
						break

				else:
					#extend left path: no corner reached
					#print("Lefts ", leftPath)
					left = self.adjust_coords(leftPath[-1], len(leftPath), pathIndex)
					#print("Adjusted left ", left)
					#
					# if self.is_obstacle(left):
					# 	#move l bound out of wall
					# 	if len(rightPath) > pathIndex:
					#
					# 		tmp = rightPath[pathIndex]
					# 		print("Right: ", tmp, "Left: ", left)
					# 		pathToRight = list(bresenham(left[0], left[1], tmp[0], tmp[1]))
					#
					# 		for point in pathToRight:
					# 			if self.is_obstacle(point) and not self.is_obstructed(point):
					# 				sensorData.append(self.package_data(point))
					#
					# 			elif not self.is_obstacle(point):
					# 				left = point
					# 				break
					# 	else:
					# 		#need to temporarily adjust r path in order to fix l
					# 		#will not matter if right in corner, because you can
					# 		#still move in the correct direction
					# 		tmp = self.adjust_coords(rightPath[-1], len(rightPath), pathIndex)
					#
					# 		pathToRight = list(bresenham(left[0], left[1], tmp[0], tmp[1]))
					# 		for point in pathToRight:
					# 			if self.is_obstacle(point) and not self.is_obstructed(point):
					# 				sensorData.append(self.package_data(point))
					#
					# 			elif not self.is_obstacle(point):
					# 				left = point
					# 				break

					leftPath.append(left)

			if len(rightPath) > pathIndex:
				#have not reached end of right path
				right = rightPath[pathIndex]

			else:
				#if statement not needed: you do the same things whether it's
				#in a corner or not
				#need to fix right bound
				right = self.adjust_coords(rightPath[-1], len(rightPath), pathIndex)
				# if self.is_obstacle(right):
				# 	#moves to L because L already fixed
				# 	pathToLeft = list(bresenham(right[0], right[1], left[0], left[1]))
				# 	for point in pathToLeft:
				# 		if self.is_obstacle(point) and not self.is_obstructed(point):
				# 			sensorData.append(self.package_data(point))
				# 		elif not self.is_obstacle(point):
				# 			right = point
				# 			break
				rightPath.append(right)

			swatchLength = 1+self.get_distance(left, right)	#stores the number of characters between right and left sides
			#must add 1 to distance because will always come up one short
			#the distance formula always comes up with mathematically correct answers when tested, so this is likely due to it somehow not accounting for the length of a character somewhere
			#print("Swatch length: ", swatchLength)
			numObstaclesInSwatch = 0	#stores how many obstacles have been hit in the current swatch
			#will also be incremented if a given cell is obstructed
			#this way, if it somehow goes beyond the confines of a room, it will still stop before hitting the far edge of the map

			#increment loop variable now, because it won't be needed for rest
			#of loop
			pathIndex += 1

			if self.get_agentdir() == "u":
				#facing up, so all points in same row: all have same x, diff y

				for y in range(left[1], (right[1] + 1)):
					current = (left[0], y)          #current node
					#check for a corner, unless we're on the left edge
					if y == left[1]:
						#we're on starting edge, no corner check
						#add current to sensor data, then skip rest of loop
						if self.is_obstacle(current) or self.is_obstructed(current):
							#add an obstacle
							numObstaclesInSwatch += 1

						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))
							continue

					previous = (left[0], (y-1))     #previous node
					if self.needs_ray(current, previous):
						#generate the helper ray, then recurse, using the left path from the current node to the end as left bound, and helper ray as right bound
						sensorData.extend(self.sense(leftPath[pathIndex:], self.helper_ray(current)))

						#set the left path as a vertical line starting here:
						#everything left of current already sensed
						#everything that may come after current in list should be thrown away, as it was scanned in the line above

						leftPath = leftPath[0:(pathIndex+1)]
						leftPath.append(current)

					else:
						#Add cell to memory, but make sure is visible first
						#This will avoid adding spaces between walls, out of bounds, or otherwise only visible by cheating
						if self.is_obstacle(current) or self.is_obstructed(current):
							#add an obstacle to the count
							numObstaclesInSwatch += 1

						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))

			elif self.get_agentdir() == "d":
                #facing down, so all points in same row: same x, diff y
                #must move from right ray to left ray
				for y in range(right[1], left[1] + 1):
					current = (right[0], y)

					if y == right[1]:
						if self.is_obstacle(current) or self.is_obstructed(current):
							#add an obstacle to the count
							numObstaclesInSwatch += 1

						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))
						continue

					previous = (right[0], y - 1)
					#print("Current: ", current, "Previous: ", previous)
					if self.needs_ray(current, previous):
						#paths have to be passed somewhat counterintuitively
						#since the helper ray is on the agent's left, it gets passed first
						helper = self.helper_ray(current)
						print("Generating a helper ray")
						for i in range (0, self.rows):
							for j in range (0, self.cols):
								if (i, j) in helper:
									print(".", end='')
								elif (i,j) in sensorData:
									print("_",end='')
								else:
									print(self.grid[i][j], end='')
							print()
						sensorData.extend(self.sense(self.helper_ray(current), rightPath[pathIndex:]))

						#set right path to end at current node
						rightPath = rightPath[0:pathIndex+1]
						rightPath.append(current)
						#will be adjusted/extended at start of next iteration as needed

					else:
						if self.is_obstacle(current) or self.is_obstructed(current):
							#add an obstacle to the count
							numObstaclesInSwatch += 1

						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))

			elif self.get_agentdir() == "r":
				#facing right, so all points in same col: same y, diff x
				#must move from l ray to r ray
				for x in range(left[0], right[0]+1):
					current = (x, left[1])


					if x == left[0]:
						if self.is_obstacle(current) or self.is_obstructed(current):
							#add an obstacle to the count
							numObstaclesInSwatch += 1

						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))
						continue

					previous = (x-1, left[1])

					if self.needs_ray(current, previous):
						if current[0] == right[0]:
							continue
						print("Left Path: ", leftPath)
						sensorData.extend(self.sense(leftPath[pathIndex:], self.helper_ray(current)))

						#adjust left path
						leftPath = leftPath[0:pathIndex+1]
						leftPath.append(current)

					else:
						if self.is_obstacle(current) or self.is_obstructed(current):
							#add an obstacle to the count
							numObstaclesInSwatch += 1

						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))

			elif self.get_agentdir() == "l":
				#facing left, all points same y, diff x
				#move from right ray to left ray
				for x in range(right[0], left[0]+1):
					current = (x, right[1])

					if x == right[0]:
						if self.is_obstacle(current) or self.is_obstructed(current):
							#add an obstacle to the count
							numObstaclesInSwatch += 1

						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))
						continue

					previous = (x-1, right[1])

					if self.needs_ray(current, previous):
						#again, pass helper ray first because it's always closer to agent left
						sensorData.extend(self.sense(self.helper_ray(current), rightPath[pathIndex:]))

						#adjust right path
						rightPath = rightPath[0:pathIndex+1]
						rightPath.append(current)

					else:
						if self.is_obstacle(current) or self.is_obstructed(current):
							#add an obstacle to the count
							numObstaclesInSwatch += 1

						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))

			else:
				#should REALLY never happen
				print("Invalid direction")

			#before proceeding with next run of loop, make sure that the paths are not going to fall on the maxima of the array
			#that is, the corners of the array itself
			if swatchLength == numObstaclesInSwatch:
				#every character was an obstacle. nothing at deeper levels wil be visible to the agent, so stop the sweep
				break


		return sensorData

	def move_valid(self, current, destination):
		#returns true iff move from current to destination legal
		#move legal iff:
			#distance from current to destination is 1
            #move does not end in obstacle or outside map
		if self.get_distance(current, destination) <= 1 and not self.is_obstacle(destination) and not self.grid[destination[0]][destination[1]] == "+":
			self.movesMade += 1
			return True
		else:
			return False

	def verify_sweep(self):
		#check that agent has actually finsihed a sweep:
		#data for bot versions of agent mem should be same
		#note that void spaces (those that cannot be reached by the agent) will appear as "+"
		self.agent.display_ref_memory()
		for x in range (0, self.rows):
			for y in range (0, self.cols):
				if not (self.agent.working_memory[x][y] == self.agent.reference_memory[x][y]):
					if self.agent.working_memory[x][y] == "_" and self.agent.reference_memory[x][y] == " ":
						return True
					#found a spot where agent has not swept
					return False

		return True

	def simulate(self, numSweeps):
		#basic main loop method that runs the simulations
		#numSweeps is how many total sweeps of building agent should make
		print("World Map:")
		self.display_world()
		while numSweeps > 0:
			print()
			print()
			print("Agent current working memory:")
			self.agent.display_memory()
			print("Agent direction: ", self.get_agentdir())
			nextAction = self.agent.get_next_action()
			print("Next action: ", nextAction)
			print()
			if nextAction == "s":
			    #sense in all 4 directions
				for i in range (0, 4):
					print("Sensing in direction ", self.get_agentdir())
					self.agent.add_data(self.sense_init())
					self.rotate()
					print()
					print("Agent working memory after sensor sweep:")
					self.agent.display_memory()
					print()
					self.agent.next_action = "c"


			elif nextAction == "n":
				#verify complete
				print("Verifying sweep complete...")
				if self.verify_sweep() == True:
					print("Verification successful, resetting agent")
					print(self.movesMade, " moves and ", self.rotationsMade, " rotations made.")
					print("Total cost of moves: ", self.movesMade*self.moveCost, " seconds.")
					print("Total cost of rotations: ", self.rotationsMade*self.rotationCost, " seconds.")
					print("Grand total time cost: ",self.rotationsMade*self.rotationCost + self.movesMade*self.moveCost, " seconds." )
					self.agent.reset()
					numSweeps -= 1

				else:
				    #the agent messed up. have it check again
					print("Verification failed. Forcing agent re-check...")
					self.agent.next_action = "c"
				    #agent will run check on next loop through

			elif nextAction == "m":
				#get next move

				nextMove = self.agent.currentPath.pop(0)
				print("Attempting a move from ", (self.agentx, self.agenty), "to ", nextMove)
				#check next move valid
				if self.move_valid((self.agentx, self.agenty), nextMove):
					print("Move from ", (self.agentx, self.agenty), "to ", nextMove, "successful.")
					self.grid[self.agentx][self.agenty] = " "
					self.set_agentx(nextMove[0])
					self.set_agenty(nextMove[1])
					self.grid[self.agentx][self.agenty] = "A"
					self.agent.set_position(nextMove)
				else:
				    #move invalid: tell agent to sense
					print("Move from ", (self.agentx, self.agenty), "to ", nextMove, "failed. Informing agent...")
					self.agent.currentPath = []
					self.agent.next_action = "s"
				    #agent will gain sensor data on next loop and try again
			time.sleep(.2)

#need to test world functionality
