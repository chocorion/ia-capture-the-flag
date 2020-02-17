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
        start = 0
        if self._currently_processing != None:
            status = self._currently_processing.tick(dt)

            if status != NodeTree.RUNNING:
                self._currently_processing = None

            if status != NodeTree.SUCCESS:
                return status
                
            start = self._current_start + 1


        for i in range(start, self._iteration):
            status = super().get_child().tick(dt)

            if status == NodeTree.RUNNING:
                self._currently_processing = super().get_child()
                self._current_start = i
                return status

            elif status == NodeTree.FAILURE:
                return status

                
        return NodeTree.SUCCESS