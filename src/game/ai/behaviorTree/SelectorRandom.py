from ai.behaviorTree import *

from random import shuffle

class SelectorRandom(NodeTree):
    """
    Implementation of NodeTree, this class represent a control node, the random selector.
    """
    def __init__(self):
        super().__init__()
        self._currentlyRunningIndex = -1
        self._savedShuffle = None


    def tick(self, dt):
        """
        This function override NodeTree.tick().
        The selector run randomly the tick of all nodes until one return success.
        Then return success. If none of theme return success, then failure.
        If a node doesn't have finish it's tick, we return running.
        
        Parameters :
            dt (int) : Delta time.

        Return : 
            State (int) : Must be NodeTree.RUNNING, NodeTree.SUCCESS or NodeTree.FAILURE.
        """
        

        start = 0

        if self._currentlyRunningIndex != -1:
            start = self._currentlyRunningIndex
            nodes = self._savedShuffle

            self._currentlyRunningIndex = -1
            self._savedShuffle = None
        else:
            nodes = super().getNodes()
            shuffle(nodes)

        for nodeIndex in range(start, len(nodes)):
            status = nodes[nodeIndex].tick(dt)

            if status == NodeTree.RUNNING:
                self._currentlyRunningIndex = nodeIndex
                self._savedShuffle = nodes

                return NodeTree.RUNNING

            if status == NodeTree.SUCCESS:
                return NodeTree.SUCCESS

        return NodeTree.FAILURE