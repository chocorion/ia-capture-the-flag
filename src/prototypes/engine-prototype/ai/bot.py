'''
Bot for user AI.
'''
class Bot:
    def __init__(self, x=0., y=0., angle=0.):
        self._x = x
        self._y = y
        self._angle = angle
    
    def __repr__(self):
        return "Bot({}, {}, {})".format(self._x, self._y, self._angle)