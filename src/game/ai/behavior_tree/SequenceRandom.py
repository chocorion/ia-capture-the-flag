from ai.behavior_tree import *

from random import shuffle

class SequenceRandom(NodeTree):
    """
    Implementation of NodeTree, this class represent a control node, the random sequence.
    """
    def __init__(self):
        super().__init__()


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

        nodes = super().get_nodes()

        shuffle(nodes)
        
        for node in nodes:
            status = node.tick(dt)

            if status == NodeTree.RUNNING:
                return NodeTree.RUNNING

            if status == NodeTree.FAILURE:
                return NodeTree.FAILURE

        return NodeTree.SUCCESS