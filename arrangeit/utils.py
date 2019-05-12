import sys
from gettext import gettext as _
from platform import system
from importlib import import_module


def platform_path():
    """Returns lowercased string holding platform name."""
    return system().lower()


def get_collector(platform=platform_path()):
    """Helper method for retrieving platform specific Collector class.

    The platform argument gets its default value on module import
    from the `platform_path`.

    If Collector class can't be imported that means host system
    isn't implemented (yet...) and so we sys.exit with a message.

    :param platform: string or default platform_path callable
    :returns: :class:`Collector` from the platform specific package
    :raises NotImplementedError: raises if platform isn't recognized
    """
    try:
        collector = import_module("arrangeit.{}.collector".format(platform))
    except ImportError:
        sys.exit(_("arrangeit doesn't work on your platform. :("))
    return collector.Collector


def get_player(platform=platform_path()):
    """Helper method for retrieving platform specific Player class.

    The platform argument gets its default value on module import
    from the `platform_path`.

    If Player class can't be imported that means host system
    isn't implemented (yet...) and so we sys.exit with a message.

    :param platform: string or default platform_path callable
    :returns: :class:`Player` from the platform specific package
    """
    try:
        player = import_module("arrangeit.{}.player".format(platform))
    except ImportError:
        sys.exit(_("arrangeit doesn't work on your platform. :("))
    return player.Player