from ai.behavior_tree import *

class NodeTreeSingleChild(NodeTree):
    """
    This abstract class represent a node, with only one child.
    """

    def _check_if_no_child(self):
        if len(super().get_nodes()) != 0:
            raise Exception("Error, this node can't have more than one child.")

    def append_node(self, node):
        """
        Append node to the end of the node list.

        Parameters : 
            node (Node) : The node to append.
        """
        self._check_if_no_child()

        super().append_node(node)


    def insert_node(self, node, index=0):
        """
        Insert node in the node list.

        Parameters : 
            node (Node) : The node to append.
            index (int) : Index to insert node at.
        """
        self._check_if_no_child()

        super().insert_node(index, node)