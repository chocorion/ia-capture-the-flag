from ai.behaviorTree import *


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
        if self._currentlyProcessing != None:
            status = self._currentlyProcessing.tick(dt)

            if status != NodeTree.RUNNING:
                self._currentlyProcessing = None

            if status != NodeTree.SUCCESS:
                return status
                
            start = self._currentStart + 1


        for i in range(start, self._iteration):
            status = super().getChild().tick(dt)

            if status == NodeTree.RUNNING:
                self._currentlyProcessing = super().getChild()
                self._currentStart = i
                return status

            elif status == NodeTree.FAILURE:
                return status

                
        return NodeTree.SUCCESS