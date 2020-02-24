from ai.behaviorTree import *

class Leaf(NodeTree):
    """
    Implemetation of NodeTree, this class represent the leaf of the behavior tree.

    Attributes:
        _fun (function(int)) : Function launched in tick.
    """

    
    def __init__(self, fun):
        super().__init__()
        self._fun = fun


    def tick(self, dt):
        """
        This function override NodeTree.tick().
        In this method we call the function given to the constructor.
        
        Parameters :
            dt (int) : Delta time, used by function in leaf for time management.

        Return : 
            State (int) : Must be NodeTree.RUNNING, NodeTree.SUCCESS or NodeTree.FAILURE.
        """

        return self._fun(dt)