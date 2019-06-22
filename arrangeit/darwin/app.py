from PIL import ImageTk

from arrangeit.base import BaseApp
from arrangeit.settings import Settings


class App(BaseApp):
    """Main app class with Mac OS specific code."""

    ## TASKS
    def activate_root(self, wid):
        """

        TODO implement

        :param wid: windows id
        :type wid: int
        """

        # for app in NSWorkspace.sharedWorkspace().runningApplications():
        #     if app.bundleIdentifier() == 'org.python.python':
        #         app.activateWithOptions_(NSApplicationActivateAllWindows | NSApplicationActivateIgnoringOtherApps)

        pass

    def move(self, wid):
        """

        TODO implement

        :param wid: windows id
        :type wid: int
        """
        return self.move_and_resize(wid)

    def move_and_resize(self, wid):
        """Moves and resizes window identified by provided identifier wid.

        TODO implement

        :param wid: windows id
        :type wid: int
        :returns: Boolean
        """
        return True

    def move_to_workspace(self, wid, number):
        """TODO implement

        :param wid: root id got from Tkinter
        :type wid: int
        :param number: our custom workspace number
        :type number: int
        """
        return False

    ## COMMANDS
    def grab_window_screen(self, model):
        """Grabs and returns screenshot of the window from provided model.

        TODO implement

        :param model: model of the window we want screenshot from
        :type model: :class:`WindowModel`
        :returns: (:class:`PIL.ImageTk.PhotoImage`, (int, int))
        """
        return ImageTk.PhotoImage(Settings.BLANK_ICON), (0, 0)
