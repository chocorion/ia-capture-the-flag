from ai.pathFinding.base.AbstractNode import AbstractNode

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

    #Override method
    def addNeighbor(self, node):
        self._neighbors.insert(0, node)

    #Override method
    def getNeighbors(self):
        raise NotImplementedError

    def _setCellCosts(self):
        raise NotImplementedError

