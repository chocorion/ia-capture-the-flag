import math
class Heuristic():

    @staticmethod
    def manhattanDistance(node, goal):
        x = abs(node._x - goal._x)
        y = abs(node._y - goal._y)
        return x + y

    @staticmethod
    def euclideanDistance(node, goal):
        x = (node._x - goal._x) ** 2 
        y = (node._y - goal._y) ** 2
        return math.sqrt(x + y)
