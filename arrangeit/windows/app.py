from PIL import ImageTk
from win32gui import MoveWindow, SetActiveWindow

from arrangeit.settings import Settings
from arrangeit.base import BaseApp


class App(BaseApp):
    """Main app class with MS Windows specific code."""

    ## TASKS
    def activate_root(self, wid):
        """Activates/focuses root window identified by provided `wid`."""
        SetActiveWindow(wid)

    def move(self, wid):
        """Just calls `move_and_resize` as the same method moves and resizes

        under MS Windows.

        :param wid: windows id
        :type wid: int
        """
        return self.move_and_resize(wid)

    def move_and_resize(self, wid):
        """Moves and resizes window identified by provided wid.

        :param wid: root id got from Tkinter
        :type wid: int
        :var model: collected window data
        :type model: :class:`WindowModel`
        :returns: Boolean
        """
        model = self.collector.collection.get_model_by_wid(wid)
        if model.is_ws_changed:
            self.move_to_workspace(wid, model.changed_ws)
        if model.is_changed:
            MoveWindow(wid, *model.changed, True)
            # if win.is_maximized():
            #     win.unmaximize()
            return False
        return True
        # http://timgolden.me.uk/pywin32-docs/win32gui__MoveWindow_meth.html
        # https://stackoverflow.com/questions/2335721/how-can-i-get-the-window-focused-on-windows-and-re-size-it

    def move_to_workspace(self, wid, number):
        pass

    ## COMMANDS
    def grab_window_screen(self, model):
        """TODO implement

        :param model: model of the window we want screenshot from
        :type model: :class:`WindowModel`
        :returns: :class:`PIL.ImageTk.PhotoImage`
        """
        return ImageTk.PhotoImage(Settings.BLANK_ICON), (0, 0)
