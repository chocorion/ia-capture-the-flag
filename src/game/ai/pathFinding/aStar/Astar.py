from ai.pathFinding.PathFinder import PathFinder
from ai.pathFinding.base import AbstractNode,Heuristic
from ai.pathFinding.aStar.NodeAstar import NodeAstar
from domain.GameObject.Block import *
from domain.Map import Map
import bisect
class Astar(PathFinder):
    
    def __init__(self, graph):
        super().__init__(graph)
    # If need an other representation than the generic graph
    # Else remove this function
    def build_graph(self):
        raise NotImplementedError
    
    def getNodeStartGoal(self, start, goal):
        x, y, cellContent = start[0] // Map.BLOCKSIZE, start[1] // Map.BLOCKSIZE, Empty()
        nodeStart = NodeAstar(x, y, cellContent)
        x, y, cellContent = goal[0] // Map.BLOCKSIZE, goal[1] // Map.BLOCKSIZE, Empty()
        nodeGoal  = NodeAstar(x, y, cellContent)
        return nodeStart, nodeGoal
    
    #Override method
    def getPath(self, start, goal):
        nodeStart, nodeGoal = self.getNodeStartGoal(start, goal)
        border = [nodeStart]
        closed = []

        while border:
            #print(border)
            current = border[0] # Get node with least cost

            if current == nodeGoal:
                path = self.reconstructPath(current, nodeStart)
                #print(path)
                return path

            # Remove current from border and add it to closed list
            del border[0]
            closed.insert(0,current)
            current.createNeighbors(self._graph)
            self.visitNeighbor(current, closed, border, nodeGoal)
        

    def totalCost(self, node, nodeGoal, heuristic):
        return node._cost + heuristic(node, nodeGoal)
    
    def reconstructPath(self, node, nodeStart):
        path = []
        path.append((node._x, node._y))
        while node != nodeStart:
            node = node._parent
            if not node : break # Should not occurs but occurs
            path.insert(0,(node._x, node._y))
        return path
    
    def setCurrentNeighbor(self, neighbor, current, nodeGoal):
        neighbor._parent        = current
        neighbor._cost          = current._cost + neighbor._cellCost
        neighbor._estimatedCost = self.totalCost(neighbor, nodeGoal, Heuristic.Heuristic.manhattanDistance)
        return neighbor


    def visitNeighbor(self, current, closed, border, nodeGoal):
        for neighbor in current._neighbors:
            
            if self.isSolid(neighbor):
                closed.insert(0,neighbor)
                continue
        
            if neighbor in closed or neighbor in border:
                continue

            neighbor = self.setCurrentNeighbor(neighbor, current, nodeGoal)
            if neighbor not in border:
                border.insert(0,neighbor) 
                #bisect.insort(border,neighbor)
        border.sort()
    
    def isSolid(self, node):
        solid = [Wall , WallTransparent]
        for s in solid:
            if isinstance(node._cellContent, s):
                return True
        return False                