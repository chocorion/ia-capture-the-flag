
# The game terrain on which the game takes place
class Map:

    def __init__(self):
        raise NotImplementedError

    # Return a map Cell at the coordinates (x,y)
    # The coordinates range from 0 to the amount of tiles in the specific direction
    def getCell(self, x, y):
        raise NotImplementedError