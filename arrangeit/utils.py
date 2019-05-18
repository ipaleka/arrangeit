import sys
from gettext import gettext as _
from platform import system
from importlib import import_module


def platform_path():
    """Returns lowercased string holding platform name."""
    return system().lower()


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


# TODO merge following 4 functions into one get_component(name, platform=None)
def get_app(platform=None):
    """Helper method for retrieving platform specific App class.

    :param platform: platform name
    :type platform: string
    :returns: ``App`` class from the platform specific package
    """
    return get_class("App", platform=platform)


def get_gui(platform=None):
    """Helper method for retrieving platform specific Gui class.

    :param platform: platform name
    :type platform: string
    :returns: ``Gui`` class from the platform specific package
    """
    return get_class("Gui", platform=platform)


def get_collector(platform=None):
    """Helper method for retrieving platform specific Collector class.

    :param platform: platform name
    :type platform: string
    :returns: ``Collector`` class from the platform specific package
    """
    return get_class("Collector", platform)


def get_player(platform=None):
    """Helper method for retrieving platform specific Player class.

    :param platform: platform name
    :type platform: string
    :returns: ``Player`` class from the platform specific package
    """
    return get_class("Player", platform)


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
            return None
        return (
            value
            if all(isinstance(val, typ[i]) for i, val in enumerate(value))
            else None
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
