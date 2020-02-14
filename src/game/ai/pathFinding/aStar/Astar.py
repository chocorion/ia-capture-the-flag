from ai.pathFinding.PathFinder import PathFinder
from ai.pathFinding.base import AbstractNode,Heuristic

class Astar(PathFinder):
    
    def __init__(self, graph):
        super().__init__(self, graph)
        raise NotImplementedError
    
    # If need an other representation than the generic graph
    # Else remove this function
    def build_graph(self):
        raise NotImplementedError

    #Override method
    def getPath(self, start, goal):
        raise NotImplementedError
    
    def totalCost(self, node, goal, heuristic):
        raise NotImplementedError
    
    def reconstructPath(self, node, start):
        raise NotImplementedError
    
    def setCurrentNeighbor(self, neighbor, current, goal):
        raise NotImplementedError

    def visitNeighbor(self, current, closed, border, goal):
        raise NotImplementedError
    