class Graph:

    def __init__(self, listNodes, listEdges, data):
        self._listNodes = listNodes 
        self._listEdges = listEdges
        # Not implemented yet, must determine which data we give to the graph
        self._data      = data 
        raise NotImplementedError
    
    def buildGraph(self):
        raise NotImplementedError
    
    # The idea would be to store the graph in a dict, to further access
    def storeGraph(self):
        raise NotImplementedError

    def getListNodes(self):
        raise NotImplementedError

    def getListEdges(self):
        raise NotImplementedError

