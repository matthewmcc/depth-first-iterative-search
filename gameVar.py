# Used so Node number and depth of search could be referenced...
# ...within and outside thread.
class GameVar:
    def __init__(self, nodeNum, depth, deltaList): 
    	self.nodeNum = nodeNum
    	self.depth = depth
    	self.deltaList = deltaList
    	self.node = None

    # Increment and return functions for the nodeNum and depth values
    def getNodeNum(self):	return self.nodeNum
    def incNodeNum(self):   self.nodeNum += 1
    def getDepth(self): return self.depth
    def incDepth(self): self.depth += 1
