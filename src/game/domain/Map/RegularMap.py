from domain.Map import Map
from domain.GameObject.Block import *
from domain.GameObject.Flag import Flag
from random import *

class RegularMap(Map):

    def __init__(self, mapData):
        self._blockHeight = mapData["blockHeight"]
        self._blockWidth = mapData["blockWidth"]
        self._height = mapData["height"]
        self._width = mapData["width"]
        self._blocks = mapData["blocks"]
        self._flags = mapData["flags"]
        self._spawns = mapData["spawns"]
        self._bots = list()

    @staticmethod
    def loadMapData(filename):

        # To use for the 'mapData' parameter in constructor
        data = {
            "height": None,         # Real height (set by model)
            "width": None,          # Real width (set by model)
            "blockHeight": None,    # The height of the map in blocks
            "blockWidth": None,     # The width of the map in blocks
            "blocks": None,         # A two dimensionnal array for storing blocks
            "flags": None,          # The flags for each team to obtain
            "spawns": None,          # Remember the spawn locations for each team
        }

        # The format character for each tile and it's constructor call
        blocks = {
            '#': 'Wall()',
            '-': 'WallTransparent()',
            ' ': 'Empty()',
            '1': 'Spawn(1)',
            '2': 'Spawn(2)'
        }

        data["spawns"] = { 1: [], 2: [] } # Spawn blocks for each team

        with open(filename, "r") as file:
            lines = file.readlines()

            mapDefinitionLines = 2 # The amount of lines before the map tiling

            data["blockWidth"] = int(lines[0].split(":")[1])
            data["blockHeight"] = int(lines[1].split(":")[1])

            data["height"] = data["blockHeight"] * Map.BLOCKSIZE
            data["width"] = data["blockWidth"] * Map.BLOCKSIZE

            # The file lines that contains the map tiling
            # Used to fill 'data["blocks"]' according to 'blocks'
            mapLines = lines[mapDefinitionLines : data["blockHeight"] + mapDefinitionLines]

            data["blocks"] = [[None for i in range(data["blockWidth"])] for i in range(data["blockHeight"])]

            for y in range(data["blockHeight"]):
                for x in range(data["blockWidth"]):
                    if mapLines[y][x] not in blocks.keys():
                        continue

                    data["blocks"][y][x] = eval(blocks[mapLines[y][x]])

                    # Game Objects know their location
                    data["blocks"][y][x].x = x * Map.BLOCKSIZE # Position is top-left
                    data["blocks"][y][x].y = y * Map.BLOCKSIZE

                    if(type(data["blocks"][y][x]).__name__ == "Spawn"):
                        # If this is a spawn block, add it to it's team's spawn blocks
                        data["spawns"][data["blocks"][y][x].team].append(data["blocks"][y][x]) 

            data["flags"] = list()

            # Read the remaining info in the file
            # starts after the map tiling
            for line in lines[data["blockHeight"] + mapDefinitionLines :]:
                # Get the attribute and it's value without '\n' (:-1)
                attributes = line[:-1].split(':')

                # flag: team, blockX, blockY
                if attributes[0] == "flag":
                    info = attributes[1].split(',')

                    # Create the new flag while converting the block X and Y to real coordinates
                    data["flags"].append(Flag(int(info[0]), int(info[1] * Map.BLOCKSIZE), int(info[2] * Map.BLOCKSIZE)))

                    continue

        return data

    def GetRandomPositionInSpawn(self, team):
        block = choice(self._spawns[team])
        return (block.x + randint(0,Map.BLOCKSIZE), block.y + randint(0,Map.BLOCKSIZE))