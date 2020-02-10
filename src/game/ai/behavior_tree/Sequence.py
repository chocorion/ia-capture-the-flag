from ai.behavior_tree import Node

class Sequence(Node):
    '''
    Success if all nodes success
    '''
    def __init__(self):
        super().__init__()

    def tick(self):
        for node in super()._nodes:
            status = node.tick()

            if status == Node.RUNNING:
                return Node.RUNNING

            if status == Node.FAILURE:
                return Node.FAILURE

        return Node.SUCCESS