from service.Physics import PhysicsMethods

from math import sqrt, atan2, cos, sin, degrees, radians

class PythonPhysics(PhysicsMethods):
    """
    Implements PhysicsMethods using python.
    """

    def distance(self,x1,x2,y1,y2):
        return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))

    def angularDistance(self,a,b):
        p = abs(b - a)
        return 360 - p if p > 180 else p

    def getAngle(self, x, y, target_x, target_y):
        return degrees(atan2(target_y - y, target_x - x))

    def applyMovement(self, x, y, angle, distance):
        return (x + distance * cos(radians(angle)),y + distance * sin(radians(angle)))

    def isInCircle(self,x1,y1,x2,y2,radius):
        return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2)) <= radius # Useless to call distance for this

    def rectIntersectsCircle(self,x1,y1,w,h,x2,y2,radius):
        # does not check if a side intersect with the circle, only corners.
        return self.isInCircle(x1,y1,x2,y2,radius) or self.isInCircle(x1+w,y1,x2,y2,radius) or self.isInCircle(x1+w,y1,x2+h,y2,radius) or self.isInCircle(x1,y1,x2+h,y2,radius)

    def polygonIntersectsRect(self, vertices, rx, ry, rw, rh):

        # go through each of the vertices, plus the next
        # vertex in the list
        next_ = 0
        for current in range(0,len(vertices)):

            # get next vertex in list
            # if we've hit the end, wrap around to 0
            next_ = current+1
            if (next_ == len(vertices)):
                next_ = 0

            # get the PVectors at our current position
            # this makes our if statement a little cleaner
            (vcx,vcy) = vertices[current];    # c for "current"
            (vnx,vny) = vertices[next];       # n for "next"

            # check against all four sides of the rectangle
            if self.lineIntersectsLine(vcx,vcy,vnx,vny, rx,ry,rw,rh):
                return True

            # test if the rectangle is INSIDE the polygon
            # note that this iterates all sides of the polygon
            # again, so only use this if you need to
            if self.pointInsidePolygon(vertices, rx,ry):
                return True

        return False

    def lineIntersectsRect(self, x1, y1, x2, y2, rx, ry, rw, rh):
        # check if the line has hit any of the rectangle's sides
        # uses the Line/Line function below
        left =   self.lineIntersectsLine(x1,y1,x2,y2, rx,ry,rx, ry+rh)
        right =  self.lineIntersectsLine(x1,y1,x2,y2, rx+rw,ry, rx+rw,ry+rh)
        top =    self.lineIntersectsLine(x1,y1,x2,y2, rx,ry, rx+rw,ry)
        bottom = self.lineIntersectsLine(x1,y1,x2,y2, rx,ry+rh, rx+rw,ry+rh)

        # if ANY of the above are true,
        # the line has hit the rectangle
        return (left or right or top or bottom)

    def lineIntersectsLine(self, x1, y1, x2, y2, x3, y3, x4, y4):
        # calculate the direction of the lines
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))

        # if uA and uB are between 0-1, lines are colliding
        return (uA >= 0 and uA <= 1 and uB >= 0 and uB <= 1)        

    def pointInsidePolygon(self, vertices, x, y):
        collision = False

        # go through each of the vertices, plus the next
        # vertex in the list
        next_ = 0
        for current in range(0,len(vertices)):

            # get next vertex in list
            # if we've hit the end, wrap around to 0
            next_ = current+1
            if (next_ == len(vertices)):
                next_ = 0

            # get the PVectors at our current position
            # this makes our if statement a little cleaner
            (vcx,vcy) = vertices[current];    # c for "current"
            (vnx,vny) = vertices[next_];       # n for "next"

            # compare position, flip 'collision' variable
            # back and forth
            if (((vcy > y and vny < y) or (vcy < y and vny > y)) or (x < (vnx-vcx)*(y-vcy) / (vny-vcy)+vcx)):
                    collision = not collision
            
        return collision
