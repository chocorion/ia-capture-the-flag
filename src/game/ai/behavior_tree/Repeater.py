from ai.behavior_tree import *


class Repeater(NodeTreeSingleChild):
    """
    Implementation of NodeTree, this class represent a control node, the repeater.
    Must have only on children
    Attributes : 
        _iteration (int) : Number of iteration of the tick method.
    """
    def __init__(self, iteration):
        super().__init__()

        self._iteration = iteration


    def tick(self, dt):
        """
        This function override NodeTree.tick().
        Run tick of all children in order for each iteration.
        If child return running, then return running.
        Else if return value is success, juste go to next iteration.
        On failure return failure.

        
        Parameters :
            dt (int) : Delta time.

        Return : 
            State (int) : Must be NodeTree.RUNNING, NodeTree.SUCCESS or NodeTree.FAILURE.
        """

        for i in range(self._iteration):
            status = super().get_nodes()[0].tick(dt)

            if status == NodeTree.RUNNING:
                return status

            elif status == NodeTree.FAILURE:
                return status

                
        return NodeTree.SUCCESS