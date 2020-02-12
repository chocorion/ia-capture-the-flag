from domain.Map import Map
from domain.GameObject.Block import *
from domain.GameObject.Flag import Flag

class RegularMap(Map):

    def __init__(self, mapData):
        self._blockHeight = mapData["blockHeight"]
        self._blockWidth = mapData["blockWidth"]
        self._height = mapData["height"]
        self._width = mapData["width"]
        self._blocks = mapData["blocks"]
        self._flags = mapData["flags"]

    @staticmethod
    def loadMapData(filename):

        data = {
            "height": None,         # Real height (set by model)
            "width": None,          # Real width (set by model)
            "blockHeight": None,    # The height of the map in blocks
            "blockWidth": None,     # The width of the map in blocks
            "blocks": None,         # A two dimensionnal array for storing blocks
            "flags": None,          # The flags for each team to obtain
        }
        blocks = {
            '#': 'Wall()',
            '-': 'WallTransparent()',
            ' ': 'Empty()',
            '1': 'Spawn(1)',
            '2': 'Spawn(2)'
        }

        with open(filename, "r") as file:
            lines = file.readlines()

            data["blockWidth"] = int(lines[0].split(":")[1])
            data["blockHeight"] = int(lines[1].split(":")[1])

            data["height"] = data["blockHeight"] * Map.CELLSIZE
            data["width"] = data["blockWidth"] * Map.CELLSIZE

            mapLines = lines[3:data["blockHeight"]+3] # Lines between 'height:__' and the end of the tiles definition in the file

            data["blocks"] = [[None for i in range(data["blockWidth"])] for i in range(data["blockHeight"])]

            for y in range(data["blockHeight"]):
                for x in range(data["blockWidth"]):
                    if mapLines[y][x] not in blocks.keys():
                        continue

                    data["blocks"][y][x] = eval(blocks[mapLines[y][x]])

            data["flags"] = list()

            # Read the remaining info in the file
            for line in lines[data["blockHeight"]+2:]:
                # Get the attribute and it's value without '\n' (:-1)
                attributes = line[:-1].split(':')

                if attributes[0] == "flag":
                    info = attributes[1].split(',')

                    data["flags"].append(Flag(info[0], info[1] * Map.CELLSIZE, info[2] * Map.CELLSIZE))


        return data