from ai.behavior_tree import *

class Sequence(NodeTree):
    '''
    Success if all nodes success
    '''
    def __init__(self):
        super().__init__()

    def tick(self, dt):
        for node in super().get_nodes():
            status = node.tick(dt)

            if status == NodeTree.RUNNING:
                return NodeTree.RUNNING

            if status == NodeTree.FAILURE:
                return NodeTree.FAILURE

        return NodeTree.SUCCESS