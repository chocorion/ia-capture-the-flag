from ai.behaviorTree import *

class NodeTreeSingleChild(NodeTree):
    """
    This abstract class represent a node, with only one child.
    """

    def _checkIfNoChild(self):
        if len(super().getNodes()) != 0:
            raise Exception("Error, this node can't have more than one child.")

    def appendNode(self, node):
        """
        Append node to the end of the node list.

        Parameters : 
            node (Node) : The node to append.
        """
        self._checkIfNoChild()

        super().appendNode(node)


    def insert_node(self, node, index=0):
        """
        Insert node in the node list.

        Parameters : 
            node (Node) : The node to append.
            index (int) : Index to insert node at.
        """
        self._checkIfNoChild()

        super().insert_node(index, node)

    
    def getChild(self):
        """
        Return the only child node.
        """
        return super().getNodes()[0]