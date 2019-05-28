import os

from PIL import ImageTk

import arrangeit
from arrangeit import constants
from arrangeit.base import BaseApp


class App(BaseApp):
    """Main app class with MS Windows specific code."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def user_data_path(self):
        """Returns MS Windows specific path for saving user's data."""
        return os.path.expanduser(os.path.join("~", arrangeit.__appname__))

    def grab_window_screen(self, model):
        """TODO implement

        :param model: model of the window we want screenshot form
        :type model: :class:`WindowModel`
        :returns: :class:`PIL.ImageTk.PhotoImage`
        """
        return ImageTk.PhotoImage(constants.BLANK_ICON)

    def move_and_resize(self, wid):
        """TODO implement

        :param wid: root id got from Tkinter
        :type wid: int
        :returns: Boolean
        """
        return None

    def move(self, wid):
        """TODO implement

        :param wid: root id got from Tkinter
        :type wid: int
        """
        return None

    def move_to_workspace(self, hwnd, number):
        """TODO implement

        :param wid: root id got from Tkinter
        :type wid: int
        :param number: our custom workspace number
        :type number: int
        """
        return None
