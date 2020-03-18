
class Physics():
    """
    Collection of methods related to physics.

    Attributes:
        instance (PhysicsMethods) : Any class that implements PhysicsMethods.
    """

    instance = None

    @staticmethod
    def SetInstance(instance):
        """
        Used to set the object that will be used to process method calls.
        """
        Physics.instance = instance

    @staticmethod
    def distance(x1,x2,y1,y2):
        """
        Returns the distance between two points, (x1,y1) and (x2,y2).
        """
        return Physics.instance.distance(x1,x2,y1,y2)
        
    @staticmethod
    def angularDistance(a,b):
        """
        Returns the angular distance between angles in degrees.
        """
        return Physics.instance.angularDistance(a,b)

    @staticmethod
    def getAngle(x, y, targetX, targetY):
        """
        Returns the angle in degrees needed to face a direction from a certain point of reference.
        """
        return Physics.instance.getAngle(x, y, targetX, targetY)

    @staticmethod
    def applyMovement(x, y, angle, distance):
        """
        Get a new point after applying angle and distance
        """
        return Physics.instance.applyMovement(x, y, angle, distance)

    @staticmethod
    def isInCircle(x1,x2,y1,y2,radius):
        """
        Returns whether a point (x1,y1) is inside a circle (x2,y2,radius).
        """
        return Physics.instance.isInCircle(x1,x2,y1,y2,radius)

    @staticmethod
    def rectIntersectsCircle(x1,y1,w,h,x2,y2,radius):
        """
        Returns whether a rect (x1,y1,w,h) is inside a circle (x2,y2,radius).
        """
        return Physics.instance.rectIntersectsCircle(x1,y1,w,h,x2,y2,radius)
    
    @staticmethod
    def polygonIntersectsRect(vertices, rx, ry, rw, rh):
        """
        Returns whether a polygon (vertices : list((x,y))) intersects or is inside a rectangle (x,y,w,h)
        """
        return Physics.instance.polygonIntersectsRect(vertices, rx, ry, rw, rh)

    @staticmethod
    def lineIntersectsRect(x1, y1, x2, y2, rx, ry, rw, rh):
        """
        Returns whether a line (x1,y1,x2,y2) intersects a rectangle (x,y,w,h)
        """
        return Physics.instance.lineIntersectsRect(x1, y1, x2, y2, rx, ry, rw, rh)

    @staticmethod
    def lineIntersectsLine(x1, y1, x2, y2, x3, y3, x4, y4):
        """
        Returns whether a line (x1,y1,x2,y2) intersects with another line (x3,y3,x4,y4)
        """
        return Physics.instance.lineIntersectsLine(x1, y1, x2, y2, x3, y3, x4, y4)

    @staticmethod
    def pointInsidePolygon(vertices, x, y):
        """
        Returns whether a point (x,y) is inside a polygon (vertices : list((x,y)))
        """
        return Physics.instance.pointInsidePolygon(vertices, x, y)

    @staticmethod
    def createCirclePolygon(nbVertices):
        """
        Returns a new polygon with (nbVertices) equal sides.
        """
        return Physics.instance.createCirclePolygon(nbVertices)