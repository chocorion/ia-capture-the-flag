from ai.astar import *

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


    def set_dest(self, x, y, node_graph=None):
        if node_graph != None:
            print("Bot compute A*...")
            print("I'm from ", self._x // self._map.get_cell_size(), self._y // self._map.get_cell_size())
            result = a_star(
                Node(
                    self._x // self._map.get_cell_size(),
                    self._y // self._map.get_cell_size(),
                    '#'
                ),
                Node(x, y, '#'),
                node_graph
            )

            print(result)

        self._dest = (x, y)


    def get_dest(self):

        return self._dest

    def get_next_dest(self):
        ''' Return the next position of the bot'''
        return self._dest

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