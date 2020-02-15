from ai.behavior_tree import *

class Condition(NodeTree):
    """
    Implementation of NodeTree.
    Must have only one child, and run it if condition is valid.

    May be implemented later...
    """

    def __init__(self, condition):
        super().__init__()
        self._condition = condition
