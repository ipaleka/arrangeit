import os

from AppKit import (
    NSSearchPathForDirectoriesInDomains,
    NSApplicationSupportDirectory,
    NSUserDomainMask,
)

from arrangeit import __appname__


def user_data_path():
    """Returns Mac OS X specific path for saving user's data."""
    return os.path.join(
        NSSearchPathForDirectoriesInDomains(
            NSApplicationSupportDirectory, NSUserDomainMask, True
        )[0],
        __appname__,
    )
