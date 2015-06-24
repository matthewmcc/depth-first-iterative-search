import sys
import copy
import thread
import time

from searchThread import *
from gameVar import *
from moveFunc import *

global root

# Gets the configuration of the first board state
def getConfig(state):
	l = sys.stdin.readline().strip()
	if l == "- abcdefgh":
		i, j = 0, 0
		while i < 8:
			l = sys.stdin.readline().strip()
			l = l[2:]
			while j < 8:
				state[i][j] = l[j]
				j += 1
			i += 1
			j = 0
		l = sys.stdin.readline().strip()

		# Sets the values of the current player and oppoenent move 
		if l[:1] in ('O, B') and i == 8:
			global players
			player = l[0]
			if player == 'B':
				opponent = 'O'
			else:
				opponent = 'B'

			players = (player, opponent)

			global tAllowed				
			tAllowed = int(l[2:])
		else:
			synErr(l, i)
	else:
		synErr(l, i)
	return board


# prints incorrect board entry error and exits
def synErr(l, i):
	print "Incorrect board configuration at input line number", i
	if i != None:
		print l
	sys.exit()


# List of tuples for all movement directions
global deltaList
deltaList = [(0, -1), (-1, 0), (-1, -1), (+1, 0), (0, +1), (+1, +1), (-1, +1), (+1, -1)]
setDeltaList(deltaList)

board = [[0]*8 for i in range(8)]
root = Tree(getConfig(board), None)
root.util = utilFunc(root, players[0], players[1])

gameVar = GameVar(0, 0, deltaList)

succ = SearchThread(root, True, players[0], players[1], gameVar)
succ.start()

# Checks if successor has returned, if not sleeps one msec and then polls again
ms = 0
tAllowed *= 400

while succ.isAlive() and ms < tAllowed:
	time.sleep(.001)
	ms += 1
succ.timeOut = False
