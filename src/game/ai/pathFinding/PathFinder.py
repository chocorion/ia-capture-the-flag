from abc import ABC,abstractmethod 
class PathFinder(ABC):
    
    @abstractmethod
    def getPath(self, start, goal, nodeGraph):
        pass


