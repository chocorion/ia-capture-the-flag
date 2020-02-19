
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
    def getAngle(x, y, target_x, target_y):
        """
        Returns the angle in degrees needed to face a direction from a certain point of reference.
        """
        return Physics.instance.getAngle(x, y, target_x, target_y)

    @staticmethod
    def applyMovement(x, y, angle, distance):
        """
        Get a new point after applying angle and distance
        """
        return Physics.instance.applyMovement(x, y, angle, distance)

    @staticmethod
    def isInCircle(x1,x2,y1,y2,radius):
        """
        Returns wether a point (x1,y1) is inside a circle (x2,y2,radius).
        """
        return Physics.instance.isInCircle(x1,x2,y1,y2,radius)

    @staticmethod
    def rectIntersectsCircle(x1,y1,w,h,x2,y2,radius):
        """
        Returns wether a rect (x1,y1,w,h) is inside a circle (x2,y2,radius).
        """
        return Physics.instance.rectIntersectsCircle(x1,y1,w,h,x2,y2,radius)