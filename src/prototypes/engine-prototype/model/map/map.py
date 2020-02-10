from model.blocks import *

blocks = {
    '#': 'Wall()',
    '-': 'Transparent_wall()',
    'F': 'Flag()',
    ' ': 'Empty()',
    '1': 'Spawn(1)',
    '2': 'Spawn(2)'
}

class Map:
    # Ugly cell size here, but needed for ai
    def __init__(self, filename, cell_size):
        self._filename = filename
        self._load_from_file(filename)
        self._cell_size = cell_size
        

    def _load_from_file(self, filename):
        with open(filename, "r") as file:
            lines = file.readlines()
            
            # -1 for \n char
            self._height = len(lines)
            self._width = len(lines[0]) - 1 

            self._map = [[None for i in range(self._width)] for i in range(self._height)]

            for y in range(self._height):
                for x in range(self._width):
                    if lines[y][x] not in blocks.keys():
                        continue

                    self._map[y][x] = eval(blocks[lines[y][x]])


    def get_spawn_zones(self):
        zones = {
            1 : [],
            2 : []
        }

        for y in range(self._height):
            for x in range(self._width):
                if self._map[y][x].get_name() == 'spawn':
                    team = self._map[y][x].get_team()

                    if zones[team] == []:
                        zones[team] = [x, y, 1, 1]
                    else:
                        zones[team] = [
                            zones[team][0],
                            zones[team][1],
                            zones[team][2] + 1 if x > zones[team][0] + zones[team][2] - 1 else zones[team][2],
                            zones[team][3] + 1 if y > zones[team][1] + zones[team][3] - 1 else zones[team][3]
                        ]
        return zones


    def get_width(self):
        return self._width

    
    def get_height(self):
        return self._height


    def is_solid(self, x, y):
        return self._map[y][x].is_solid()

    def is_empty(self, x, y):
        return isinstance(self._map[y][x], Empty)

    def get_tile(self, x, y):
        return self._map[y][x]

    def get_cell_size(self):
        return self._cell_size

    def mark_start_cell(self, x, y):
        self._map[y][x] = Start()

    def mark_end_cell(self, x, y):
        self._map[y][x] = End()

    def mark(self, x, y):
        self._map[y][x] = Way()

    def unmark(self, x, y):
        if isinstance(self._map[y][x], Start) or isinstance(self._map[y][x], End):
            self._map[y][x] = Empty()

    def clear_path(self):
        for y in range(self._height):
            for x in range(self._width):
                if isinstance(self._map[y][x], Way):
                    self._map[y][x] = Empty()

    def __repr__(self):
        return "Map({})".format(self._filename)
        
        
    def __str__(self):
        result = ""
        for y in range(self._height):
            for x in range(self._width):
                result += str(self._map[y][x])
            result += '\n'
        
        return result

