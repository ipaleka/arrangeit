import ctypes
import ctypes.wintypes

from PIL import Image

from arrangeit.base import BaseCollector
from arrangeit.data import WindowModel
from arrangeit.settings import Settings
from arrangeit.windows.apihelpers import TITLEBARINFO, WINDOWINFO, Api
from win32api import EnumDisplayMonitors
from win32con import (
    GA_ROOTOWNER,
    GCL_HICON,
    GWL_EXSTYLE,
    GWL_STYLE,
    NULL,
    STATE_SYSTEM_INVISIBLE,
    WM_GETICON,
    WS_EX_NOACTIVATE,
    WS_EX_TOOLWINDOW,
    WS_THICKFRAME,
)
from win32gui import (
    GetClassLong,
    GetClassName,
    GetDC,
    GetWindowLong,
    GetWindowPlacement,
    GetWindowText,
    IsIconic,
    IsWindow,
    IsWindowEnabled,
    IsWindowVisible,
    SendMessageTimeout,
)
from win32ui import CreateBitmap, CreateDCFromHandle

DWMWA_CLOAKED = 14


class Collector(BaseCollector):
    """Collecting windows class with MS Windows specific code."""

    def __init__(self):
        """Creates and sets Api instance after call to super."""
        super().__init__()
        self.api = Api()

    def _get_uwpapp_icon(self, hwnd):
        """Returns icon from UWP package associated with provided windows identifier.

        Uses cached package for provided hwnd if it has been already retrieved.

        :param hwnd: window id
        :type hwnd: int
        :returns: :class:`PIL.Image` instance
        """
        if self.api.packages.get(hwnd) is None:
            self.api.packages[hwnd] = self.api.get_package(hwnd)
        return self.api.packages[hwnd].icon

    def _get_application_icon(self, hwnd):
        """Returns application icon of the window with provided hwnd.

        :param hwnd: window id
        :type hwnd: int
        :var icon_handle: handle to windows icon in window instance
        :type icon_handle: int
        :returns: :class:`PIL.Image` instance
        """
        _, icon_handle = SendMessageTimeout(hwnd, WM_GETICON, 1, 0, 0, 50)
        if icon_handle == 0:
            icon_handle = GetClassLong(hwnd, GCL_HICON)
            if icon_handle == 0:
                return self._get_uwpapp_icon(hwnd)

        return self._get_image_from_icon_handle(icon_handle)

    def get_application_name(self, hwnd):
        """Returns application name for the window represented by provided handle.

        For Windows versions greater than 8.1 it uses package app_name if there's cached
        package for provided hwnd.

        Otherwise it tries to extract the name from executable path.

        If previous methods haven't succeed it returns window's class name.

        :param hwnd: window id
        :type hwnd: int
        :param app_name: executable name without extension
        :type app_name: str
        :returns: str
        """
        if self.api.packages.get(hwnd) is not None:
            return self.api.packages[hwnd].app_name

        app_name = self.api.executable_name_for_hwnd(hwnd)
        return app_name if app_name is not None else GetClassName(hwnd)

    def _get_image_from_icon_handle(self, icon_handle):
        """Creates and returns PIL image from provided handle to icon.

        :param icon_handle: handle to windows icon in window instance
        :type icon_handle: int
        :var size: icon size in pixels
        :type size: int
        :var source_hdc: handle to root device context
        :type source_hdc: int
        :var bitmap: PyGdiHANDLE of icon bitmap
        :type bitmap: int
        :var main_hdc: handle to icon device context
        :type main_hdc: int
        :var buffer: string of bitmap bits
        :type buffer: str
        :returns: :class:`PIL.Image` instance
        """
        size = Settings.ICON_SIZE
        source_hdc = CreateDCFromHandle(GetDC(0))

        bitmap = CreateBitmap()
        bitmap.CreateCompatibleBitmap(source_hdc, size, size)
        main_hdc = source_hdc.CreateCompatibleDC()

        main_hdc.SelectObject(bitmap)
        main_hdc.DrawIcon((0, 0), icon_handle)

        buffer = bitmap.GetBitmapBits(True)  # TODO this is deprecated, use GetDIBits
        return Image.frombuffer("RGBA", (size, size), buffer, "raw", "BGRA", 0, 1)

    def _get_window_geometry(self, hwnd):
        """Returns window geometry for the window represented by provided handle.

        Window geometry is represented with tuple (x, y, width, height)

        :param hwnd: window id
        :type hwnd: int
        :returns: (int, int, int, int)
        """
        left, top, right, bottom = GetWindowPlacement(hwnd)[-1]
        return (left, top, right - left, bottom - top)

    def _get_window_title(self, hwnd):
        """Returns title/caption of the window represented by provided handle.

        :param hwnd: window id
        :type hwnd: int
        :returns: str
        """
        return GetWindowText(hwnd)

    def _is_activable(self, hwnd):
        """Checks if provided hwnd represents window that can be activated.

        :param hwnd: window id
        :type hwnd: int
        :returns: Boolean
        """
        window_info = WINDOWINFO()
        ctypes.windll.user32.GetWindowInfo(hwnd, ctypes.byref(window_info))
        return window_info.dwExStyle & WS_EX_NOACTIVATE == 0

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

    def _is_cloaked(self, hwnd):
        """Checks if provided hwnd represents window that is "cloaked".

        TODO try-except in Windows 7, XP, ...

        TODO check what to do with cloaked in another workspaces

        :param hwnd: window id
        :type hwnd: int
        :var cloaked: flag holding non-zero value if window is cloaked
        :type cloaked: :class:`wintypes.INT`
        :returns: Boolean
        """
        cloaked = ctypes.wintypes.INT()
        ctypes.windll.dwmapi.DwmGetWindowAttribute(
            hwnd, DWMWA_CLOAKED, ctypes.byref(cloaked), ctypes.sizeof(cloaked)
        )
        return cloaked.value != 0

    def _is_tool_window(self, hwnd):
        """Checks if provided hwnd represents tool window.

        :param hwnd: window id
        :type hwnd: int
        :returns: Boolean
        """
        return GetWindowLong(hwnd, GWL_EXSTYLE) & WS_EX_TOOLWINDOW != 0

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
        return title_info.rgstate[0] & STATE_SYSTEM_INVISIBLE != 0

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
                restored=self.is_restored(hwnd),
                title=self._get_window_title(hwnd),
                icon=self._get_application_icon(hwnd),
                name=self.get_application_name(hwnd),
                workspace=self.get_workspace_number_for_window(hwnd),
            )
        )

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

    def get_available_workspaces(self):
        """

        TODO implement

        :param hwnd: window id
        :type hwnd: int
        :returns: str
        """
        return [(0, "")]

    def get_monitors_rects(self):
        """Returns list of available monitors position and size rectangles.

        :returns: list [(x,y,w,h)]
        """
        return [rect for (_a, _b, rect) in EnumDisplayMonitors(None, None)]

    def get_windows(self):
        """Creates and returns list of all the windows handles

        :returns: list of integers
        """
        return self.api.enum_windows()

    def get_workspace_number_for_window(self, hwnd):
        """TODO implement

        :param hwnd: window id
        :type hwnd: int
        :returns: str
        """
        return 0

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

    def is_resizable(self, hwnd):
        """Checks if provided hwnd represents window that can be resized.

        :param hwnd: window id
        :type hwnd: int
        :returns: Boolean
        """
        return GetWindowLong(hwnd, GWL_STYLE) & WS_THICKFRAME != 0

    def is_restored(self, hwnd):
        """Checks if provided hwnd represents window that is not minimized.

        :param hwnd: window id
        :type hwnd: int
        :returns: Boolean
        """
        return not IsIconic(hwnd)

    def is_valid_state(self, hwnd):
        """Checks if provided hwnd represents window with valid state for collecting.

        Checking just :func:`_is_activable` for now.

        :param hwnd: window id
        :type hwnd: int
        :returns: Boolean
        """
        if not self._is_activable(hwnd):
            return False

        if self._is_cloaked(hwnd):
            return False

        return True
