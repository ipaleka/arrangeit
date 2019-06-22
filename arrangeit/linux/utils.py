import os

from arrangeit import __appname__


def user_data_path():
    """Returns GNU/Linux platform specific path for saving user's data.

    It first try with .local/share in user home directory, and if there's
    no such directory returns .arrangeit directory in user home directory.

    :returns: str path
    """
    local = os.path.join("~", ".local", "share")
    if os.path.exists(os.path.expanduser(local)):
        return os.path.expanduser(os.path.join(local, __appname__))
    return os.path.expanduser(os.path.join("~", ".{}".format(__appname__)))
