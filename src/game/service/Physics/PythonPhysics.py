from service.Physics import PhysicsMethods

from math import sqrt

class PythonPhysics(PhysicsMethods):

    def isInCircle(self,x1,x2,y1,y2,radius):
        return sqrt(pow(x1 - x2, 1) + pow(y1 - y2, 2)) <= radius
