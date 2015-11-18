"""
Module that provides *nodes* that are used in a :class:`TreeMap`.

The :class:`TreeMapNode` is in fact a tree itself.
"""


class TreeMapNode(object):
    """
    Simple node class to represent elements in a :class:`TreeMap` structure.

    This node type allows to construct a tree with *named* nodes (or named arcs which is the same).

    See:
        :class:`TreeMap`.
    """
    def __init__(self, element=None):
        """
        Constructor.

        Args:
            element: Object to add into the node.

        """
        super(TreeMapNode, self).__init__()
        self._element = element
        self._nodes = dict()
        self._parent = None

        self._depth = -1 # a node depth of -1 is considered as an error

    ####################################################################################################################
    # Node methods
    ####################################################################################################################
    def set_parent(self, node):
        """
        Attach node to its parent.

        Args:
            node: Parent node.

        Note:
            ``node`` can be ``None``. In that case, the node is detached from its previous parent.

        """
        self._parent = node

        if node is None:
            # detach from parent
            self._depth = 0
        else:
            self._depth = node.get_depth() + 1

    def set_child_node(self, name, node):
        """
        Add one child node to this node.

        Args:
            name (str): Name of the child.
            node (TreeMapNode): Node to add.

        Warning:
            No test is done to see whether or not a node was already attached with that name. If this is the case, the
            new node takes the place of the old one that is now unreachable. See :meth:`set_unique_child_node`.
        """
        assert isinstance(node, TreeMapNode)
        self._nodes[name] = node
        node.set_parent(self)

    def set_unique_child_node(self, name, node):
        """
        Add one child node to this node.

        Args:
            name (str): Name of the child.
            node (TreeMapNode): Node to add.

        Note:
            The name must **not** be in use.
        """
        try:
            temp = self._nodes[name]
            raise RuntimeError("Name '%s' is already used for child node" % name)
        except KeyError:
            pass

        self.set_child_node(name, node)

    def get_child_node(self, name):
        """
        Retrieve child node.

        Args:
            name (str): Name of the node to retrieve.

        Warning:
            The name of the node **must** exist otherwise a ``KeyError`` is raised.
            See :meth:`get_child_node_or_default`.
        """
        return self._nodes[name]

    def get_child_node_or_default(self, name, default=None):
        """
        Retrieve child node if it exist or return a default value.

        Args:
            name (str): Name of the node to retrieve.
            default: Default value to return if no named child node is found.

        """
        try:
            return self._nodes[name]
        except KeyError:
            return default

    def get_child_nodes_names(self):
        """
        Return a list with all child names.

        """
        return self._nodes.keys()

    def get_child_nodes(self):
        """
        Return child nodes.

        """
        return self._nodes.values()

    def generate_child_nodes(self):
        """

        Yields:
        """
        for node in self._nodes:
            yield node

    def has_children(self):
        """
        Return ``True`` is node has one or more children, ``False`` otherwise.


        """
        if self._nodes:
            return True

        return False

    def generate_child_leaf_nodes(self):
        """
        Generate leaf nodes of this node.

        """

        def _yield_child_leaf_nodes(node):
            """

            Args:
                node:

            Yields:
            """
            if not node.has_children():
                yield node
            else:
                for child_node in node.generate_child_nodes():
                    # recursivity is not compatible with yield in Python2.x: you have to re-yield results
                    for child in _yield_child_leaf_nodes(child_node):
                        yield child

        return _yield_child_leaf_nodes(self)

    def detach_children(self):
        """
        Erase references to children without deleting them.

        These children might be used somewhere else, otherwise they will be taken care by ``Python``'s garbage collector.
        """
        for node in self.get_child_nodes():
            node.set_parent(None)
        self._nodes = dict()

    def get_depth(self):
        """
        Returns depth of node in the :class:`TreeMap` object.
        """
        return self._depth

    ####################################################################################################################
    # Element methods
    ####################################################################################################################
    def set_element(self, element):
        """
        Attach the element of this node.

        Args:
            element: Object to contain in this node.

        Note:
            Only one element can be set/attached to a node.
        """
        self._element = element

    def get_element(self):
        """
        Retrieve the element of this node.

        """
        return self._element

    def has_element(self):
        """
        Detect if an element has been attached to this node.
        """
        return self._element is not None

    def nbr_children(self):
        """
        Return the number of children if any.

        """
        return len(self._nodes)

    def delete_element(self):
        """
        Delete element.

        Note:
            To simply detach the element (without erasing it) from this node, call ``set_element(None)``.
        """
        del self._element
        self._element = None

    ###
    # Debug methods
    ###
    def _children_to_string(self, level, string_lst):
        """

        Args:
            level:
            string_lst:
        """
        for (node_link, node) in self._nodes.items():
            string_lst.append("%s%s:" % (' ' * level, node_link))
            node._children_to_string(level+2, string_lst)

    def children_to_string(self, level=0):
        """

        Args:
            level:

        Returns:
        """
        strings = list()
        self._children_to_string(level, strings)

        return '\n'.join(strings)


class RootTreeMapNode(TreeMapNode):
    """
    A :class:`TreeMapNode` to represent a root node in a :class:`TreeMap` tree.

    This node is a dummy node. It allows to have :class:`TreeMap` trees behave like forests.


    """
    def __init__(self, element=None):
        """
        Constructor.

        Args:
            element: object to attach to this root.
        """
        super(RootTreeMapNode, self).__init__(element)

        self._depth = 0