from ai.astar import *

import math

def distance(x1, y1, x2, y2):
    x = (x2 - x1) ** 2 
    y = (y2 - y1) ** 2
    return math.sqrt(x + y)

'''
Bot for user AI.
'''
class Bot:
    def __init__(self, game_map=None, x=0., y=0., angle=0.):
        self._x = x
        self._y = y
        self._angle = angle

        self._current_dest = ()
        self._map = game_map

        self._path_index = -1
        self._path = None


    def set_dest(self, x, y, node_graph=None):
        if node_graph != None:
            cell_size = self._map.get_cell_size()
            print("Bot compute A*...")
            print("I'm from ", self._x // self._map.get_cell_size(), self._y // self._map.get_cell_size())
            result = a_star(
                Node(
                    self._x // cell_size,
                    self._y // cell_size,
                    '#'
                ),
                Node(x, y, '#'),
                node_graph
            )

            path = list()

            for node in result[0]:
                path.append((node.x * cell_size + cell_size//2, node.y * cell_size + cell_size//2))

            self._path = path
            self._path_index = 0

        self._dest = (x, y)


    def get_dest(self):
        return self._dest

    def is_position_check(self, position_x, position_y):
        return distance(self._x, self._y, position_x, position_y) < 20

    def get_next_dest(self):
        ''' Return the next position of the bot'''

        # Basic situation, bot don't use A*
        if self._path_index == -1:
            return self._dest

        (dest_x, dest_y) = self._path[self._path_index]

        if self.is_position_check(dest_x, dest_y):
            if self._path_index + 1 < len(self._path):
                self._path_index += 1

                return self.get_next_dest()

        return (dest_x, dest_y)
            


        

    def save_pos(self):
        self._saved_pos = (self._x, self._y)

    def get_saved_pos(self):
        return self._saved_pos

    def update(self, x, y, angle):
        self._x = x
        self._y = y
        self._angle = angle
        
    
    def __repr__(self):
        return "Bot({}, {}, {})".format(self._x, self._y, self._angle)