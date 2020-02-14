
# A collection of methods to help with game physics
class Physics():

    instance = None

    # Needs to be called before using any methods
    @staticmethod
    def SetInstance(instance):
        Physics.instance = instance

    @staticmethod
    def isInCircle(x1,x2,y1,y2,radius):
        Physics.instance.isInCircle(x1,x2,y1,y2,radius)