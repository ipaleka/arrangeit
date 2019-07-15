import os
import sys

from arrangeit import __appname__


def user_data_path():
    """Returns MS Windows specific path for saving user's data."""
    return os.path.expanduser(os.path.join("~", __appname__))


def extract_name_from_bytes_path(path):
    """Returns name without directory structure and extension from given path.

    :param path: full path to file
    :type path: bytes
    :returns: str
    """
    return os.path.splitext(os.path.basename(path))[0].decode(sys.getdefaultencoding())
