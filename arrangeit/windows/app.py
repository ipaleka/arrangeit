import os

import arrangeit
from arrangeit.base import BaseApp


class App(BaseApp):
    """Main app class with MS Windows specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def user_data_path(self):
        """Returns MS Windows specific path for saving user's data."""
        return os.path.expanduser(os.path.join("~", arrangeit.__appname__))

