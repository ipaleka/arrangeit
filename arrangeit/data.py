from arrangeit.constants import WINDOW_MODEL_TYPES, WINDOW_RECT_ELEMENTS
from arrangeit.utils import get_value_if_valid_type


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
    :var icon: window's application icon
    :type icon: :class:`PIL.Image.Image`
    :var workspace: virtual workspace the window is on (screen, number)
    :type workspace: (int, int)
    :var changed: changed window rectangle (x, y, width, height)
    :type changed: (int, int, int, int)
    :var changed_ws: changed window workspace
    :type changed_ws: int or None
    """

    wid = None
    rect = ()
    resizable = None
    title = None
    name = None
    icon = None
    workspace = None
    changed = ()
    changed_ws = None

    def __init__(self, **kwargs):
        """Calls setup with given kwargs."""
        self.setup(**kwargs)

    def setup(self, **kwargs):
        """Sets model data from provided kwargs

        or sets the value to None/() if attribute isn't provided.
        """
        for attr, typ in WINDOW_MODEL_TYPES.items():
            setattr(self, attr, get_value_if_valid_type(kwargs.get(attr), typ))

    def wh_from_ending_xy(self, x, y):
        """Returns (width, height) for model rect from provided x and y

        if provided point is greater than changed x and y (set during LOCATE phase),
        otherwise returns two-tuple of None.

        :returns: (int, int) or (None, None)
        """
        if x > self.changed[0] and y > self.changed[1]:
            return (x - self.changed[0], y - self.changed[1])
        return (None, None)

    def set_changed(self, **kwargs):
        """Creates `changed` attribute from provided arguments.

        Accepts "rect" argument, individual rect element(s) as defined by
        WINDOW_RECT_ELEMENTS or "ws" argument. If some rect part isn't provided
        then `changed`, respectively `rect` is used for valid changes or rect elements.

        Resets to () if any of provided rect arguments is invalid in regard to
        WINDOW_MODEL_TYPES for "rect". changed_ws is reset to None in such a case.

        :var index: argument's index in rect tuple
        :type index: int
        :var changed: temporary collection holding calculated values
        :type changed: list
        :var new_value: new value for rect element
        :type new_value: int
        """
        if "ws" in kwargs:
            self.changed_ws = get_value_if_valid_type(
                kwargs["ws"], WINDOW_MODEL_TYPES["workspace"]
            )
            del kwargs["ws"]
            if not kwargs:
                return None

        if "rect" in kwargs:
            self.changed = get_value_if_valid_type(
                kwargs["rect"], WINDOW_MODEL_TYPES["rect"]
            )
            return None

        changed = list(self.changed) if self.changed != () else list(self.rect)
        for elem, value in kwargs.items():
            if elem not in WINDOW_RECT_ELEMENTS:
                changed = []
                break
            index = WINDOW_RECT_ELEMENTS.index(elem)
            new_value = get_value_if_valid_type(
                value, WINDOW_MODEL_TYPES["rect"][index]
            )
            if new_value is None:
                changed = []
                break
            changed[index] = new_value

        self.changed = tuple(changed)

    @property
    def x(self):
        return self.rect[0] if self.rect is not None else None

    @property
    def y(self):
        return self.rect[1] if self.rect is not None else None

    @property
    def w(self):
        return self.rect[2] if self.rect is not None else None

    @property
    def h(self):
        return self.rect[3] if self.rect is not None else None

    @property
    def ws(self):
        return self.workspace


class WindowsCollection(object):
    """Class holding visible windows collection."""

    _members = None

    def __init__(self):
        """Initializes empty _members list."""
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

    async def get_model_by_wid(self, wid):
        """Returns window model having provided wid from collection.

        :param wid: window id (xid, hwnd, ...)
        :type wid: int
        :returns: WindowModel instance
        """
        try:
            return next(model for model in self._members if model.wid == wid)
        except StopIteration:
            return None
