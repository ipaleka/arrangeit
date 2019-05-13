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

    :param name: string
    :param platform: string or None
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


def get_app(platform=None):
    """Helper method for retrieving platform specific App class.

    :param platform: string or None
    :returns: **App** class from the platform specific package
    """
    return get_class("App", platform=platform)


def get_collector(platform=None):
    """Helper method for retrieving platform specific Collector class.

    :param platform: string
    :returns: **Collector** class from the platform specific package
    """
    return get_class("Collector", platform)


def get_player(platform=None):
    """Helper method for retrieving platform specific Player class.

    :param platform: string
    :returns: **Player** class from the platform specific package
    """
    return get_class("Player", platform)
