from ai.behaviorTree import *

class Sequence(NodeTree):
    """
    Implementation of NodeTree, this class represent a control node, the sequence.
    """
    def __init__(self):
        super().__init__()
        self._currentlyProcessingIndex = -1


    def tick(self, dt):
        """
        This function override NodeTree.tick().
        The selector run the tick of all nodes until one return failure.
        If none of theme return failure, then tick return success.
        Else return failure or running if a child does't have finish computation.
        
        Parameters :
            dt (int) : Delta time.

        Return : 
            State (int) : Must be NodeTree.RUNNING, NodeTree.SUCCESS or NodeTree.FAILURE.
        """
        nodes = super().getNodes()
        start = 0

        if self._currentlyProcessingIndex != -1:
            start = self._currentlyProcessingIndex
            self._currentlyProcessingIndex = -1

        for nodeIndex in range(start, len(nodes)):
            status = nodes[nodeIndex].tick(dt)

            if status == NodeTree.RUNNING:
                self._currentlyProcessingIndex = nodeIndex
                return NodeTree.RUNNING

            if status == NodeTree.FAILURE:
                return NodeTree.FAILURE

        return NodeTree.SUCCESS