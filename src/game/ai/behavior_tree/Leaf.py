from ai.behavior_tree import Node

class Leaf(Node):
    def __init__(self, fun):
        super().__init__()
        self._fun = fun

    def tick(self):
        return fun()