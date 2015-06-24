# Tree class used for 
class Tree(object):
    def __init__(self, state, parent):
        self.child = None
        self.move = None
        self.state = state
        self.parent = parent
        self.util = 0

        # Increments the depth of the node
        if parent == None:
            self.depth = 0
        else: self.depth = parent.depth + 1

	# Prints the given board state to the console
    def printBoard(self):
    	i = 0
    	while i < 8:
    		print self.arrayToString(i)
    		i += 1

	# Returns a row of the board as a SyntaxWarning
    def arrayToString(self, i):
    	s = ""
    	j = 0
    	while j < 8:
    		s += str(self.state[i][j])
    		j += 1
    	return s

    def setMove(self, move): self.move = move