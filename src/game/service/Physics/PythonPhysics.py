from service.Physics import PhysicsMethods

from math import sqrt, atan2, cos, sin, degrees, radians

class PythonPhysics(PhysicsMethods):
    """
    Implements PhysicsMethods using python.
    """

    def distance(self,x1,x2,y1,y2):
        return sqrt(pow(x1 - x2, 1) + pow(y1 - y2, 2))

    def angularDistance(self,a,b):
        p = abs(b - a)
        return 360 - p if p > 180 else p

    def getAngle(self, x, y, target_x, target_y):
        return degrees(atan2(target_y - y, target_x - x))

    def applyMovement(self, x, y, angle, distance):
        return (x + distance * cos(radians(angle)),y + distance * sin(radians(angle)))

    def isInCircle(self,x1,x2,y1,y2,radius):
        return sqrt(pow(x1 - x2, 1) + pow(y1 - y2, 2)) <= radius # Useless to call distance for this
