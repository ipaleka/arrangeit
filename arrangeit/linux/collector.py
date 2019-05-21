import gi
gi.require_version("Wnck", "3.0")
from gi.repository import Wnck

from arrangeit.base import BaseCollector
from arrangeit.data import WindowModel


class Collector(BaseCollector):
    """Collecting windows class with GNU/Linux specific code."""

    def is_applicable(self, window_type):
        """Checks if provided ``window_type`` qualifies window for collecting.

        :param window_type: type of window
        :type window_type: Wnck.WindowType int flag
        :returns: Boolean
        """
        return window_type in (
            Wnck.WindowType.NORMAL,
            Wnck.WindowType.DIALOG,
            Wnck.WindowType.UTILITY,
        )

    def is_valid_state(self, window_type, window_state):
        """Checks if ``window state`` for ``window_type`` qualifies window to collect.

        :param window_type: type of window
        :type window_type: Wnck.WindowType int flag
        :param window_state: current state of window
        :type window_state: Wnck.WindowState int flag
        :returns: Boolean
        """
        return not (
            window_state & Wnck.WindowState.FULLSCREEN  # TODO Research do we need this
            or (
                window_type == Wnck.WindowType.DIALOG
                and window_state & Wnck.WindowState.SKIP_TASKLIST
            )
            or (
                window_state & Wnck.WindowState.HIDDEN
                and not window_state & Wnck.WindowState.MINIMIZED
            )
        )

    def is_resizable(self, window_type):
        """Checks if provided ``window_type`` implies that window is resizable.

        :param window_type: type of window
        :type window_type: Wnck.WindowType int flag
        :returns: Boolean
        """
        return window_type in (Wnck.WindowType.NORMAL,)

    def get_windows(self):
        """Returns windows list from the Wnck.Screen object.

        :var screen: provides all the windows instances
        :type screen: Wnck.Screen object
        :returns: list of Wnck.Window instances
        """
        screen = Wnck.Screen.get_default()
        screen.force_update()
        return screen.get_windows()

    def check_window(self, win):
        """Checks does window qualify to be collected

        by checking window type applicability with :func:`is_applicable`
        and its state validity for the type with :func:`is_valid_state`.

        :param win: window instance to check
        :type win: Wnck.Window object
        :var window_type: window type
        :type window_type: Wnck.WindowType int flag
        :var window_state: window state
        :type window_state: Wnck.WindowState int flag
        :returns: Boolean
        """
        window_type = win.get_window_type()
        # First of all, skip windows that not qualify at all
        if not self.is_applicable(window_type):
            return False

        window_state = win.get_state()
        # Skip windows having type and state combination that not qualify
        if not self.is_valid_state(window_type, window_state):
            return False

        return True

    def add_window(self, win):
        """Creates WindowModel instance from provided win and adds it to collection.

        :param win: window to create WindowModel from it
        :type win: Wnck.Window object
        """
        self.collection.add(
            WindowModel(
                wid=win.get_xid(),
                rect=win.get_geometry(),
                resizable=self.is_resizable(win.get_window_type()),
                title=win.get_name(),
                name=win.get_class_group_name(),
            )
        )

    async def get_window_by_wid(self, wid):
        """Returns window instance having provided wid.

        :var wid: window id
        :type wid: int
        :returns: Wnck.Window object
        """
        return Wnck.Window.get(wid)

    async def get_window_move_resize_mask(self, model):
        """Returns flag indicating what is changed when we move/resize window.

        Returned flag is combination of the X, Y, WIDTH and HEIGHT bits.

        NOTE we just return all for now

        :param model: model holding window data
        :type model: :class:`WindowModel` instance
        :returns: int flag
        """
        return (
            Wnck.WindowMoveResizeMask.X
            | Wnck.WindowMoveResizeMask.Y
            | Wnck.WindowMoveResizeMask.WIDTH
            | Wnck.WindowMoveResizeMask.HEIGHT
        )
        # return (
        #     (0 if model.changed[0] == model.rect[0] else Wnck.WindowMoveResizeMask.X)
        #     | (0 if model.changed[1] == model.rect[1] else Wnck.WindowMoveResizeMask.Y)
        #     | (
        #         0
        #         if model.changed[2] == model.rect[2]
        #         else Wnck.WindowMoveResizeMask.WIDTH
        #     )
        #     | (
        #         0
        #         if model.changed[3] == model.rect[3]
        #         else Wnck.WindowMoveResizeMask.HEIGHT
        #     )
        # )
