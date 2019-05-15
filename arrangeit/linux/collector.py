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
        if window_type in (
            Wnck.WindowType.NORMAL,
            Wnck.WindowType.DIALOG,
            Wnck.WindowType.UTILITY,
        ):
            return True
        return False

    def is_valid_state(self, window_type, window_state):
        """Checks if ``window state`` for ``window_type`` qualifies window to collect.

        :param window_type: type of window
        :type window_type: Wnck.WindowType int flag
        :param window_state: current state of window
        :type window_state: Wnck.WindowState int flag
        :returns: Boolean
        """
        if (
            (window_state & Wnck.WindowState.FULLSCREEN != 0)
            or (
                (window_type == Wnck.WindowType.DIALOG)
                and (window_state & Wnck.WindowState.SKIP_TASKLIST != 0)
            )
            or (
                (window_state & Wnck.WindowState.HIDDEN != 0)
                and (window_state & Wnck.WindowState.MINIMIZED == 0)
            )
        ):
            return False
        return True

    def is_resizable(self, window_type):
        """Checks if provided ``window_type`` implies that window is resizable.

        :param window_type: type of window
        :type window_type: Wnck.WindowType int flag
        :returns: Boolean
        """
        if window_type in (Wnck.WindowType.NORMAL,):
            return True
        return False

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

    def __call__(self):
        """Populates ``collection`` with WindowModel instances

        created from the windows list provided by :func:`get_windows`
        after they are checked for compliance with :func:`check_window`
        by calling :func:`add_window`.

        :var win: current window instance in the loop
        :type win: Wnck.Window object
        """
        for win in self.get_windows():
            if self.check_window(win):
                self.add_window(win)

        win = None
        Wnck.shutdown()
