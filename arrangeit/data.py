class WindowModel(object):
    """Class holding window data.

    :var wid: window id (xid, hwnd, ...)
    :type wid: int
    :var rect: window rectangle (x, y, width, height)
    :type rect: (int, int, int, int)
    :var WindowModel.resizable: is window resizable or not
    :type WindowModel.resizable: Boolean
    :var title: window title/caption
    :type title: string
    :var name: window's application name
    :type name: string
    """

    wid = None
    rect = None
    resizable = None
    title = None
    name = None
    # ws = None  # workspace

    def __init__(self, **kwargs):
        """Calls setup with given kwargs."""
        self.setup(**kwargs)

    def setup(self, **kwargs):
        """Sets model data from provided kwargs

        or sets the value to None if attribute isn't provided.
        """
        self.wid = kwargs.get("wid", None)
        self.rect = kwargs.get("rect", None)
        self.resizable = kwargs.get("resizable", None)
        self.title = kwargs.get("title", None)
        self.name = kwargs.get("name", None)


class WindowsCollection(object):
    """Class holding visible windows collection."""

    _members = None

    def __init__(self):
        """Initializec empty _members list."""
        self._members = []

    @property
    def size(self):
        """Returns the size of _members list."""
        return len(self._members)

    def clear(self):
        """Empties the _members list."""
        self._members.clear()

    def add(self, instance):
        """Adds given instance to _members list.

        Raises ValueError if given ``instance`` isn't a WindowModel instance.

        :param instance: window data
        :type instance: WindowModel instance
        """
        if not isinstance(instance, WindowModel):
            raise ValueError("accepting only WindowModel instance")
        self._members.append(instance)

    def generator(self):
        """Yields the next member from ``_members``.

        Raises ValueError if given ``instance`` isn't a WindowModel instance.
        :returns: WindowModel instance
        """
        for member in self._members:
            yield member
