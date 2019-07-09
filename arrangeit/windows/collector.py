import os
import re
import ctypes
import ctypes.wintypes
from itertools import product
import logging
import xml.etree.ElementTree as ET

from PIL import Image

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

from arrangeit.base import BaseCollector
from arrangeit.data import WindowModel
from arrangeit.settings import Settings
from arrangeit.utils import open_image
from arrangeit.windows.apihelpers import (
    TITLEBARINFO,
    WINDOWINFO,
    PACKAGE_INFO,
    enum_windows,
    _package_full_name_from_handle,
    package_info_reference_from_full_name,
    package_info_buffer_from_reference,
    package_full_name_from_hwnd,
    _close_package_info,
    _close_handle,
    _package_id_from_handle,
    _package_family_name_from_handle,
    get_child_process_with_different_pid,
    get_child_with_different_pid
)

DWMWA_CLOAKED = 14
ERROR_SUCCESS = 0x0
ERROR_INSUFFICIENT_BUFFER = 0x7A
APPMODEL_ERROR_NO_PACKAGE = 15700

PACKAGE_FILTER_ALL_LOADED = 0x00000000
PACKAGE_FILTER_HEAD = 0x00000010
PACKAGE_INFORMATION_FULL = 0x00000100

ICON_TYPES = (".targetsize-256_altform-fullcolor", ".targetsize-96_altform-unplated",".scale-200", "", ".scale-100")


class Package(object):
    """TODO tests and docstring"""

    path = ""
    app_name = ""
    icon = open_image("white.png")

    def __init__(self, path=""):
        self.path = path
        self.setup_package()

    def get_first_image(self, sources):
        for name, suffix in product(sources, ICON_TYPES):
            check_name = os.path.splitext(name)[0] + suffix + os.path.splitext(name)[1]
            path = os.path.join(self.path, check_name)
            if os.path.exists(path):
                try:
                    print(path)
                    image = Image.open(path)
                    return image.resize((Settings.ICON_SIZE, Settings.ICON_SIZE), Image.HAMMING)
                except IOError:
                    pass

        return open_image("white.png")

    def namespace_for_element(self, element):
        match = re.match(r"\{.*\}", element.tag)
        return match.group(0) if match else ""

    def setup_package(self):

        manifest_file = os.path.join(self.path, "AppXManifest.xml")
        if not os.path.exists(manifest_file):
            return
        tree = ET.parse(manifest_file)
        root = tree.getroot()
        namespace = self.namespace_for_element(root)

        for identity in next(root.iter("{}Identity".format(namespace))).iter():
            if "Name" in identity.attrib:
                self.app_name = identity.attrib["Name"].split(".")[-1]

        sources = []
        for subelem in next(root.iter("{}Applications".format(namespace))).iter():
            if "VisualElements" in subelem.tag:
                for name in ("Square44x44Logo", "Square150x150Logo"):
                    attrib = subelem.attrib.get(name)
                    if attrib not in sources:
                        sources.append(attrib)

        for prop in next(root.iter("{}Properties".format(namespace))).iter():
            if "Logo" in prop.tag and prop.text not in sources:
                sources.append(prop.text)

        self.icon = self.get_first_image(sources)


class Api(object):
    """TODO tests and docstring"""

    packages = {}

    def get_package(self, hwnd):

        full_name = package_full_name_from_hwnd(hwnd)
        if not full_name:
            logging.info("get_package: hwnd {} has no full_name.".format(hwnd))
            return Package("")

        package_info_reference = package_info_reference_from_full_name(full_name)
        package_info_buffer, _a = package_info_buffer_from_reference(
            package_info_reference
        )
        package_info = PACKAGE_INFO.from_buffer(package_info_buffer)

        _close_package_info(package_info_reference.contents)

        # print(package_info.path)
        return Package(package_info.path)


class Collector(BaseCollector):
    """Collecting windows class with MS Windows specific code."""

    def __init__(self):
        """TODO tests and docstring"""
        super().__init__()
        self.api = Api()

    def _get_uwpapp_icon(self, hwnd):
        """
        TODO check what is happened when window is minimized (no different child_pid)
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

    def _get_class_name(self, hwnd):
        """Returns class name for the window represented by provided handle.

        TODO tests

        :param hwnd: window id
        :type hwnd: int
        :returns: str
        """
        if self.api.packages.get(hwnd) is not None:
            return self.api.packages[hwnd].app_name

        return GetClassName(hwnd)

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
                name=self._get_class_name(hwnd),
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
        return enum_windows()

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
