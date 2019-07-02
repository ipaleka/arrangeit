from PIL import ImageTk

from win32con import SW_MINIMIZE, SW_RESTORE
from win32gui import IsIconic, MoveWindow, SetActiveWindow, ShowWindow

from arrangeit.base import BaseApp
from arrangeit.settings import Settings


class App(BaseApp):
    """Main app class with MS Windows specific code."""

    ## TASKS
    def activate_root(self, hwnd):
        """Activates/focuses root window identified by provided `hwnd`."""
        SetActiveWindow(hwnd)

    def move(self, hwnd):
        """Just calls `move_and_resize` as the same method moves and resizes

        under MS Windows.

        :param hwnd: windows id
        :type hwnd: int
        """
        return self.move_and_resize(hwnd)

    def move_and_resize(self, hwnd):
        """Moves and resizes window identified by provided hwnd.

        :param hwnd: root id got from Tkinter
        :type hwnd: int
        :var model: collected window data
        :type model: :class:`WindowModel`
        :returns: Boolean
        """
        model = self.collector.collection.get_model_by_wid(hwnd)
        if model.is_ws_changed:
            self.move_to_workspace(hwnd, model.changed_ws)
        if model.is_changed:
            if IsIconic(hwnd):
                ShowWindow(hwnd, SW_RESTORE)
            MoveWindow(hwnd, *model.changed, True)
            if not model.restored:
                ShowWindow(hwnd, SW_MINIMIZE)
            return False
        return True

    def move_to_workspace(self, hwnd, number):
        """TODO implement"""
        pass

    ## COMMANDS
    def grab_window_screen(self, model):
        """TODO implement

        :param model: model of the window we want screenshot from
        :type model: :class:`WindowModel`
        :returns: :class:`PIL.ImageTk.PhotoImage`
        """
        return ImageTk.PhotoImage(Settings.BLANK_ICON), (0, 0)
