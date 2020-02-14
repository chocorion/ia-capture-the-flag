class Edge:
    
    def __init__(self, node1, node2):
        self._node1 = node1
        self._node2 = node2
        raise NotImplementedError

    def getNodes(self):
        return self._node1, self._node2
        