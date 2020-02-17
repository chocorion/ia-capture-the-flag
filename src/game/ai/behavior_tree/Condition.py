from ai.behavior_tree import *

class Condition(NodeTreeSingleChild):
    """
    Implementation of NodeTree.
    Must have only one child, and run it if condition is valid.

    Attributes:
        _condition (function()) : Function that return boolean value.
    """

    def __init__(self, condition):
        super().__init__()
        self._condition = condition

    def tick(self, dt):
        # Don't repeat condition if child was already running
        if self._currently_processing != None:
            status = self._currently_processing.tick(dt)

            if status != NodeTree.RUNNING:
                self._currently_processing = None

            return status

        if self._condition():
            status = super().get_child().tick(dt)

            if status == NodeTree.RUNNING:
                self._currently_processing = super().get_child()
            else:
                return status

        else:
            return NodeTree.FAILURE
