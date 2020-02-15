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
        if self._condition():
            return super().get_child().tick(dt)
        else:
            return NodeTree.FAILURE
