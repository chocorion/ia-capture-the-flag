from random import *

class Map:
    """
    The game terrain on which the game takes place.

    BLOCKSIZE : The size of the side of a block.

    Attributes:
        inside mapData :
        width (int):        Width in real coordinates
        height (int):       Height in real coordinates
        blockWidth (int):   Width in amount of blocks
        blockHeight (int):  Height in amount of blocks
        blocks (list):      2 dimensional array containing the map blocks
        bots (list):        The player's bots
    """

    BLOCKSIZE = None # Given in mapdata

    def __init__(self, mapData):
        """
        Initialize the Map according to mapData.

        Parameters:
            mapData (dict) : Must contain enough informations to initialize each attribute.
        """
        raise NotImplementedError

    @staticmethod
    def loadMapData(source):
        """
        Load the mapData dictionary using any source. Implement this method to get the required data for the constructor
        """
        raise NotImplementedError

    def getCell(self, x, y):
        """
        Return a map Cell at the coordinates (x,y)

        Returns:
            point (x,y): Ranges from 0 to the amount of blocks (blockWidth for x and blockHeight for y).
        """
        raise NotImplementedError

    @staticmethod
    def GetRandomPositionInBlock(block, margin = 0):
        """
        Obtain a random coordinate inside a block

        Parameters:
            block (Block): A block with x and y coordinates.

        Returns:
            point (x,y): A point inside the given block.
        """
        return (block.x + randint(margin,Map.BLOCKSIZE - margin), block.y + randint(margin,Map.BLOCKSIZE - margin))