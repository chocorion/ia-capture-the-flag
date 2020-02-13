import math
class Heuristic():

    @staticmethod
    def manhattanDistance(node, goal):
        x = abs(node.x - goal.x)
        y = abs(node.y - goal.y)
        return x + y

    @staticmethod
    def euclideanDistance(node, goal):
        x = (node.x - goal.x) ** 2 
        y = (node.y - goal.y) ** 2
        return math.sqrt(x + y)
