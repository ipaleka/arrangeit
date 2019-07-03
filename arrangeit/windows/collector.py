import ctypes
import ctypes.wintypes

from PIL import Image

import win32ui
from win32api import CloseHandle, EnumDisplayMonitors, OpenProcess
from win32con import (
    GA_ROOTOWNER,
    GCL_HICON,
    GWL_EXSTYLE,
    GWL_STYLE,
    NULL,
    PROCESS_QUERY_INFORMATION, 
    PROCESS_VM_READ,
    STATE_SYSTEM_INVISIBLE,
    WM_GETICON,
    WS_EX_NOACTIVATE,
    WS_EX_TOOLWINDOW,
    WS_THICKFRAME,
)
from win32gui import (
    EnumChildWindows,
    EnumWindows,
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
from win32process import GetWindowThreadProcessId, GetModuleFileNameEx
from win32ui import CreateBitmap, CreateDCFromHandle

from arrangeit.base import BaseCollector
from arrangeit.data import WindowModel
from arrangeit.settings import Settings
from arrangeit.utils import append_to_collection, open_image

DWMWA_CLOAKED = 14
ERROR_SUCCESS = 0x0
ERROR_INSUFFICIENT_BUFFER = 0x7A
PACKAGE_FILTER_ALL_LOADED = 0x00000000
PACKAGE_FILTER_HEAD = 0x00000010
PACKAGE_INFORMATION_FULL = 0x00000100

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000


class PACKAGE_INFO_REFERENCE(ctypes.Structure):
    """"""

    _fields_ = [
        ("reserved", ctypes.c_void_p),
    ]


class PACKAGE_SUBVERSION(ctypes.Structure):
    """"""

    _fields_ = [
        ("Revision", ctypes.wintypes.ATOM),
        ("Build", ctypes.wintypes.ATOM),
        ("Minor", ctypes.wintypes.ATOM),
        ("Major", ctypes.wintypes.ATOM),
    ]


class PACKAGE_VERSION(ctypes.Union):
    """"""

    _fields_ = [
        ("Version", ctypes.c_uint64),
        ("DUMMY", PACKAGE_SUBVERSION),
    ]


class PACKAGE_ID(ctypes.Union):
    """"""

    _fields_ = [
        # ("reserved", ctypes.wintypes.UINT),
        # ("processorArchitecture", ctypes.wintypes.UINT),
        ("reserved", ctypes.c_uint32),
        ("processorArchitecture", ctypes.c_uint32),
        ("version", PACKAGE_VERSION),
        # ("VersionRevision", ctypes.wintypes.ATOM),
        # ("VersionBuild", ctypes.wintypes.ATOM),
        # ("VersionMinor", ctypes.wintypes.ATOM),
        # ("VersionMajor", ctypes.wintypes.ATOM),
        ("name", ctypes.c_wchar_p),
        ("publisher", ctypes.c_wchar_p),
        ("resourceId", ctypes.c_wchar_p),
        ("publisherId", ctypes.c_wchar_p),        
    ]

    # _map = {"processorArchitecture": EnumProcessorArchitecture}


class PACKAGE_INFO(ctypes.Union):
    """"""

    _fields_ = [
        ("reserved", ctypes.c_uint32),
        ("flags", ctypes.c_uint32),
        ("path", ctypes.c_wchar_p),
        ("packageFullName", ctypes.c_wchar_p),
        ("packageFamilyName", ctypes.c_wchar_p),
        ("packageId", PACKAGE_ID),
    ]


class TITLEBARINFO(ctypes.Structure):
    """Class holding ctypes ctypes.Structure data for title bar information."""

    _fields_ = [
        ("cbSize", ctypes.wintypes.DWORD),
        ("rcTitleBar", ctypes.wintypes.RECT),
        ("rgstate", ctypes.wintypes.DWORD * 6),
    ]


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

    def _get_children(self, hwnd):
        """
        :returns: list of integers
        """
        children = []
        EnumChildWindows(hwnd, append_to_collection, children)
        return children

    def package_full_name_from_handle(self, handle):
        length = ctypes.c_uint()
        retval = ctypes.windll.kernel32.GetPackageFullName(
            handle, ctypes.byref(length), None
        )
        assert retval == ERROR_INSUFFICIENT_BUFFER

        full_name = ctypes.create_unicode_buffer(length.value + 1)
        retval = ctypes.windll.kernel32.GetPackageFullName(
            handle, ctypes.byref(length), full_name
        )
        assert retval == ERROR_SUCCESS

        return full_name

    def package_path_from_full_name(self, full_name):
        length = ctypes.c_uint()
        retval = ctypes.windll.kernel32.GetPackagePathByFullName(
            ctypes.byref(full_name), ctypes.byref(length), None
        )
        assert retval == ERROR_INSUFFICIENT_BUFFER

        package_path = ctypes.create_unicode_buffer(length.value)
        retval = ctypes.windll.kernel32.GetPackagePathByFullName(
            ctypes.byref(full_name), ctypes.byref(length), ctypes.byref(package_path)
        )
        assert retval == ERROR_SUCCESS

        return package_path

    def package_family_name_from_full_name(self, full_name):
        length = ctypes.c_uint()
        retval = ctypes.windll.kernel32.PackageFamilyNameFromFullName(
            ctypes.byref(full_name), ctypes.byref(length), None
        )
        assert retval == ERROR_INSUFFICIENT_BUFFER

        family_name = ctypes.create_unicode_buffer(length.value)
        retval = ctypes.windll.kernel32.PackageFamilyNameFromFullName(
            ctypes.byref(full_name), ctypes.byref(length), ctypes.byref(family_name)
        )
        assert retval == ERROR_SUCCESS

        return family_name

    def package_id_from_full_name(self, full_name):
        length = ctypes.c_uint(0)
        count = ctypes.c_uint()

        retval = ctypes.windll.kernel32.PackageIdFromFullName(
            ctypes.byref(full_name),
            PACKAGE_INFORMATION_FULL, 
            ctypes.byref(length),
            None
        )
        assert retval == ERROR_INSUFFICIENT_BUFFER
        
        buffer = ctypes.create_string_buffer(length.value)
        retval = ctypes.windll.kernel32.PackageIdFromFullName(
            ctypes.byref(full_name),
            PACKAGE_INFORMATION_FULL, 
            ctypes.byref(length), 
            ctypes.byref(buffer)
        )
        assert retval == ERROR_SUCCESS

        return buffer

    def package_info_reference_from_full_name(self, full_name):
        package_info_reference = ctypes.pointer(PACKAGE_INFO_REFERENCE())
        retval = ctypes.windll.kernel32.OpenPackageInfoByFullName(
            ctypes.byref(full_name), 0, ctypes.byref(package_info_reference)
        )
        assert retval == ERROR_SUCCESS

        return package_info_reference

    def package_info_buffer_from_reference(self, package_info_reference):
        length = ctypes.c_uint(0)
        count = ctypes.c_uint()

        retval = ctypes.windll.kernel32.GetPackageInfo(
            package_info_reference, 
            PACKAGE_FILTER_HEAD, 
            ctypes.byref(length),
            None,
            ctypes.byref(count)
        )
        assert retval == ERROR_INSUFFICIENT_BUFFER
        
        buffer = ctypes.create_string_buffer(length.value)
        retval = ctypes.windll.kernel32.GetPackageInfo(
            package_info_reference, 
            PACKAGE_FILTER_HEAD, 
            ctypes.byref(length), 
            ctypes.byref(buffer),
            ctypes.byref(count)
        )
        assert retval == ERROR_SUCCESS

        return buffer

    def get_uwpapp_icon(self, hwnd):
        """
        TODO check what is happened when window is minimized (no different child_pid)
        """        
        _, pid = GetWindowThreadProcessId(hwnd)
        children = self._get_children(hwnd)
        for child in children:
            _, child_pid = GetWindowThreadProcessId(child)
            if child_pid != pid:
                # hprocess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, child_pid)
                hprocess = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, child_pid)
                break

        full_name = self.package_full_name_from_handle(hprocess.handle)
        print("\n             full name:", full_name.value)
        package_path = self.package_path_from_full_name(full_name)
        print("          package path:", package_path.value)
        family_name = self.package_family_name_from_full_name(full_name)
        print("           family name:", family_name.value)
        package_info_reference = self.package_info_reference_from_full_name(full_name)
        print("package info reference:", package_info_reference.contents.reserved)

        package_info_buffer = self.package_info_buffer_from_reference(package_info_reference)
        package_info = PACKAGE_INFO()
        ctypes.memmove(ctypes.addressof(package_info), package_info_buffer, ctypes.sizeof(package_info))
        print("       packageFullName:", package_info.packageFullName)

        package_id_buffer = self.package_id_from_full_name(full_name)
        package_id = PACKAGE_ID()
        ctypes.memmove(ctypes.addressof(package_id), package_id_buffer, ctypes.sizeof(package_id))
        print("       package id name:", package_id.name)

        CloseHandle(hprocess)
        ctypes.windll.kernel32.ClosePackageInfo(package_info_reference)

        # print("no icon", GetWindowText(hwnd))
        # hicon = LoadIcon(hwnd, icon_handle)
        return open_image("white.png")

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
                return self.get_uwpapp_icon(hwnd)

        return self._get_image_from_icon_handle(icon_handle)

    def _get_class_name(self, hwnd):
        """Returns class name for the window represented by provided handle.

        :param hwnd: window id
        :type hwnd: int
        :returns: str
        """
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
                name=self._get_class_name(hwnd),
                icon=self._get_application_icon(hwnd),
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
        """Creates and returns list of all the windows hwnds

        by calling win32gui.EnumWindows with append_to_collection as the argument.

        :returns: list of integers
        """
        hwnds = []
        EnumWindows(append_to_collection, hwnds)
        return hwnds

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
