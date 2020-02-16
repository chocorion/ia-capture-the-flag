
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
    def isInCircle(x1,x2,y1,y2,radius):
        """
        Returns wether a point (x1,y1) is inside a circle (x2,y2,radius).
        """
        Physics.instance.isInCircle(x1,x2,y1,y2,radius)