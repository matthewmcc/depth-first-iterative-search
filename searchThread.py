import copy
import threading

from tree import *
from gameVar import *
from moveFunc import *

# Thread for computing the next move under a given time constraint
class SearchThread(threading.Thread):
	def __init__(self, node, timeOut, maxPlayer, minPlayer, gameVar):
		threading.Thread.__init__(self)
		self.node = node
		self.timeOut = timeOut
		self.minPlayer = minPlayer
		self.maxPlayer = maxPlayer
		self.gameVar = gameVar

	# Begins thread execution
	def run(self):

		# Check if given board is already in terminal state
		if terminalTest(self.node, self.maxPlayer, self.minPlayer):
			self.timeOut = False
			print "No possible moves for both players. GAME OVER"
			return

		# Checks if player can move on the given board
		if not anyMove(self.node, self.maxPlayer, self.minPlayer):
			print "move a -1 nodes 0 depth 0 minimax 0"
			return

		# Iterative Deepening Alpha Beta Search Loop
		limit = 0
		while self.timeOut:
			limit += 1
			v = self.maxValue(self.node, self.maxPlayer, self.minPlayer, -100, 100, limit, True)

			# If the search didn't timeout new board state and minimax estimate are storeed
			if self.timeOut:
				result = self.gameVar.node
				minimaxEstimate = v

			# If the resultis in a terminal state or the mininaxEstimate is then the search is terminated early
			if terminalTest(result, self.maxPlayer, self.minPlayer) or minimaxEstimate >= 100 or minimaxEstimate <= -100:
				self.timeOut = False

			print "Depth", limit, "Nodes", self.gameVar.nodeNum

		# Print the results of the search to the 
		result.printBoard()
		print "move", result.move[0], result.move[1], "nodes", self.gameVar.nodeNum, "minimax", minimaxEstimate


	def maxValue(self, node, movePlayer, otherPlayer, alpha, beta, limit, top):
		# Terminal test
		if node.util > 100 or node.depth == limit:
			return node.util
		v = -100

		tList = tileList(node.state, movePlayer);

		# Loops through the current move players tiles
		i = 0
		while i < len(tList) and self.timeOut:
			j = 0

			# Checks for all possible moves given a tile coordinate and a board state
			while j < len(self.gameVar.deltaList) and self.timeOut:

				# Checks if move is possible given move direction, tile to move and board state
				if canMove(node, self.gameVar.deltaList[j][0], self.gameVar.deltaList[j][1], tList[i], movePlayer, otherPlayer):
					# Creates new node
					nState = copy.deepcopy(node.state)
					t = Tree(nState, node)

					# Increment nodes expanded
					self.gameVar.incNodeNum()

					makeMove(t, self.gameVar.deltaList[j][0], self.gameVar.deltaList[j][1], tList[i], movePlayer, otherPlayer)
					t.util = utilFunc(t, self.maxPlayer, self.minPlayer)

					# If the returned value of minValue is larger a new best board is stored
					vS = self.minValue(t, otherPlayer, movePlayer, alpha, beta, limit)
					if v < vS and top:
						self.gameVar.node = t
					v = max(v, vS)

					alpha = max(alpha, v)
					if v >= beta:
						return v

				j += 1
			i += 1
		return v

	def minValue(self, node, movePlayer, otherPlayer, alpha, beta, limit):
		# Terminal test
		if node.util > 100 or node.depth == limit:
			return node.util
		v = 100

		tList = tileList(node.state, movePlayer);

		# Loops through the current move players tiles
		i = 0
		while i < len(tList) and self.timeOut:
			j = 0

			# Checks for all possible moves given a tile coordinate and a board state
			while j < len(self.gameVar.deltaList) and self.timeOut:

				# Checks if move is possible given move direction, tile to move and board state
				if canMove(node, self.gameVar.deltaList[j][0], self.gameVar.deltaList[j][1], tList[i], movePlayer, otherPlayer):
					# Creates new node
					nState = copy.deepcopy(node.state)
					t = Tree(nState, node)

					# Increment nodes expanded
					self.gameVar.incNodeNum()

					makeMove(t, self.gameVar.deltaList[j][0], self.gameVar.deltaList[j][1], tList[i], movePlayer, otherPlayer)
					t.util = utilFunc(t, self.maxPlayer, self.minPlayer)

					v = min(v, self.maxValue(t, otherPlayer, movePlayer, alpha, beta, limit, False))
					beta = min(beta, v)
					if v <= alpha:
						return v

				j += 1
			i += 1
		return v