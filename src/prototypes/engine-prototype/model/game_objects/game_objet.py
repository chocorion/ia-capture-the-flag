from math import sqrt

class Game_object():
    def __init__(self, x=0., y=0.):
        '''
        x : float
        y : float
        '''
        self._x = x
        self._y = y


    def distance_to(other):
        return sqrt((self._x - other._x)**2 - (self._y - other._y)**2)


    def get_x(self):
        return self._x

    def get_y(self):
        return self._y