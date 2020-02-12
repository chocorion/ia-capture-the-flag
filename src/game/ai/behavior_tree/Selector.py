from ai.behavior_tree import *


class Selector(NodeTree):
    '''
    Success if one node success.
    '''
    def __init__(self):
        super().__init__()

    def tick(self, dt):
        for node in super().get_nodes():
            status = node.tick(dt)

            if status == NodeTree.RUNNING:
                return NodeTree.RUNNING

            if status == NodeTree.SUCCESS:
                return NodeTree.SUCCESS

        return NodeTree.FAILURE