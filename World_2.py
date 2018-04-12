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

	def set_agentdir(self, dir):
		self.agentdir = dir

	def is_obstacle(self, node):
		#returns true iff there is an obstacle at (x, y)
		return (self.grid[node[0]][node[1]] == "#")

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
        #node is the spot you are trying to see
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
				if grid[leftx][lefty] == "#":
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
			nexty += slope
			nextx = start[0] + ((nexty - start[1])/slope)

			#ensure (nextx, nexty) in bounds
			if (nextx < 0) or (nextx >= self.rows) or (nexty < 0) or (nexty >= self.cols):
				#(nextx, nexty) out of bounds, should not be added to path
				#probably redundant, but better to be safe than sorry
				break

			#add them to the path, even if they are obstacles
			path.append((nextx, nexty))

			#determine whether to stop extending ray
			if self.is_obstacle(nextx, nexty):
				break

		return path

	def boundary_in_corner(self, node, side):
		#node: current node in path
		#side: "l" or "r"
		#return true iff node in corner

		#can lump some cases together due to symetry
		if (self.get_agentdir() == "r" and side == "l") or (self.get_agentdir() == "u" and side == "r"):

			if self.is_obstacle((node[0], node[1] + 1)) and self.is_obstacle((node[0] - 1, node[1])) and self.is_obstacle((node[0] - 1, node[1] + 1)):
				return True

			else:
				return False

		elif (self.get_agentdir() == "r" and side == "r") or (self.get_agentdir() == "d" and side == "l"):

			if self.is_obstacle((node[0], node[1] + 1)) and self.is_obstructed((node[0] + 1, node[1] + 1)) and self.is_obstructed((node[0] + 1, node[1])):
				return True

			else:
				return False

		elif (self.get_agentdir() == "l" and side == "l") or (self.get_agentdir() == "d" and side == "r"):

			if self.is_obstacle((node[0], node[1] - 1)) and self.is_obstructed((node[0] + 1, node[1])) and self.is_obstructed((node[0] + 1, node[1] - 1)):
				return True

			else:
				return False

		elif (self.get_agentdir() == "l" and side == "r") or (self.get_agentdir() == "u" and side == "l"):

			if self.is_obstacle((node[0], node[1] - 1)) and self.is_obstructed((node[0] - 1, node[1] - 1)) and self.is_obstructed((node[0] - 1, node[1])):
				return True

			else:
				return False

		else:
			print("Error")
			return False

	def helper_ray(self, corner):
		#corner is ordered pair coordinates of corner through which ray passes
		return self.extend_ray((agentx, agenty), corner)

	def farther_from_agent(self, current, previous):
		#returns true iff current farther from agent than previous
		#used to check for visual obstruction: if current closer or same distance to agent, no obstruction occurs
		foo = self.get_agentx()
		bar = self.get_agenty()
		bas = (foo, bar)
		return (self.get_distance(current, bas)) > (self.get_distance(previous, bas))

	def needs_ray(self, current, previous):
		#it is assumed that this will not be called on the first cell in a row
		#takes current and previous spaces and determines if a helper ray is needed
		#returns False if no action needed
		#returns True if need helper ray
		if self.is_obstacle(current):
			if self.is_obstacle(previous):
				return False
			else:
				#if current same distance to agent or closer, no obstruction occurs
				if self.farther_from_agent(current, previous):
					#blockage happens
					return True
				else:
					#no blockage
					return False

		elif not self.is_obstacle(current):
			if not self.is_obstacle(previous):
				return False
			else:
				if self.farther_from_agent(current, previous):
					return True
				else:
					return False

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
			#print()
			#print("Current left path ", leftPath)
			#print("Index: ", pathIndex)
			#print("Length of left path:", len(leftPath))
			#loop to manually stop when all characters on frontier are obstacles


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
						#print("Right good")
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

					if self.is_obstacle(left):
						#move l bound out of wall
						if len(rightPath) > pathIndex:
							tmp = rightPath[pathIndex]

							pathToRight = list(bresenham(left[0], left[1], tmp[0], tmp[1]))

							for point in pathToRight:
								if self.is_obstacle(point) and not self.is_obstructed(point):
									sensorData.append(self.package_data(point))

								elif not self.is_obstacle(point):
									left = point
									break
						else:
							#need to temporarily adjust r path in order to fix l
							#will not matter if right in corner, because you can
							#still move in the correct direction
							tmp = self.adjust_coords(rightPath[-1], len(rightPath), pathIndex)

							pathToRight = list(bresenham(left[0], left[1], tmp[0], tmp[1]))
							for point in pathToRight:
								if self.is_obstacle(point) and not self.is_obstructed(point):
									sensorData.append(self.package_data(point))

								elif not self.is_obstacle(point):
									left = point
									break

					leftPath.append(left)

			if len(rightPath) > pathIndex:
				#have not reached end of right path
				right = rightPath[pathIndex]

			else:
				#if self.boundary_in_corner(right, "r"):
				#if statement not needed: you do the same things whether it's
				#in a corner or not
				#need to fix right bound
				right = self.adjust_coords(rightPath[-1], len(rightPath), pathIndex)
				if self.is_obstacle(right):
					#moves to L because L already fixed
					pathToLeft = list(bresenham(right[0], right[1], left[0], left[1]))
					for point in pathToLeft:
						if self.is_obstacle(point) and not self.is_obstructed(point):
							sensorData.append(self.package_data(point))
						elif not self.is_obstacle(point):
							right = point
							break
				rightPath.append(right)

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
						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))

			elif self.get_agentdir() == "d":
                #facing down, so all points in same row: same x, diff y
                #must move from right ray to left ray
				for y in range(right[1], left[1] + 1):
					current = (right[0], y)

					if y == right[1]:
						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))
						continue

					previous = (right[0], y - 1)

					if self.needs_ray(current, previous):
						#paths have to be passed somewhat counterintuitively
						#since the helper ray is on the agent's left, it gets passed first
						sensorData.extend(self.sense(self.helper_ray(current), rightPath[pathIndex:]))

						#set right path to end at current node
						rightPath = rightPath[0:pathIndex+1]
						rightPath.append(current)
						#will be adjusted/extended at start of next iteration as needed

					else:
						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))

			elif self.get_agentdir() == "r":
				#facing right, so all points in same col: same y, diff x
				#must move from l ray to r ray
				for x in range(left[0], right[0]+1):
					current = (x, left[1])

					if x == left[0]:
						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))
						continue

					previous = (x-1, left[1])

					if self.needs_ray(current, previous):
						sensorData.extend(self.sense(leftPath[pathIndex:], self.helper_ray(current)))

						#adjust left path
						leftPath = leftPath[0:pathIndex+1]
						leftPath.append(current)

					else:
						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))

			elif self.get_agentdir() == "l":
				#facing left, all points same y, diff x
				#move from right ray to left ray
				for x in range(right[0], left[0]+1):
					current = (x, right[1])

					if x == right[0]:
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
						if not self.is_obstructed(current):
							sensorData.append(self.package_data(current))

			else:
				#should REALLY never happen
				print("Invalid direction")

		return sensorData




#need to test world functionality






world = World_2(11, 22)
print("Agent location:", world.agentx, ", ", world.agenty)
print("Actual world")
world.display_world()
world.set_agentdir("d")
agentMap = world.grid
visible = world.sense_init()

for item in visible:
	item = item.pop()

print("Tiles visible to agent:")
for i in range (0, world.rows):
	for j in range (0, world.cols):
		if [(i, j)] in visible:
			print("-", end="")
		else:
			print(agentMap[i][j], end="")
	print()
#print(agentMap)
