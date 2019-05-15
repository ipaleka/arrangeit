import ctypes

from win32con import (
    GA_ROOTOWNER,
    GWL_EXSTYLE,
    NULL,
    STATE_SYSTEM_INVISIBLE,
    WS_EX_TOOLWINDOW,
    WS_EX_NOACTIVATE,
    WS_THICKFRAME,
)
from win32gui import (
    EnumWindows,
    GetClassName,
    GetWindowLong,
    GetWindowRect,
    GetWindowText,
    IsWindow,
    IsWindowEnabled,
    IsWindowVisible,
)

from arrangeit.base import BaseCollector
from arrangeit.data import WindowModel
from arrangeit.utils import append_to_collection


class TITLEBARINFO(ctypes.Structure):
    """Class holding ctypes ctypes.Structure data for title bar information."""

    _fields_ = [("cbSize", ctypes.wintypes.DWORD), ("rcTitleBar", ctypes.wintypes.RECT), ("rgstate", ctypes.wintypes.DWORD * 6)]


class WINDOWINFO(ctypes.Structure):
    """Class holding ctypes ctypes.Structure data for window information."""

    _fields_ = [
        ("cbSize", ctypes.wintypes.DWORD),
        ("rcWindow", ctypes.wintypes.RECT),
        ("rcClient", ctypes.wintypes.RECT),
        ("dwStyle", ctypes.wintypes.DWORD),
        ("dwExStyle", ctypes.wintypes.DWORD),
        ("dwWindowStatus", ctypes.wintypes.DWORD),
        ("cxWindowBorders", ctypes.wintypes.UINT),
        ("cyWindowBorders", ctypes.wintypes.UINT),
        ("atomWindowType", ctypes.wintypes.ATOM),
        ("win32conreatorVersion", ctypes.wintypes.DWORD),
    ]


class Collector(BaseCollector):
    """Collecting windows class with MS Windows specific code."""

    def _is_tray_window(self, hwnd):
        """Checks if provided hwnd represents window residing in system tray

        or "Program Manager" window.

        https://github.com/Answeror/lit/blob/master/windows.py

        :param hwnd: window id
        :type hwnd: int
        :returns: Boolean
        """
        title_info = TITLEBARINFO()
        title_info.cbSize = ctypes.sizeof(title_info)
        ctypes.windll.user32.GetTitleBarInfo(hwnd, ctypes.byref(title_info))
        if title_info.rgstate[0] & STATE_SYSTEM_INVISIBLE:
            return True
        return False

    def _is_alt_tab_applicable(self, hwnd):
        """Checks if provided hwnd represents window visible in "Alt+Tab screen".

        https://devblogs.microsoft.com/oldnewthing/?p=24863

        :param hwnd: window id
        :type hwnd: int
        :returns: Boolean
        """
        hwnd_walk = NULL
        hwnd_try = ctypes.windll.user32.GetAncestor(hwnd, GA_ROOTOWNER)
        while hwnd_try != hwnd_walk:
            hwnd_walk = hwnd_try
            hwnd_try = ctypes.windll.user32.GetLastActivePopup(hwnd_walk)
            if IsWindowVisible(hwnd_try):
                break
        if hwnd_walk != hwnd:
            return False
        return True

    def _is_tool_window(self, hwnd):
        """Checks if provided hwnd represents tool window.

        :param hwnd: window id
        :type hwnd: int
        :returns: Boolean
        """
        return GetWindowLong(hwnd, GWL_EXSTYLE) & WS_EX_TOOLWINDOW

    def is_applicable(self, hwnd):
        """Checks if provided hwnd represents window type that should be collected.

        :param hwnd: window id
        :type hwnd: int
        :returns: Boolean
        """
        if not (IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd)):
            return False

        if not self._is_alt_tab_applicable(hwnd):
            return False

        if self._is_tray_window(hwnd):
            return False

        if self._is_tool_window(hwnd):  # TODO: research do we need this
            return False

        return True

    def _is_activable(self, hwnd):
        """Checks if provided hwnd represents window that can be activated.

        :param hwnd: window id
        :type hwnd: int
        :returns: Boolean
        """
        window_info = WINDOWINFO()
        ctypes.windll.user32.GetWindowInfo(hwnd, ctypes.byref(window_info))
        return window_info.dwExStyle & WS_EX_NOACTIVATE

    def is_valid_state(self, hwnd):
        """Checks if provided hwnd represents window with valid state for collecting.

        Checking just :func:`_is_activable` for now.

        :param hwnd: window id
        :type hwnd: int
        :returns: Boolean
        """
        if self._is_activable(hwnd):
            return False

        return True

    def is_resizable(self, hwnd):

        return GetWindowLong(hwnd, GWL_EXSTYLE) & WS_THICKFRAME

    def get_windows(self):
        """Creates and returns list of all the windows hwnds

        by calling win32gui.EnumWindows with append_to_collection as the argument.

        :returns: list of integers
        """
        hwnds = []
        EnumWindows(append_to_collection, hwnds)
        return hwnds

    def check_window(self, hwnd):
        """Checks does window qualify to be collected

        by checking window type applicability with :func:`is_applicable`
        and its current state validity with :func:`is_valid_state`.

        :param hwnd: window id
        :type hwnd: int
        :returns: Boolean
        """
        if not self.is_applicable(hwnd):
            return False

        if not self.is_valid_state(hwnd):
            return False

        return True

    def _get_window_geometry(self, hwnd):
        """Returns window geometry for the window represented by provided handle.

        Window geometry is represented with tuple (x, y, width, height)

        :param hwnd: window id
        :type hwnd: int
        :returns: (int, int, int, int)
        """
        left, top, right, bottom = GetWindowRect(hwnd)
        return (left, top, right - left, bottom - top)

    def _get_window_title(self, hwnd):
        """Returns title/caption of the window represented by provided handle.

        :param hwnd: window id
        :type hwnd: int
        :returns: str
        """
        return GetWindowText(hwnd)

    def _get_class_name(self, hwnd):
        """Returns class name for the window represented by provided handle.

        :param hwnd: window id
        :type hwnd: int
        :returns: str
        """
        return GetClassName(hwnd)

    def add_window(self, hwnd):
        """Creates WindowModel instance from provided hwnd and adds it to collection.

        :param hwnd: window id
        :type hwnd: int
        """
        self.collection.add(
            WindowModel(
                wid=hwnd,
                rect=self._get_window_geometry(hwnd),
                resizable=self.is_resizable(hwnd),
                title=self._get_window_title(hwnd),
                name=self._get_class_name(hwnd),
            )
        )
