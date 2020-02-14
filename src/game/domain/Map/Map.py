
# The game terrain on which the game takes place
class Map:

    BLOCKSIZE = 100

    # mapData: The data used to create the map in memory
    def __init__(self, mapData):
        self.width = None          # Width in real coordinates
        self.height = None         # Height in real coordinates
        self.blockWidth = None     # Width in real coordinates
        self.blockHeight = None    # Width in real coordinates
        self.blocks = None         # 2 dimensional array
        self._bots = None           # the player's bots

    # Implement this method to get the required data for the constructor
    @staticmethod
    def loadMapData(source):
        raise NotImplementedError

    # Return a map Cell at the coordinates (x,y)
    # The coordinates range from 0 to the amount of tiles in the specific direction
    def getCell(self, x, y):
        raise NotImplementedError