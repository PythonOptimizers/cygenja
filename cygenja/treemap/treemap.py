from cygenja.treemap.treemap_node import RootTreeMapNode, TreeMapNode
from cygenja.treemap.location_descriptor import LocationDescriptor


class TreeMap(object):
    """
    *TreeDict* (or *TreeMap*)-like data structure but with each node containing an element.
    
    Nodes are accessed/created by a :class:`LocationDescriptor` (or a corresponding string) containing the **whole**
    path to the node.
    
    Linking nodes are created on the fly if needed.
    """
    def __init__(self):
        """
        Constructor.

        """
        super(TreeMap, self).__init__()
        # dummy root node
        self._root_node = RootTreeMapNode()

        self._nbr_of_nodes = 0

    def clear(self):
        """
        Clear the structure but without deleting anything.
        
        Some nodes/elements might be used somewhere else. We simply detach node references from the dummy root node.
        """
        self._root_node.detach_children()
        self._nbr_of_nodes = 0

    ####################################################################################################################
    # Basic info about the tree
    ####################################################################################################################
    def nbr_of_nodes(self):
        """
        Return the number of nodes in the tree.

        Warning:
            Nodes can be detached without the tree knowing it. As long as you only use the methods defined in a
            :class:`TreeMap`, this number reflects exactly the number of nodes in the tree.
        """
        return self._nbr_of_nodes

    def is_empty(self):
        """
        Test if tree is empty or not.

        """
        # nodes can be detached without the tree knowing it...
        return self._root_node.nbr_children() == 0

    ####################################################################################################################
    # Internal node management
    ####################################################################################################################
    def _get_location_descriptor(self, location):
        """
        Get corresponding :class:`LocationDescriptor` object from a string or a :class:`LocationDescriptor` itself.
        
        Args:
            location: a string or a :class:`LocationDescriptor`.
        
        Returns:
            A corresponding :class:`LocationDescriptor` object. If ``location`` is a :class:`LocationDescriptor`,
            we simply return it.
        
        Raises:
            A ``RuntimeError`` is raised whenever the `location` object is not recognized a string or :class:`self._nbr_of_nodes`.
        """
        loc_descriptor = None
        if isinstance(location, basestring):
            loc_descriptor = LocationDescriptor(location)
        elif isinstance(location, LocationDescriptor):
            loc_descriptor = location
        else:
            raise RuntimeError("Argument is neither a string nor a self._nbr_of_nodes")

        return loc_descriptor

    def _get_node(self, loc_descriptor, create_non_existing_nodes=False):
        """
        Get node corresponding to last location in a :class:`LocationDescriptor` object.
        
        Args:
            loc_descriptor: A  :class:`LocationDescriptor` object
            create_non_existing_nodes (bool): Do we create non existing nodes along the way (including last node)?
        
        Raises:
            RuntimeError if a node along the path given in by the :class:`LocationDescriptor` object does not exist
            **if** ``create_non_existing_nodes`` is set to ``False``.
        
        """
        node = self._root_node

        for location in loc_descriptor.generate_all_sub_locations():
            child = node.get_child_node_or_default(location, None)
            if child is None:
                if not create_non_existing_nodes:
                    raise RuntimeError("Node at location '%s' in '%s' does not exist!" % (location, loc_descriptor.to_string()))
                else:
                    # create empty node
                    child = TreeMapNode(None)
                    node.set_child_node(location, child)
                    self._nbr_of_nodes += 1
            node = child

        return node

    def _create_entry(self, location, element, unique=True, delete_element=False):
        """
        Create an entry located at ``location``.
        
        Args:
            location: String or :class:`LocationDescriptor` to describe a "separator location" (i.e. dir1/dir2/dir3 for
                instance).
            element: Element to store at the location.
            unique: ``True`` means that the element to store **must** be unique and that the corresponding node doesn't already exist.
            delete_element: In case the element must not be unique, delete or not the existing element at
                the ``location`` if it exist?
        
        Returns:
            The created node with the element.
            
        Raises:
            A ``RuntimeError`` is raised if leaf node already exists and ``unique`` is set to ``True``.

        Note:
            Non existing linking node (i.e. non leaf nodes) are created on the fly.
        """
        loc_descriptor = self._get_location_descriptor(location)

        # find parent node
        parent_node = self._root_node
        if loc_descriptor.nbr_of_sub_locations() > 1:
            parent_node = self._get_node(loc_descriptor.get_sub_location_descriptor(), create_non_existing_nodes=True)

        # find child node if it exist
        last_location = loc_descriptor.last_sub_location()
        child_node = parent_node.get_child_node_or_default(last_location, None)
        if child_node is None:
            # create node
            child_node = TreeMapNode(element)
            parent_node.set_child_node(last_location, child_node)
            self._nbr_of_nodes += 1
        else:
            # child node exist
            if unique:
                raise RuntimeError("Node corresponding to the location '%s' already exist!" % loc_descriptor.to_string())
            elif delete_element:
                child_node.delete_element()
            child_node.set_element(element)

        return child_node

    def _get_dummy_root(self):
        """

        Returns:
        """
        return self._root_node

    def _has_node(self, location):
        """

        Args:
            location:

        Returns:
        """
        loc_descriptor = self._get_location_descriptor(location)
        # find node
        node = None
        try:
            node = self._get_node(loc_descriptor)
        except RuntimeError as e:
            pass

        return node is not None

    ####################################################################################################################
    # Element management
    ####################################################################################################################
    def add_unique_element(self, location, element):
        """
        Create an entry located at ``location``.
        
        Args:
            location: String or :class:`LocationDescriptor` to describe a "separator location" (i.e. dir1/dir2/dir3 for
                instance).
            element: Element to store.
        
        Returns:
            The created node with the element.

        Notes:
            The different sub locations entries **must** exist and the last one **MUST NOT** already exist.
            Use the more loose :meth:`add_element` method if needed.
        """
        return self._create_entry(location, element, unique=True)

    def add_element(self, location, element, delete_elem=False):
        """
        Create an entry located at ``location``.
        
        Args:
            location: String or :class:`LocationDescriptor` to describe a "separator location" (i.e. dir1/dir2/dir3 for
                instance).
            element: Element to store.
            delete_elem: Delete old element or not if it exist?
        
        Returns:
            The created node with the element.
            
        Notes:
            The different sub locations entries **must** exist and the last may or may not already exist.
            Use the more strict :meth:`add_unique_element` method if needed.
            
            You don't need to have a common root node. We internally use a dummy root node.
        """
        return self._create_entry(location, element, unique=False, delete_element=delete_elem)

    def retrieve_element(self, location):
        """
        
        Args:
            location:
        
        Returns:
        """
        loc_descriptor = self._get_location_descriptor(location)
        # find node
        node = self._get_node(loc_descriptor)
        return node.get_element()

    def retrieve_element_or_default(self, location, default=None):
        """
        
        Args:
            location:
            default: 
        
        Returns:
        """
        loc_descriptor = self._get_location_descriptor(location)
        # find node
        node = None
        try:
            node = self._get_node(loc_descriptor)
        except Exception as e:
            return default

        return node.get_element()

    ####################################################################################################################
    # DEBUG
    ####################################################################################################################
    def to_string(self):
        """
        
        Returns:
        """
        return self._root_node.children_to_string(0)

