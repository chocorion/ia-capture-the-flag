import bisect
import math
import collections
import time
from ai.astar.node import Node
from ai.astar.board import *

from queue import PriorityQueue
# Result from A*, able to return multiple variables
Result = collections.namedtuple('Result', ['path', 'border', 'closed'])

PathMap = {}


# Heuristic cost methods (Estimated cost to goal)
############

def manhattanDistance(node, goal):
    x = abs(node.x - goal.x)
    y = abs(node.y - goal.y)
    return x + y


def euclideanDistance(node, goal):
    x = (node.x - goal.x) ** 2 
    y = (node.y - goal.y) ** 2
    return math.sqrt(x + y)

############

# Cost so far and heuristic cost
def totalCost(node, goal):
    return node.cost + manhattanDistance(node, goal)


# Reconstruct shortest path from start to goal node
def reconstructPath(node, start):
    path = []
    path.append(node)
    while node != start:
        node = node.parent
        path.insert(0, node)
    return path



def getPath(current, start, border, closed):
    path = Result(
        reconstructPath(current, start)
        , border
        , closed
    )

    PathMap[(start.x, start.y, current.x, current.y)] = path
    return path

def setCurrentNeighbor(neighbor, current, goal):
    neighbor.parent        = current
    neighbor.cost          = current.cost + neighbor.cellCost
    neighbor.estimatedCost = totalCost(neighbor, goal)
    return neighbor

def isSolid(neighbor):
    Solids = ['#', '-']
    return neighbor.cellContent in Solids
    
def visitNeighbor(current, closed, border, goal):
    for neighbor in current.neighbors:
        if isSolid(neighbor): # Blocked node
            #closed.append(neighbor)
            closed.insert(0,neighbor) #opti
            continue
        
        if neighbor in closed or neighbor in border:
            continue

        neighbor = setCurrentNeighbor(neighbor, current, goal)

        if neighbor not in border:
            border.insert(0,neighbor) #opti
            #bisect.insort(border, neighbor) # Adds node in border list (Ascending order)
    border.sort() #opti
    

# Calculate shortest path form start to goal
def a_star(start, goal, nodeGraph):
    #First check if path already contained in pathMap (no need to recalculate it)
    extremity = (int(start.x), int(start.y), goal.x, goal.y)

    if extremity in PathMap:
        print("Find the Path ! " + str(extremity))
        return PathMap[extremity]

    border = [start]
    closed = []
    
    while border:
        current = border[0] # Get node with least cost
        
        if current == goal:
            return getPath(current, start, border, closed)

        # Remove current from border and add it to closed list
        del border[0]
        #closed.append(current)
        closed.insert(0,current) #opti
        createNeighbors(current, nodeGraph)
        visitNeighbor(current, closed, border, goal)

