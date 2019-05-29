import os

import arrangeit


def user_data_path():
    """Returns MS Windows specific path for saving user's data."""
    return os.path.expanduser(os.path.join("~", arrangeit.__appname__))
