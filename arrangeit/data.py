# arrangeit - cross-platform desktop utility for easy windows management
# Copyright (C) 1999-2019 Ivica Paleka

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from operator import attrgetter

from arrangeit.settings import Settings
from arrangeit.utils import get_value_if_valid_type


class WindowModel(object):
    """Class holding window data.

    :var WindowModel.wid: window id (xid, hwnd, ...)
    :type WindowModel.wid: int
    :var rect: window rectangle (x, y, width, height)
    :type rect: (int, int, int, int)
    :var WindowModel.resizable: is window resizable or not
    :type WindowModel.resizable: Boolean
    :var WindowModel.restored: is window restored or minimized
    :type WindowModel.restored: Boolean
    :var WindowModel.title: window title/caption
    :type WindowModel.title: string
    :var WindowModel.name: window's application name
    :type WindowModel.name: string
    :var WindowModel.icon: window's application icon
    :type WindowModel.icon: :class:`PIL.Image.Image`
    :var workspace: virtual workspace the window is on in format 1000 * screen + number
    :type workspace: int
    :var changed: changed window rectangle (x, y, width, height)
    :type changed: () or (int, int, int, int)
    :var changed_ws: changed window workspace
    :type changed_ws: None or int
    """

    wid = None
    rect = ()
    resizable = None
    restored = None
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
        for attr, typ in Settings.WINDOW_MODEL_TYPES.items():
            setattr(self, attr, get_value_if_valid_type(kwargs.get(attr), typ))

    def set_changed(self, **kwargs):
        """Creates ``changed`` attribute from provided arguments.

        Accepts "rect" argument, individual rect element(s) as defined by
        Settings.WINDOW_MODEL_RECT_ELEMENTS or "ws" argument. If some rect part isn't provided
        then ``changed``, respectively ``rect`` is used for valid changes or rect elements.

        Resets to () if any of provided rect arguments is invalid in regard to
        Settings.WINDOW_MODEL_TYPES for "rect". changed_ws is reset to None in such a case.

        NOTE this method needs refactoring

        :var index: argument's index in rect tuple
        :type index: int
        :var changed: temporary collection holding calculated values
        :type changed: list
        :var new_value: new value for rect element
        :type new_value: int
        """
        if "ws" in kwargs:
            self.changed_ws = get_value_if_valid_type(
                kwargs["ws"], Settings.WINDOW_MODEL_TYPES["workspace"]
            )
            del kwargs["ws"]
            if not kwargs:
                return None

        previous = list(self.changed) if self.changed != () else list(self.rect)
        if "rect" in kwargs:
            changed = get_value_if_valid_type(
                kwargs["rect"], Settings.WINDOW_MODEL_TYPES["rect"]
            )
            if changed != tuple(previous):
                self.changed = changed
            return None

        changed = []
        for elem, value in kwargs.items():
            if elem not in Settings.WINDOW_MODEL_RECT_ELEMENTS:
                changed = []
                break
            index = Settings.WINDOW_MODEL_RECT_ELEMENTS.index(elem)
            new_value = get_value_if_valid_type(
                value, Settings.WINDOW_MODEL_TYPES["rect"][index]
            )
            if new_value is None:
                changed = []
                break
            if new_value != previous[index]:
                changed = previous
                changed[index] = new_value

        self.changed = tuple(changed)

    def clear_changed(self):
        """Resets changing related attributes to initial empty values."""
        self.changed = ()
        self.changed_ws = None

    @property
    def is_changed(self):
        """Checks if model rect has been changed.

        :returns: Boolean
        """
        return self.changed != () and self.changed != self.rect

    @property
    def is_ws_changed(self):
        """Checks if workspace has been changed.

        :returns: Boolean
        """
        return self.changed_ws is not None and self.changed_ws != self.ws

    @property
    def changed_x(self):
        return (
            self.changed[0]
            if self.changed != ()
            else (self.rect[0] if self.rect != () else None)
        )

    @property
    def changed_y(self):
        return (
            self.changed[1]
            if self.changed != ()
            else (self.rect[1] if self.rect != () else None)
        )

    @property
    def changed_w(self):
        return (
            self.changed[2]
            if self.changed != ()
            else (self.rect[2] if self.rect != () else None)
        )

    @property
    def changed_h(self):
        return (
            self.changed[3]
            if self.changed != ()
            else (self.rect[3] if self.rect != () else None)
        )

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
        """Shorter alias for workspace attribute."""
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

    def sort(self):
        """Sorts collection for presentation queue.

        First model stays first and the others are sorted by their workspace first
        and then on current position. <starts from workspace number 0 when all
        the windows from greater workspaces numbers are exhausted.

        :var others: sorted list without first element
        :type others: list
        :var index: index of first element having greater or equal workspace like first
        :type index: int
        """
        others = sorted(self._members[1:], key=attrgetter("ws"))
        index = next(
            (i for i, model in enumerate(others) if model.ws >= self._members[0].ws), 0
        )
        self._members = self._members[:1] + others[index:] + others[:index]

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

    def get_windows_list(self):
        """Prepares and returns list of windows ids, titles and icons.

        :returns: [(int, str, :class:`PIL.Image.Image`)]
        """
        return [
            (model.wid, model.title, model.icon) for model in list(self.generator())
        ]

    def get_model_by_wid(self, wid):
        """Returns window model having provided wid from collection.

        :param wid: window id (xid, hwnd, ...)
        :type wid: int
        :returns: WindowModel instance
        """
        try:
            return next(model for model in self._members if model.wid == wid)
        except StopIteration:
            return None

    def repopulate_for_wid(self, wid, remove_before):
        """Repopulates collection starting from the window with identifier ``wid``

        without including models placed before provided ``remove_before``.

        :param wid: window id (xid, hwnd, ...)
        :type wid: int
        :param remove_before: window id (xid, hwnd, ...)
        :type wid: int
        :var start_index: index of model that is going to become the first
        :type start_index: int
        :var remove_index: index of first model that is not going to be removed
        :type remove_index: int
        """
        start_index = next(
            i for i, model in enumerate(self._members) if model.wid == wid
        )
        remove_index = next(
            i for i, model in enumerate(self._members) if model.wid == remove_before
        )
        self._members = (
            self._members[start_index:] + self._members[remove_index:start_index]
        )

    def export(self):
        """Prepares for saving useful data from collection."""
        return [
            (
                model.changed or model.rect,
                model.resizable,
                model.restored,
                model.title,
                model.name,
                model.changed_ws or model.ws,
            )
            for model in self._members
        ]
