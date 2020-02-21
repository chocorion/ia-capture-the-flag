from ai.behaviorTree import *

class Succeeder(NodeTreeSingleChild):
    """
    Implemetation of NodeTreeSingleChild, this class represent a succeeder.

    Attributes:
        _fun (function(int)) : Function launched in tick.
    """

    
    def __init__(self):
        super().__init__()


    def tick(self, dt):
        """
        This function override NodeTree.tick().
        Run its child and return success, except if child status is : Running
        
        Parameters :
            dt (int) : Delta time.

        Return : 
            State (int) : Must be NodeTree.RUNNING or NodeTree.SUCCESS.
        """

        status = super().getChild().tick(dt)

        if status == NodeTree.RUNNING:
            return status

        return NodeTree.SUCCESS