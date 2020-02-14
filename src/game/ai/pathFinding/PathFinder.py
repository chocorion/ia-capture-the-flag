from abc import ABC,abstractmethod 
class PathFinder(ABC):

    @abstractmethod
    def __init__(self, graph):
        self._graph = graph
    
    @abstractmethod
    def getPath(self, start, goal):
        pass


