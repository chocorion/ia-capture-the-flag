from ai.behaviorTree import *

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
        if self._currentlyProcessing != None:
            status = self._currentlyProcessing.tick(dt)

            if status != NodeTree.RUNNING:
                self._currentlyProcessing = None

            return status

        if self._condition():
            status = super().getChild().tick(dt)

            if status == NodeTree.RUNNING:
                self._currentlyProcessing = super().getChild()
            else:
                return status

        else:
            return NodeTree.FAILURE
