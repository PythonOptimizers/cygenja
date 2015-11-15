import os


class LocationDescriptor(object):
    """
    Class to locate object in a :class:`TreeMap`.

    A location descriptor `dir1/dir2/dir3` can be used with a :class:`TreeMap` dict-like object like this:

    >>>d = TreeMap()
    >>>l = LocationDescriptor('dir1/dir2/dir3')
    >>>d.add_element(l, 44)

    A path of 3 nodes is created in the :class:`TreeMap` object `d`.

    ``dir1``, ``dir2`` and ``dir3`` are considered as (sub) *locations*. ``dir1/dir2/dir3`` is also considered as a *location*.
    """
    def __init__(self, locations=None, separation_char=os.sep):
        """
        Constructor.

        Args:
            locations: Can be either a string with sub-strings joined by the separation character or a list of strings,
                each giving a location.
            separation_char: Separation character in the location string.

        Raises:
            TypeError: if argument is not recognized as either a string, a list of strings or ``None``.

        Notes:
            Empty :class:`LocationDescriptor`s **are** allowed and empty locations are also allowed.
        """
        super(LocationDescriptor, self).__init__()

        self._separation_char = separation_char

        # type tests
        if isinstance(locations, list):
            self._locations_list = list(locations)
        elif isinstance(locations, str) or isinstance(locations, unicode):
            self._locations_list = locations.split(self._separation_char)
        elif locations is None:
            self._locations_list = list()
        else:
            raise TypeError("Argument in constructor not recognized.")

    def nbr_of_sub_locations(self):
        """
        Return number of sub-locations.
        """
        # TODO: keep the number of sub locations instead of calling costly len function?
        return len(self._locations_list)

    def is_empty(self):
        """
        Test if locator is emtpy.

        """
        return self.nbr_of_sub_locations() == 0

    def push_location(self, location):
        """
        Push sub location into the stack of locations.

        Args:
            location (str): New location to add.
        """
        self._locations_list.append(location)

    def pop_location(self):
        """
        Pop (last) sub location and return it.
        """
        return self._locations_list.pop()

    def generate_all_sub_locations(self):
        """
        Generate all sub locations one by one.

        Yields:
            sublocation (str): one of the sub locations.
        """
        for i in range(self.nbr_of_sub_locations()):
            yield self._locations_list[i]

    def generate_all_but_last_sub_locations(self):
        """
        Generate all but last sub locations one by one.

        Yields:
            sublocation (str): one of the sub locations.
        """
        for i in range(self.nbr_of_sub_locations()-1):
            yield self._locations_list[i]

    def generate_cumulative_all_sub_locations(self):
        """
        Generate all sub-locations but in a cumulative way.

        If ``location == loc1.loc2.loc3``, then this generator will yield:

        loc1
        loc1.loc2
        loc1.loc2.loc3

        Yields:
        """

        for index in range(self.nbr_of_sub_locations()):
            yield self.get_sub_location_descriptor(0, index+1)

    def last_sub_location(self):
        """

        Returns:
        """
        return self._locations_list[-1]

    def sub_location(self, nbr):
        """
        Return a given sub location, 0-based.

        Args:
            nbr:

        Returns:
        """
        assert nbr > -1, "Sub location number must be greater or equal to 0!"
        assert nbr < self.nbr_of_sub_locations() - 1, "Sub location number must be lower than %d!" % self.nbr_of_sub_locations() - 1
        return self._locations_list[nbr]

    def get_locations_list(self, lower_bound=0, upper_bound=None):
        """
        Return the internal location list.

        Args:
            lower_bound:
            upper_bound:

        Returns:
        """
        real_upper_bound = upper_bound
        if upper_bound is None:
            real_upper_bound = self.nbr_of_sub_locations()

        try:
            return self._locations_list[lower_bound:real_upper_bound]
        except:
            return list()

    def get_sub_location_descriptor(self, lower_bound=0, upper_bound=-1):
        """
        Return a :class:`LocationDescriptor` object with a sub location.

        We follow ``Python``'s range convention.

        Args:
            lower_bound: Idem. The location corresponding to this index is **not** included.
            upper_bound: An integer index (0-based) following ``Python`` convention for list.

        Returns:
            A sub :class:``LocationDescriptor`` object corresponding to the bounds. If the given location bounds are
            invalid, returns ``None``.

        Notes:
            By default, returns the sub location descriptor without the last location.
        """
        try:
            return LocationDescriptor(self._locations_list[lower_bound:upper_bound])
        except:
            return None

    def clone(self):
        """
        Clone object.

        Returns:
            A deepcopy of the object.
        """
        return LocationDescriptor(self._locations_list)

    def __add__(self, other):
        """
        Create a **new** :class:`LocationDescriptor` object that is the sum of this one and another.

        Args:
            self: This :class:`LocationDescriptor` object.
            other: Another :class:`LocationDescriptor` object.

        Returns:
            Sum of both :class:`LocationDescriptor` objects.
        """
        # sanity tests
        assert isinstance(other, LocationDescriptor), "You can only add LocationDescriptor together."
        assert self._separation_char == other._separation_char, \
            "You can only add LocationDescriptor together if they share the same separator character."
        new_location_string_list = self.get_locations_list() + other.get_locations_list()
        return LocationDescriptor(new_location_string_list)

    def __iadd__(self, other):
        """
        **Extend** an existing :class:`LocationDescriptor` object by another.

        Args:
            self: This :class:`LocationDescriptor` object.
            other: Another :class:`LocationDescriptor` object.

        Returns:
            The updated :class:`LocationDescriptor` object itself.
        """
        # sanity tests
        assert isinstance(other, LocationDescriptor), "You can only add LocationDescriptor together."
        assert self._separation_char == other._separation_char, \
            "You can only add LocationDescriptor together if they share the same separator character."
        self._locations_list.extend(other._locations_list)

        return self

    def __eq__(self, other):
        """
        Detect if another object is equal to this :class:`LocationDescriptor` object.

        Args:
            other: object to test.

        """
        if not isinstance(other, LocationDescriptor):
            return False

        nbr_of_sub_locations = self.nbr_of_sub_locations()

        if nbr_of_sub_locations != other.nbr_of_sub_locations():
            return False

        for i in range(nbr_of_sub_locations):
            if self._locations_list[i] != other._locations_list[i]:
                return False

        return True

    def to_string(self, other_separation_char=None):
        """
        String representation of :class:`LocationDescriptor` object.

        Args:
            other_separation_char: If needed, another separator character can be used.

        Returns:
        """
        separation_char = self._separation_char
        if other_separation_char is not None:
            separation_char = other_separation_char
        return separation_char.join(self._locations_list)

    def __str__(self):
        return self.to_string()