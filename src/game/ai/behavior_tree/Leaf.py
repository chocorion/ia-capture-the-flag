from ai.behavior_tree import *

class Leaf(NodeTree):
    def __init__(self, fun):
        super().__init__()
        self._fun = fun

    def tick(self, dt):
        return self._fun(dt)