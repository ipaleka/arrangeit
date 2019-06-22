import os

from arrangeit import __appname__


def user_data_path():
    """Returns MS Windows specific path for saving user's data."""
    return os.path.expanduser(os.path.join("~", __appname__))
