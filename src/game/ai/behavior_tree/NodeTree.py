class NodeTree:

    RUNNING = 0
    SUCCESS = 1
    FAILURE = 2
    
    def __init__(self):
        self._nodes = list()

    def tick(self, dt):
        pass

    def append_node(self, node):
        '''
        Append node to the end of the node list.
        '''

        self._nodes.append(node)

    def insert_node(self, node, index=0):
        '''
        Insert node in the node list at index.
        '''

        self._nodes.insert(index, node)

    def get_nodes(self):
        return self._nodes