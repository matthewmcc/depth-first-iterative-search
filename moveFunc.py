# returns the str representation of an integer of coordinates
def intToStr(i):
	return str(unichr(i + 97))

# Sets deltaList
def setDeltaList(dL):
	global deltaList
	deltaList = dL

# returns a list of tiles of the given maxPlayer to move
def tileList(state, player):
	tList = []
	tup = ()
	i, j = 0, 0
	while i < 8:
		while j < 8:
			if state[i][j] == player:
				tup = (i, j)
				tList.append(tup)
			j += 1
		j = 0	
		i += 1
	return tList

# Adds the deltas to the given coordinates
def addDelta(xy, dX, dY):
	xy[0] = xy[0] + dX
	xy[1] = xy[1] + dY
	
# 	
def tupToList(xy, dX, dY):
	xyL = [] * 2
	xyL = [xy[0] + dX, xy[1] + dY]
	return xyL

# Checks if a given coordinate is in range of the board
def inRange(xy):
	if xy[0] > -1 and xy[0] < 8 and xy[1] > -1 and xy[1] < 8:
		return True
	return False

# Makes any extra flanking moves given by orginal move
def flank(node, dX, dY, xy, movePlayer, otherPlayer):
	xyL = tupToList(xy, dX, dY)
	node.state[xyL[0]][xyL[1]] = movePlayer
	
	while 1:
		addDelta(xyL, dX, dY)
		if node.state[xyL[0]][xyL[1]] == movePlayer:
			return 
		elif node.state[xyL[0]][xyL[1]] == otherPlayer:
			node.state[xyL[0]][xyL[1]] = movePlayer

# Checks any extra flankning moves are possible
def canFlank(node, dX, dY, xy, movePlayer, otherPlayer):
	xyL = tupToList(xy, dX, dY)
	
	if inRange(xyL) and node.state[xyL[0]][xyL[1]] == otherPlayer:
		while 1:
			addDelta(xyL, dX, dY)
			if (not inRange(xyL)):
				return False
			elif node.state[xyL[0]][xyL[1]] == movePlayer:
				return True
			elif node.state[xyL[0]][xyL[1]] == otherPlayer:
				continue
			else: return False
	return False

# Moves the direct line in move and tests for extra 
def makeMove(node, dX, dY, xy, movePlayer, otherPlayer):
	xyL = tupToList(xy, dX, dY)
	node.state[xyL[0]][xyL[1]] = movePlayer

	while 1:
		addDelta(xyL, dX, dY)
		if node.state[xyL[0]][xyL[1]] != otherPlayer and node.state[xyL[0]][xyL[1]] != movePlayer:
			node.state[xyL[0]][xyL[1]] = movePlayer

			# Adds the move coordinates to the node
			move = (intToStr(xyL[1]), xyL[0] + 1)
			node.setMove(move)
			for i in deltaList:
				if not(dX == i[0] and dY == i[1]) and canFlank(node, i[0], i[1], xyL, movePlayer, otherPlayer):

					flank(node, i[0], i[1], xyL, movePlayer, otherPlayer)

			return

		elif node.state[xyL[0]][xyL[1]] == otherPlayer:
			node.state[xyL[0]][xyL[1]] = movePlayer

# Returns the tile gain given a move direction
def canMove(node, dX, dY, xy, movePlayer, otherPlayer):
	xyL = tupToList(xy, dX, dY)

	if inRange(xyL) and node.state[xyL[0]][xyL[1]] == otherPlayer:
		while 1:
			addDelta(xyL, dX, dY)
			if (not inRange(xyL)):
				return False
			elif node.state[xyL[0]][xyL[1]] != otherPlayer and node.state[xyL[0]][xyL[1]] != movePlayer:
				return True
			elif node.state[xyL[0]][xyL[1]] == otherPlayer:
				continue
			else: return False
	return False

# Test to see if a game state is game over
def terminalTest(node, movePlayer, otherPlayer):
	tList = []
	tList = tileList(node.state, movePlayer)
	if len(tList) == 0:
		return True
	for xy in tList:
		for delta in deltaList:
			if canMove(node, delta[0], delta[1], xy, movePlayer, otherPlayer):
				return False

	tList = tileList(node.state, otherPlayer)
	if len(tList) == 0:
		return True
	for xy in tList:
		for delta in deltaList:
			if canMove(node, delta[0], delta[1], xy, otherPlayer, movePlayer):
				return False
	return True

# Returns a value given by the difference between maxPlayer and minPlayer tiles
def utilFunc(node, maxPlayer, minPlayer):
	maxList = tileList(node.state, maxPlayer)
	minList = tileList(node.state, minPlayer)
	util = len(maxList) - len(minList)

	# Checks if the given state is a complete game and which player won
	if terminalTest(node, maxPlayer, minPlayer):
		if util > 0:
			util += 100
		else:
			util -= 100
	return util

# Checks if the player can move and returns True if yes else False
def anyMove(node, movePlayer, otherPlayer):
	tList = tileList(node.state, movePlayer)

	for m in tList:
		for d in deltaList:
			if canMove(node, d[0], d[1], m, movePlayer, otherPlayer):
				return True
	return False
