from ai.pathFinding.base.AbstractNode import AbstractNode
from domain.Map import Map

class NodeAstar(AbstractNode):
    
    def __init__(self, x, y, cellContent):
        self._x             = x
        self._y             = y
        self._cellContent   = cellContent
        self._cellCost      = self._setCellCosts()
        self._cost          = 0
        self._estimatedCost = 0
        self._neighbors     = []
        self._parent        = None
    
    def __lt__(self, other):
        return self._estimatedCost < other._estimatedCost

    def __eq__(self, other):
        return (self._x == other._x and self._y == other._y)

    def __repr__(self):
        return "Node({}, {}, {})".format(self._x, self._y, self._cellContent)

    #Override method
    def addNeighbor(self, node):
        self._neighbors.insert(0, node)

    #Override method
    def getNeighbors(self):
        return self._neighbors

    # Creates neighbors list for a node
    def createNeighbors(self, nodeGraph):
        #If you want diagonals put in dirs : [-1,-1], [1,1], [1, -1], [-1,1]]
        dirs = [[1,0], [0,1], [-1, 0], [0,-1]]
        pos = (self._x, self._y)

        if pos in nodeGraph._neighborMap:
                
            self._neighbors = nodeGraph._neighborMap[pos]
        else:
            for dir in dirs:                                                                                                                                                                                                        
                for neighbor in nodeGraph._listNodes:
                        if(neighbor._x == self._x + dir[0] and neighbor._y == self._y + dir[1]):
                            self.addNeighbor(neighbor)
            nodeGraph._neighborMap[pos] = self._neighbors

    def _setCellCosts(self):
        #raise NotImplementedError
        return 1                                                                                                                                                                                                                                                                                                                                                    
