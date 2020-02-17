from ai.behavior_tree import *

from random import shuffle

class SelectorRandom(NodeTree):
    """
    Implementation of NodeTree, this class represent a control node, the random selector.
    """
    def __init__(self):
        super().__init__()
        self._currently_running_index = -1
        self._saved_shuffle = None


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

        if self._currently_running_index != -1:
            start = self._currently_running_index
            nodes = self._saved_shuffle

            self._currently_running_index = -1
            self._saved_shuffle = None
        else:
            nodes = super().get_nodes()
            shuffle(nodes)

        for node_index in range(start, len(nodes)):
            status = nodes[node_index].tick(dt)

            if status == NodeTree.RUNNING:
                self._currently_running_index = node_index
                self._saved_shuffle = nodes

                return NodeTree.RUNNING

            if status == NodeTree.SUCCESS:
                return NodeTree.SUCCESS

        return NodeTree.FAILURE