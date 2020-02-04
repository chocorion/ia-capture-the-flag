'''
Bot for user AI.
'''
class Bot:
    def __init__(self, x=0., y=0., angle=0.):
        self._x = x
        self._y = y
        self._angle = angle

        self._current_dest = ()


    def set_dest(self, x, y):
        self._dest = (x, y)


    def get_dest(self):
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