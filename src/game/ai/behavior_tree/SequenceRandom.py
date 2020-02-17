from ai.behavior_tree import *

from random import shuffle

class SequenceRandom(NodeTree):
    """
    Implementation of NodeTree, this class represent a control node, the random sequence.
    """
    def __init__(self):
        super().__init__()
        self._currently_processing_index = -1
        self._saved_shuffle = None


    def tick(self, dt):
        """
        This function override NodeTree.tick().
        The selector run the tick of all nodes randomly, until one return failure.
        If none of theme return failure, then tick return success.
        Else return failure or running if a child does't have finish computation.
        
        Parameters :
            dt (int) : Delta time.

        Return : 
            State (int) : Must be NodeTree.RUNNING, NodeTree.SUCCESS or NodeTree.FAILURE.
        """

        
        start = 0

        if self._currently_processing_index != -1:
            start = self._currently_processing_index
            nodes = self._saved_shuffle

            self._currently_processing_index = -1
            self._saved_shuffle = None
        else:
            nodes = super().get_nodes()
            shuffle(nodes)

        
        for node_index in range(start, len(nodes)):
            status = nodes[node_index].tick(dt)

            if status == NodeTree.RUNNING:
                self._currently_processing_index = node_index
                self._saved_shuffle = nodes
                return NodeTree.RUNNING

            if status == NodeTree.FAILURE:
                return NodeTree.FAILURE

        return NodeTree.SUCCESS