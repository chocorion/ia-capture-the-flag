from abc import ABC,abstractmethod 
class AbstractNode(ABC):
    
    @abstractmethod
    def __init__(self):
        self._x           = None
        self._y           = None
        self._cellContent = None
        self._neighbors   = None
        self._parent      = None
    
    @abstractmethod
    def addNeighbor(self, node):
        pass

    @abstractmethod
    def getNeighbors(self):
        pass
    

