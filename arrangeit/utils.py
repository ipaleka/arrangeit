import sys
from gettext import gettext as _
from platform import system
from importlib import import_module


def platform_path():
    """Returns lowercased string holding platform name."""
    return system().lower()


def platform_user_data_path():
    """Retrieves platform specific user data directory path."""
    module = import_module("arrangeit.{}.utils".format(platform_path()))
    return getattr(module, "user_data_path")()


def get_class(name, platform):
    """Helper method for retrieving platform specific class instance

    for given ``name`` and ``platform``.

    If provided ``platform`` is None then we use :func:`platform_path`.

    If class can't be imported that means host system
    isn't implemented (yet...) and so we sys.exit with a message.

    :param name: function name suffix
    :type name: string
    :param platform: platform name
    :type platform: string or None
    :returns: class instance from the platform specific package
    """
    try:
        module = import_module(
            "arrangeit.{}.{}".format(
                platform if platform is not None else platform_path(), name.lower()
            )
        )
    except ImportError:
        sys.exit(_("arrangeit can't run on your platform. :("))
    return getattr(module, name)


def get_component_class(name, platform=None):
    """Helper method for retrieving platform specific App class.

    :param platform: platform name
    :type platform: string
    :returns: class with provided `name` from the platform specific package
    """
    return get_class(name, platform=platform)


def get_value_if_valid_type(value, typ):
    """Returns provided value if it's of provided type

    or returns None if it's not. If value is None then None is returned.
    If provided value and typ are collections then each element is checked.

    :param value: value to check for type
    :type value: Python type
    :param typ: type to check on ``value``
    :type typ: Python type
    :returns: value or None
    """
    if isinstance(value, (tuple, list)):
        if not isinstance(typ, (tuple, list)) or len(value) != len(typ):
            return ()
        return (
            value if all(isinstance(val, typ[i]) for i, val in enumerate(value)) else ()
        )
    return value if isinstance(value, typ) else None


def append_to_collection(element, collection):
    """Simple helper function to append provided elem to provided collection.

    This function is used as callback argument for win32gui.EnumWindows
    and it requires True to be returned.

    :param element: element to add
    :type element: int
    :param collection: collection to add element to
    :type collection: list
    :returns: True
    """
    collection.append(element)
    return True


def quarter_by_smaller(width, height):
    """Helper method for retrieving one-forth for given ``width`` and ``height``

    with aspect ratio of 16:9.

    Starting point for calculation is the smaller value - the presumption
    is that monitors could be stacked in left-to-right **or** top-to-bottom manner.

    :param width: total desktop area width
    :type width: int
    :param height: total desktop area height
    :type height: int
    :returns: (int, int)
    """
    if width > height:
        return (int((height / 4) * 16 / 9), height // 4)
    return (width // 4, int((width / 4) * 9 / 16))


def increased_by_fraction(value, fraction):
    """Helper method for increasing provided value by provided fraction.

    :param value: value to increase
    :type value: int
    :param fraction: fraction of a whole to increase value by
    :type fraction: float
    :returns: int
    """
    return round(value * (1.0 + fraction))


def get_snapping_rects_for_rect(rect, snap):
    """Returns four snapping rectangles created from provided rect.

    Snapping rectangle is created around window connected edge points pair with
    height (or width) of 2*SNAP_PIXELS and width (or height) of related window side.

    :param rect: window rectangle (x, y, width, height)
    :type rect: (int, int, int, int)
    :param snap: snapping distance in pixels
    :type snap: int
    :returns: four-tuple of (x, y, width, height)
    """
    x, y, w, h = rect
    return (
        (x - snap, y - snap, w + 2 * snap, 2 * snap),
        (x + w - snap, y - snap, 2 * snap, h + 2 * snap),
        (x - snap, y + h - snap, w + 2 * snap, 2 * snap),
        (x - snap, y - snap, 2 * snap, h + 2 * snap),
    )

