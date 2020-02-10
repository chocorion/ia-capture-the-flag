class Node:

    def __init__(self, x, y, cellContent):
        self.x = x
        self.y = y
        self.cellContent = cellContent
        self.cellCost = self.setCellCosts()
        self.cost = 0
        self.estimatedCost = 0
        self.neighbors = []
        self.parent = None
    
    def __repr__(self):
        return "Node({}, {}, {})".format(self.x, self.y, self.cellContent)

    def addNeighbor(self, node):
        self.neighbors.append(node)

    def __lt__(self, other):
        return self.estimatedCost < other.estimatedCost

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    # Get cell cost based on content
    def setCellCosts(self):
        # Water
        if self.cellContent is 'w':
            return 100

        # Mountains
        if self.cellContent is 'm':
            return 50

        # Forests
        if self.cellContent is 'f':
            return 10

        # Grassland
        if self.cellContent is 'g':
            return 5

        # Roads
        if self.cellContent is 'r':
            return 1

        # Default
        return 1
