from ai.behavior_tree import *


class RepeaterUntilFail(NodeTreeSingleChild):
    """
    Implementation of NodeTree, this class represent a control node, the repeater.
    Must have only on child.
    """

    def __init__(self):
        super().__init__()


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

        while True:
            status = super().get_child().tick(dt)

            if status == NodeTree.RUNNING:
                return status

            elif status == NodeTree.SUCCESS:
                return NodeTree.RUNNING

            else:
                # On child failure return success.
                return NodeTree.SUCCESS