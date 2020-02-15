from abc import (ABCMeta, abstractmethod)

import copy

class NodeTree(metaclass=ABCMeta):
    """
    This is a basic class for representing nodes in behavior tree.

    Attributes:
        _nodes (Node) : List of children.
        _currently_processing (Node): As a node can take many tick to processing task,
            node store the currently processing node. It's faster than looking in all
            the tree for the active node.

    Enumeration:
        RUNNING : Node must return NodeTree.RUNNING if computation is not finish.
        SUCCESS : Node must return NodeTree.SUCCESS on success.
        FAILURE : Node must return NodeTree.FAILURE on failuer.
    """
    
    RUNNING = 0
    SUCCESS = 1
    FAILURE = 2
    
    def __init__(self):
        self._nodes = list()
        self._currently_processing = None

    @abstractmethod
    def tick(self, dt):
        """
        Core method of the node, called for processing the behavior tree.

        Parameters :
            dt (int) : Delta time, used by function in leaf for time management.

        Return : 
            State (int) : Must be NodeTree.RUNNING, NodeTree.SUCCESS or NodeTree.FAILURE.
        """
        ...


    def append_node(self, node):
        """
        Append node to the end of the node list.

        Parameters : 
            node (Node) : The node to append.
        """

        self._nodes.append(node)


    def insert_node(self, node, index=0):
        """
        Insert node in the node list.

        Parameters : 
            node (Node) : The node to append.
            index (int) : Index to insert node at.
        """

        self._nodes.insert(index, node)


    def get_nodes(self):
        """
        Return the list of all direct child of the node.
        """

        return copy.copy(self._nodes)