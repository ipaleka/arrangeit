# arrangeit - cross-platform desktop utility for easy windows management
# Copyright (C) 1999-2019 Ivica Paleka

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import ctypes
import ctypes.wintypes
import logging
import os
import re
import sys
import xml.etree.ElementTree as ET
from itertools import product

from PIL import Image

from arrangeit.settings import Settings
from arrangeit.utils import Rectangle, open_image
from arrangeit.windows.utils import extract_name_from_bytes_path
from arrangeit.windows.vdi import VirtualDesktopsWin10

APPMODEL_ERROR_NO_PACKAGE = 15700
ERROR_INSUFFICIENT_BUFFER = 0x7A
ERROR_SUCCESS = S_OK = 0x00000000
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PACKAGE_FILTER_HEAD = 0x00000010
UWP_ICON_SUFFIXES = (
    ".targetsize-256_altform-fullcolor",
    ".targetsize-96_altform-unplated",
    ".scale-200",
    "",  # as is
    ".scale-100",
)
DWMWA_CLOAKED = 14
DWMWA_EXTENDED_FRAME_BOUNDS = 9
DWM_TNP_RECTDESTINATION = 0x00000001
DWM_TNP_RECTSOURCE = 0x00000002
DWM_TNP_OPACITY = 0x00000004
DWM_TNP_VISIBLE = 0x00000008
DWM_TNP_SOURCECLIENTAREAONLY = 0x00000010


def platform_supports_packages():
    """Returns Boolean indicating if Windows version supports packages.

    :var version: platform version data
    :type version: named tuple
    :returns: Boolean
    """
    try:
        version = sys.getwindowsversion()
        if version.major > 6 or (version.major == 6 and version.minor > 1):
            return True
        return False
    except AttributeError:  # Sphinx
        return None


def platform_supports_virtual_desktops():
    """Returns Boolean indicating if Windows version supports virtual desktops.

    :var version: platform version data
    :type version: named tuple
    :returns: Boolean
    """
    try:
        version = sys.getwindowsversion()
        if version.major >= 10:
            return True
        return False
    except AttributeError:  # Sphinx
        return None


class DWM_THUMBNAIL_PROPERTIES(ctypes.Structure):
    """Class holding ctypes.Structure data for DWM thumbnail properties."""

    _fields_ = [
        ("dwFlags", ctypes.wintypes.DWORD),
        ("rcDestination", ctypes.wintypes.RECT),
        ("rcSource", ctypes.wintypes.RECT),
        ("opacity", ctypes.wintypes.BYTE),
        ("fVisible", ctypes.wintypes.BOOL),
        ("fSourceClientAreaOnly", ctypes.wintypes.BOOL),
    ]


class TITLEBARINFO(ctypes.Structure):
    """Class holding ctypes.Structure data for title bar information."""

    _fields_ = [
        ("cbSize", ctypes.wintypes.DWORD),
        ("rcTitleBar", ctypes.wintypes.RECT),
        ("rgstate", ctypes.wintypes.DWORD * 6),
    ]


class WINDOWINFO(ctypes.Structure):
    """Class holding ctypes.Structure data for window information."""

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
        ("wCreatorVersion", ctypes.wintypes.DWORD),
    ]


class PACKAGE_SUBVERSION(ctypes.Structure):
    """Class holding subpackage version data."""

    _fields_ = [
        ("Revision", ctypes.wintypes.USHORT),
        ("Build", ctypes.wintypes.USHORT),
        ("Minor", ctypes.wintypes.USHORT),
        ("Major", ctypes.wintypes.USHORT),
    ]


class PACKAGE_VERSION_U(ctypes.Union):
    """Helper class holding union data for package version."""

    _fields_ = [("Version", ctypes.c_uint64), ("DUMMYSTRUCTNAME", PACKAGE_SUBVERSION)]


class PACKAGE_VERSION(ctypes.Structure):
    """Class holding data for package version."""

    _anonymous_ = ("u",)
    _fields_ = [("u", PACKAGE_VERSION_U)]


class PACKAGE_ID(ctypes.Structure):
    """Class holding data for package identication."""

    _fields_ = [
        ("reserved", ctypes.c_uint32),
        ("processorArchitecture", ctypes.c_uint32),
        ("version", PACKAGE_VERSION),
        ("name", ctypes.c_wchar_p),
        ("publisher", ctypes.c_wchar_p),
        ("resourceId", ctypes.c_wchar_p),
        ("publisherId", ctypes.c_wchar_p),
    ]


class PACKAGE_INFO(ctypes.Structure):
    """Class holding data for package information."""

    _fields_ = [
        ("reserved", ctypes.c_uint32),
        ("flags", ctypes.c_uint32),
        ("path", ctypes.c_wchar_p),
        ("packageFullName", ctypes.c_wchar_p),
        ("packageFamilyName", ctypes.c_wchar_p),
        ("packageId", PACKAGE_ID),
    ]


class PACKAGE_INFO_REFERENCE(ctypes.Structure):
    """Class holding ctypes.Structure pointer to package information struture."""

    _fields_ = [("reserved", ctypes.c_void_p)]


class Helpers(object):
    """Helper class for calls to WinDLL API."""

    def __init__(self):
        """Calls setup methods."""
        self._setup_base()
        self._setup_common_helpers()
        self._setup_thumbnail_helpers()
        if platform_supports_packages():
            self._setup_win8_helpers()

    def _setup_base(self):
        """Sets wWinDLL domain objects and helper shortcuts.

        :var _user32: object holding API functions from user32 domain
        :type _user32: :class:`ctypes.WinDLL`
        :var _kernel32: object holding API functions from kernel32 domain
        :type _kernel32: :class:`ctypes.WinDLL`
        :var _psapi: object holding API functions from psapi domain
        :type _psapi: :class:`ctypes.WinDLL`
        :var _dwmapi: object holding API functions from dwmapi domain
        :type _dwmapi: :class:`ctypes.WinDLL`
        :var WNDENUMPROC: helper function for windows enumeration
        :type WNDENUMPROC: :class:`ctypes.WINFUNCTYPE`
        """
        self._user32 = ctypes.WinDLL("user32", use_last_error=True)
        self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self._psapi = ctypes.WinDLL("psapi", use_last_error=True)
        self._dwmapi = ctypes.WinDLL("dwmapi", use_last_error=True)
        self.WNDENUMPROC = ctypes.WINFUNCTYPE(
            ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM
        )

    def _setup_helper(self, section, name, argtypes, restype):
        """Retrieves and returns Windows API function with given ``name`` from ``section``.

        Also sets given ``argtypes``and ``restype`` attributes to functiom.

        :var section: object holding API functions from specific domain
        :type section: :class:`ctypes.WinDLL`
        :var name: Windows API function name
        :type name: str
        :var argtypes: collection of ctypes objects arguments to Windows API function
        :type argtypes: tuple
        :var restype: returning value of Windows API function
        :type restype: ctypes type object
        :returns: Windows API function callback
        """
        helper = getattr(section, name)
        helper.argtypes = argtypes
        helper.restype = restype
        return helper

    def _setup_common_helpers(self):
        """Sets helper methods common to all MS Windows versions."""
        self._get_ancestor = self._setup_helper(
            self._user32,
            "GetAncestor",
            (ctypes.wintypes.HWND, ctypes.wintypes.UINT),
            ctypes.wintypes.HWND,
        )
        self._get_last_active_popup = self._setup_helper(
            self._user32,
            "GetLastActivePopup",
            (ctypes.wintypes.HWND,),
            ctypes.wintypes.HWND,
        )
        self._get_titlebar_info = self._setup_helper(
            self._user32,
            "GetTitleBarInfo",
            (ctypes.wintypes.HWND, ctypes.POINTER(TITLEBARINFO)),
            ctypes.wintypes.BOOL,
        )
        self._get_window_info = self._setup_helper(
            self._user32,
            "GetWindowInfo",
            (ctypes.wintypes.HWND, ctypes.POINTER(WINDOWINFO)),
            ctypes.wintypes.BOOL,
        )
        self._get_windows_thread_process_id = self._setup_helper(
            self._user32,
            "GetWindowThreadProcessId",
            (ctypes.wintypes.HWND, ctypes.POINTER(ctypes.wintypes.DWORD)),
            ctypes.wintypes.DWORD,
        )
        self._enum_windows = self._setup_helper(
            self._user32,
            "EnumWindows",
            (self.WNDENUMPROC, ctypes.wintypes.LPARAM),
            ctypes.wintypes.BOOL,
        )
        self._enum_child_windows = self._setup_helper(
            self._user32,
            "EnumChildWindows",
            (ctypes.wintypes.HWND, self.WNDENUMPROC, ctypes.wintypes.LPARAM),
            ctypes.wintypes.BOOL,
        )
        self._open_process = self._setup_helper(
            self._kernel32,
            "OpenProcess",
            (ctypes.wintypes.DWORD, ctypes.wintypes.BOOL, ctypes.wintypes.DWORD),
            ctypes.wintypes.HANDLE,
        )
        self._close_handle = self._setup_helper(
            self._kernel32,
            "CloseHandle",
            (ctypes.wintypes.HANDLE,),
            ctypes.wintypes.BOOL,
        )
        self._get_process_image_file_name = self._setup_helper(
            self._psapi,
            "GetProcessImageFileNameA",
            (ctypes.wintypes.HANDLE, ctypes.wintypes.LPSTR, ctypes.wintypes.DWORD),
            ctypes.wintypes.DWORD,
        )
        self._dwm_get_window_attribute = self._setup_helper(
            self._dwmapi,
            "DwmGetWindowAttribute",
            (
                ctypes.wintypes.HWND,
                ctypes.wintypes.DWORD,
                ctypes.wintypes.LPVOID,
                ctypes.wintypes.DWORD,
            ),
            ctypes.wintypes.DWORD,
        )

    def _setup_thumbnail_helpers(self):
        """Sets helper methods for DWM thumnails."""
        self._dwm_is_composition_enabled = self._setup_helper(
            self._dwmapi,
            "DwmIsCompositionEnabled",
            (ctypes.POINTER(ctypes.wintypes.BOOL),),
            ctypes.wintypes.DWORD,
        )
        self._dwm_register_thumbnail = self._setup_helper(
            self._dwmapi,
            "DwmRegisterThumbnail",
            (
                ctypes.wintypes.HANDLE,
                ctypes.wintypes.HANDLE,
                ctypes.POINTER(ctypes.wintypes.HANDLE),
            ),
            ctypes.wintypes.DWORD,
        )
        self._dwm_update_thumbnail_properties = self._setup_helper(
            self._dwmapi,
            "DwmUpdateThumbnailProperties",
            (ctypes.wintypes.HANDLE, ctypes.POINTER(DWM_THUMBNAIL_PROPERTIES)),
            ctypes.wintypes.DWORD,
        )
        self._dwm_unregister_thumbnail = self._setup_helper(
            self._dwmapi,
            "DwmUnregisterThumbnail",
            (ctypes.wintypes.HANDLE,),
            ctypes.wintypes.DWORD,
        )

    def _setup_win8_helpers(self):
        """Sets helper methods specific to MS Windows versions >= 8."""
        self._get_package_full_name = self._setup_helper(
            self._kernel32,
            "GetPackageFullName",
            (
                ctypes.wintypes.HANDLE,
                ctypes.POINTER(ctypes.c_uint32),
                ctypes.wintypes.LPCWSTR,
            ),
            ctypes.wintypes.LONG,
        )
        self._open_package_info_by_full_name = self._setup_helper(
            self._kernel32,
            "OpenPackageInfoByFullName",
            (
                ctypes.wintypes.LPCWSTR,
                ctypes.c_uint32,
                ctypes.POINTER(PACKAGE_INFO_REFERENCE),
            ),
            ctypes.wintypes.LONG,
        )
        self._get_package_info = self._setup_helper(
            self._kernel32,
            "GetPackageInfo",
            (
                PACKAGE_INFO_REFERENCE,
                ctypes.c_uint32,
                ctypes.POINTER(ctypes.c_uint32),
                ctypes.POINTER(ctypes.c_uint8),
                ctypes.POINTER(ctypes.c_uint32),
            ),
            ctypes.wintypes.LONG,
        )
        self._close_package_info = self._setup_helper(
            self._kernel32,
            "ClosePackageInfo",
            (PACKAGE_INFO_REFERENCE,),
            ctypes.wintypes.LONG,
        )


class Package(object):
    """Helper class for calls to Windows API.

    :var path: filesystem path to package directory
    :type path: str
    :var app_name: name of package's first application
    :type app_name: str
    :var Package.icon: application icon
    :type Package.icon: :class:`PIL.Image`
    """

    path = ""
    app_name = ""
    icon = open_image("white.png")

    def __init__(self, path=""):
        """Sets ``path`` attribute from provided argument and calls package setup.

        :param path: filesystem path to package directory
        :type path: str
        """
        self.path = path
        self.setup_package()

    def _get_first_image(self, sources):
        """Returns first image that exists in filesystem for provided ``sources``

        in combination to package path and defined icon sufixess. Returned image is
        resized to icon size defined in Settings.

        :param sources: collection of image paths relative to their package directory
        :type sources: list
        :var check_name: filename made of sources element and suffix
        :type check_name: str
        :var path: full path to eventual image file
        :type path: str
        :returns: :class:`PIL.Image` instance
        """
        for name, suffix in product(sources, UWP_ICON_SUFFIXES):
            check_name = os.path.splitext(name)[0] + suffix + os.path.splitext(name)[1]
            path = os.path.join(self.path, check_name)
            if os.path.exists(path):
                try:
                    return Image.open(path).resize(
                        (Settings.ICON_SIZE, Settings.ICON_SIZE), Image.BICUBIC
                    )
                except IOError:
                    pass

        return open_image("white.png")

    def _get_manifest_root(self):
        """Returns root element of package's manifest XML document.

        :var manifest_file: path to XML document
        :type manifest_file: str
        :var tree: package information
        :type tree: :class:`xml.etree.ElementTree`
        :returns: :class:`xml.etree.ElementTree.Element`
        """
        manifest_file = os.path.join(self.path, "AppXManifest.xml")
        if not os.path.exists(manifest_file):
            return True

        tree = ET.parse(manifest_file)
        return tree.getroot()

    def _namespace_for_element(self, element):
        """Returns XML namespace from the tag of provided XML ``element``.

        https://stackoverflow.com/a/20104763/11703358

        :param element: element of XML document
        :type element: :class:`xml.etree.ElementTree.Element`
        :var match: regular expression match object
        :type match: :class:`re.Match`
        :returns: str
        """
        match = re.match(r"\{.*\}", element.tag)
        return match.group(0) if match else ""

    def _setup_app_name(self, root):
        """Sets app_name attribute from provided ``root`` XML element

        by extracting Identity element's Name attribute.

        :param root: root element of XML document
        :type root: :class:`xml.etree.ElementTree.Element`
        :var namespace: namespace retrieved from root XML element
        :type namespace: str
        :var identity: package's identity
        :type identity: :class:`xml.etree.ElementTree.Element`
        """
        namespace = self._namespace_for_element(root)
        for identity in next(root.iter("{}Identity".format(namespace))).iter():
            if "Name" in identity.attrib:
                self.app_name = identity.attrib["Name"].split(".")[-1]
                break

    def _setup_icon(self, root):
        """Sets icon attribute from provided ``root`` XML element

        by extracting predefined image types from XML document and picking
        the first that exists in filesystem.

        :param root: root element of XML document
        :type root: :class:`xml.etree.ElementTree.Element`
        :var sources: collection of image paths relative to their package directory
        :type sources: list
        :var namespace: namespace retrieved from root XML element
        :type namespace: str
        :var subelem: current child element of the first Applications XML element
        :type subelem: :class:`xml.etree.ElementTree.Element`
        :var prop: current child element of the first Properties XML element
        :type prop: :class:`xml.etree.ElementTree.Element`
        :var attrib: image path relative to package directory
        :type attrib: str
        """
        sources = []
        namespace = self._namespace_for_element(root)
        for subelem in next(root.iter("{}Applications".format(namespace))).iter():
            if "VisualElements" in subelem.tag:
                for name in ("Square44x44Logo", "Square150x150Logo"):
                    attrib = subelem.attrib.get(name)
                    if attrib not in sources:
                        sources.append(attrib)
                break

        for prop in next(root.iter("{}Properties".format(namespace))).iter():
            if "Logo" in prop.tag and prop.text not in sources:
                sources.append(prop.text)
                break

        self.icon = self._get_first_image(sources)

    def setup_package(self):
        """Retrieves and sets package data.

        TODO add call to this method after window is exposed if it was minimized

        :var root: root element of XML document
        :type root: :class:`xml.etree.ElementTree.Element`
        """
        root = self._get_manifest_root()
        self._setup_app_name(root)
        self._setup_icon(root)


class DummyVirtualDesktops(object):
    """Helper class for systems that don't support virtual desktops."""

    def get_desktops(self, refresh=False):
        """Returns list with single two-tuple of 0 and empty string."""
        return [(0, "")]

    def get_window_desktop(self, hwnd, refresh=False):
        """Returns two-tuple of 0 and empty string."""
        return (0, "")

    def move_window_to_desktop(self, hwnd, desktop_ordinal):
        """Just returns None."""
        return None


class Api(object):
    """Helper class for calls to Windows API.

    :var packages: cached collection of packages distincted by windows handles
    :type packages: dictionary of :class:`Package`
    :var helpers: object holding helper methods for Windows API functions
    :type helpers: :class:`Helpers`
    :var Api.vdi: object holding methods of virtual desktop interface
    :type Api.vdi: :class:`VirtualDesktopsWin10`
    """

    packages = {}
    helpers = None
    vdi = None

    def __init__(self):
        """Initializes and sets attribute for helpers instance."""
        self.helpers = Helpers()
        self.vdi = (
            DummyVirtualDesktops()
            if not platform_supports_virtual_desktops()
            else VirtualDesktopsWin10()
        )

    def _package_full_name_from_handle(self, handle):
        """Returns full name of the package associated with provided process handle.

        First we call :func:`_get_package_full_name` helper function to fill ``length``
        variable, and afterwards to fill ``full_name`` variable.

        :param handle: process handle
        :type handle: int
        :var length: buffer size in characters
        :type length: :class:`ctypes.c_uint`
        :var ret_val: function returned value indicating error/success status
        :type ret_val: int
        :var full_name: buffer holding package full name
        :type full_name: array of :class:`ctypes.c_wchar`
        :returns: array of :class:`ctypes.c_wchar`
        """
        length = ctypes.c_uint()
        ret_val = self.helpers._get_package_full_name(
            handle, ctypes.byref(length), None
        )
        if ret_val == APPMODEL_ERROR_NO_PACKAGE:
            return None

        full_name = ctypes.create_unicode_buffer(length.value + 1)
        ret_val = self.helpers._get_package_full_name(
            handle, ctypes.byref(length), full_name
        )
        if ret_val != ERROR_SUCCESS:
            logging.info(
                "_package_full_name_from_handle: error -> {}".format(
                    str(ctypes.WinError(ctypes.get_last_error()))
                )
            )
            return None

        return full_name

    def _package_full_name_from_hwnd(self, hwnd):
        """Returns full name of the package associated with provided window identifier.

        :func:`enum_windows` is called to retrieve all the children windows. Very first
        package full name is returned if it can be retrieved from associated process
        of a child window.

        :param hwnd: window handle
        :type hwnd: int
        :var child: child window identifier
        :type child: int
        :var child_pid: child process identifier
        :type child_pid: int
        :var hprocess: child process handle
        :type hprocess: int
        :var full_name: buffer holding package full name
        :type full_name: array of :class:`ctypes.c_wchar`
        :returns: array of :class:`ctypes.c_wchar`
        """
        for child in self.enum_windows(hwnd, enum_children=True):
            child_pid = ctypes.wintypes.DWORD(0)
            self.helpers._get_windows_thread_process_id(child, ctypes.byref(child_pid))
            hprocess = self.helpers._open_process(
                PROCESS_QUERY_LIMITED_INFORMATION, False, child_pid
            )
            full_name = self._package_full_name_from_handle(hprocess)
            self.helpers._close_handle(hprocess)
            if full_name is not None:
                return full_name

    def _package_info_buffer_from_reference(self, package_info_reference):
        """Returns buffer of package info structure from provided reference.

        First we call :func:`_get_package_info` helper function to fill ``length``
        variable, and afterwards to fill ``buffer`` variable.

        :param package_info_reference: reference to package info structure pointer
        :type package_info_reference: int
        :var length: buffer size in characters
        :type length: :class:`ctypes.c_uint`
        :var count: number of elements in buffer array
        :type count: :class:`ctypes.c_uint`
        :var ret_val: function returned value indicating error/success status
        :type ret_val: int
        :var buffer: buffer holding reference to package info structure
        :type buffer: array of :class:`ctypes.c_char`
        :var buffer_bytes: size of package info structure data
        :type buffer_bytes: array of bytes
        :returns: array of :class:`ctypes.c_char`
        """
        length = ctypes.c_uint(0)
        count = ctypes.c_uint()

        ret_val = self.helpers._get_package_info(
            package_info_reference.contents,
            PACKAGE_FILTER_HEAD,
            ctypes.byref(length),
            None,
            ctypes.byref(count),
        )
        if ret_val != ERROR_INSUFFICIENT_BUFFER:
            logging.info(
                "_package_info_buffer_from_reference: error -> {}".format(
                    str(ctypes.WinError(ctypes.get_last_error()))
                )
            )
            return None

        buffer = ctypes.create_string_buffer(length.value)
        buffer_bytes = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_uint8))
        ret_val = self.helpers._get_package_info(
            package_info_reference.contents,
            PACKAGE_FILTER_HEAD,
            ctypes.byref(length),
            buffer_bytes,
            ctypes.byref(count),
        )
        if ret_val != ERROR_SUCCESS:
            logging.info(
                "_package_info_buffer_from_reference: error -> {}".format(
                    str(ctypes.WinError(ctypes.get_last_error()))
                )
            )
            return None

        return buffer

    def _package_info_reference_from_full_name(self, full_name):
        """Returns reference to package info structure from provided package full name.

        :param full_name: buffer holding package full name
        :type full_name: array of :class:`ctypes.c_wchar`
        :var package_info_reference: reference to package info structure pointer
        :type package_info_reference: int
        :var ret_val: function returned value indicating error/success status
        :type ret_val: int
        :returns: int
        """
        package_info_reference = ctypes.pointer(PACKAGE_INFO_REFERENCE())
        ret_val = self.helpers._open_package_info_by_full_name(
            full_name, 0, package_info_reference
        )
        if ret_val != ERROR_SUCCESS:
            logging.info(
                "_package_info_reference_from_full_name: error -> {}".format(
                    str(ctypes.WinError(ctypes.get_last_error()))
                )
            )
            return None

        return package_info_reference

    def _rectangle_to_wintypes_rect(self, rectangle):
        """Creates and returns wintypes RECT instance from provided rectangle.

        :param rectangle: area represented with x0 y0 x1 y1 points
        :type rectangle: :class:`arrangeit.utils.Rectangle`
        :var winrect: rectangle as ctypes.wintypes type
        :type winrect: :class:`ctypes.wintypes.RECT`
        :returns: :class:`ctypes.wintypes.RECT`
        """
        winrect = ctypes.wintypes.RECT()
        winrect.left, winrect.top, winrect.right, winrect.bottom = rectangle
        return winrect

    def _update_thumbnail(self, thumbnail_id, rectangle):
        """Updates thumbnail with provided id based on provided rectangle.

        :param thumbnail_id: id of thumbnail to update
        :type thumbnail_id: :class:`ctypes.wintypes.HANDLE`
        :param rectangle: area occupied by thumbnail
        :type rectangle: :class:`arrangeit.utils.Rectangle`
        :var winrect: rectangle as ctypes.wintypes type
        :type winrect: :class:`ctypes.wintypes.RECT`
        :var properties: thumbnail properties
        :type properties: :class:`DWM_THUMBNAIL_PROPERTIES`
        :var ret_val: function returned value indicating error/success status
        :type ret_val: int
        :returns: :class:`ctypes.wintypes.HANDLE`
        """
        properties = DWM_THUMBNAIL_PROPERTIES()
        properties.dwFlags = (
            DWM_TNP_RECTDESTINATION
            | DWM_TNP_RECTSOURCE
            | DWM_TNP_OPACITY
            | DWM_TNP_VISIBLE
            | DWM_TNP_SOURCECLIENTAREAONLY
        )
        winrect = self._rectangle_to_wintypes_rect(rectangle)
        properties.rcDestination = winrect
        properties.rcSource = winrect
        properties.opacity = ctypes.wintypes.BYTE(255)
        properties.fVisible = True
        properties.fSourceClientAreaOnly = False

        ret_val = self.helpers._dwm_update_thumbnail_properties(
            thumbnail_id, ctypes.byref(properties)
        )
        if ret_val != S_OK:
            logging.info(
                "_update_thumbnail: error -> {}".format(
                    str(ctypes.WinError(ctypes.get_last_error()))
                )
            )
            return None

        return thumbnail_id

    def _wintypes_rect_to_rectangle(self, winrect):
        """Creates and returns Rectangle from provided wintypes RECT instance.

        :param winrect: rectangle as ctypes.wintypes type
        :type winrect: :class:`ctypes.wintypes.RECT`
        :returns: :class:`arrangeit.utils.Rectangle`
        """
        return Rectangle(winrect.left, winrect.top, winrect.right, winrect.bottom)

    def cloaked_value(self, hwnd):
        """Helper function to return DWM cloaked value for window with provided hwnd.

        0 is returned for Windows 7 and earlier versions (helper method returns
        error value).

        :param hwnd: window id
        :type hwnd: int
        :var cloaked: flag holding non-zero value if window is cloaked
        :type cloaked: :class:`ctypes.wintypes.INT`
        :var ret_val: function returned value indicating error/success status
        :type ret_val: int
        :returns: int
        """
        cloaked = ctypes.wintypes.DWORD()
        ret_val = self.helpers._dwm_get_window_attribute(
            hwnd, DWMWA_CLOAKED, ctypes.byref(cloaked), ctypes.sizeof(cloaked)
        )
        return cloaked.value if ret_val == S_OK else 0

    def enum_windows(self, hwnd=None, enum_children=False):
        """Helper function to enumerate either desktop windows or children windows

        for window identified by provided hwnd.

        :param hwnd: window id
        :type hwnd: int
        :param enum_children: should children windows be enumerated
        :type enum_children: Boolean
        :returns: list
        """
        hwnds = []

        def append_to_collection(element, param):
            """Simple inner helper function to append provided element to parent hwnds.

            :param element: element to add
            :type element: int
            :returns: True
            """
            hwnds.append(element)
            return True

        func = self.helpers.WNDENUMPROC(append_to_collection)
        if enum_children:
            self.helpers._enum_child_windows(hwnd, func, 0)
        else:
            self.helpers._enum_windows(func, 0)

        return hwnds

    def executable_name_for_hwnd(self, hwnd):
        """Returns name of the executable associated with provided window identifier.

        :param hwnd: window handle
        :type hwnd: int
        :var pid: process identifier
        :type pid: int
        :var hprocess: process handle
        :type hprocess: int
        :var path_buffer: buffer holding executable path
        :type path_buffer: array of :class:`ctypes.c_wchar`
        :var ret_val: function returned value indicating success for value > 0
        :type ret_val: int
        :returns: str
        """
        pid = ctypes.wintypes.DWORD()
        self.helpers._get_windows_thread_process_id(hwnd, ctypes.byref(pid))
        hprocess = self.helpers._open_process(
            PROCESS_QUERY_LIMITED_INFORMATION, False, pid
        )
        path_buffer = ctypes.create_string_buffer(500)
        ret_val = self.helpers._get_process_image_file_name(hprocess, path_buffer, 500)
        self.helpers._close_handle(hprocess)
        if ret_val:
            return extract_name_from_bytes_path(path_buffer.value)

    def extended_frame_rect(self, hwnd):
        """Helper function to return DWM frame rect for window with provided hwnd.

        :param hwnd: window id
        :type hwnd: int
        :var winrect: area of window extended bounds
        :type winrect: :class:`ctypes.wintypes.RECT`
        :var ret_val: function returned value indicating success for value > 0
        :type ret_val: int
        :returns: int
        """
        winrect = ctypes.wintypes.RECT()
        ret_val = self.helpers._dwm_get_window_attribute(
            hwnd,
            DWMWA_EXTENDED_FRAME_BOUNDS,
            ctypes.byref(winrect),
            ctypes.sizeof(winrect),
        )
        if ret_val != S_OK:
            logging.info(
                "extended_frame_rect: error -> {}".format(
                    str(ctypes.WinError(ctypes.get_last_error()))
                )
            )
            return None

        return self._wintypes_rect_to_rectangle(winrect)

    def get_ancestor_by_type(self, hwnd, ancestor_type):
        """Helper function to return hwnd of ancestor window of window with given hwnd.

        :param hwnd: window id
        :type hwnd: int
        :param ancestor_type: window ancestor type
        :type ancestor_type: int
        :returns: int
        """
        return self.helpers._get_ancestor(hwnd, ancestor_type)

    def get_desktop_ordinal_for_window(self, hwnd):
        """Returns corresponding desktop ordinal of the window with provided hwnd.

        :param hwnd: window id
        :type hwnd: int
        :returns: int
        """
        return self.vdi.get_window_desktop(hwnd)[0]

    def get_desktops(self):
        """Returns list of virtual desktops.

        Returned list contains two-tuples of desktop numbers in order
        and their corresponding names. A name is formatted from "Desktop "
        translation forllowed by ordinal increased by 1.

        :returns: [(int, str)]
        """
        return [
            (i, "{} {}".format(Settings.DESKTOP_STR, i + 1))
            for (i, _a) in self.vdi.get_desktops()
        ]

    def get_last_active_popup(self, hwnd):
        """Helper function to return hwnd of last popup of window with provided hwnd.

        :param hwnd: window id
        :type hwnd: int
        :returns: int
        """
        return self.helpers._get_last_active_popup(hwnd)

    def get_package(self, hwnd):
        """Returns :class:`Package` holding needed package data from provided window id.

        :param hwnd: window id
        :type hwnd: int
        :var full_name: buffer holding package full name
        :type full_name: array of :class:`ctypes.c_wchar`
        :var package_info_reference: reference to package info structure pointer
        :type package_info_reference: int
        :var package_info_buffer: buffer holding reference to package info structure
        :type package_info_buffer: array of :class:`ctypes.c_char`
        :var package_info: structure holding package data
        :type package_info: :class:`PACKAGE_INFO`
        :returns: :class:`Package`
        """
        full_name = self._package_full_name_from_hwnd(hwnd)
        if not full_name:
            logging.info("get_package: hwnd {} has no full_name.".format(hwnd))
            return Package("")

        package_info_reference = self._package_info_reference_from_full_name(full_name)
        package_info_buffer = self._package_info_buffer_from_reference(
            package_info_reference
        )
        package_info = PACKAGE_INFO.from_buffer(package_info_buffer)
        self.helpers._close_package_info(package_info_reference.contents)
        return Package(package_info.path)

    def is_dwm_composition_enabled(self):
        """Helper function returning True if DWM composition is enabled in system.

        :var enabled: composition enabled or not value
        :type enabled: :class:`ctypes.wintypes.BOOL`
        :returns: Boolean
        """
        enabled = ctypes.wintypes.BOOL()
        self.helpers._dwm_is_composition_enabled(ctypes.byref(enabled))
        return enabled.value

    def move_window_to_desktop(self, hwnd, number):
        """Moves window with provided hwnd to desktop with provided ordinal.

        :param hwnd: window id
        :type hwnd: int
        :param number: desktop ordinal
        :type number: int
        :returns: int
        """
        return self.vdi.move_window_to_desktop(hwnd, number)

    def setup_thumbnail(self, from_hwnd, root_hwnd, rectangle):
        """Create, updates and returns handle of thumbnail of provided source window

        created in root window.

        :param from_hwnd: identifier of window to make thumbnail of
        :type from_hwnd: int
        :param root_hwnd: identifier of root window to make thumbnail in
        :type root_hwnd: int
        :param rectangle: area occupied by thumbnail
        :type rectangle: :class:`arrangeit.utils.Rectangle`
        :var thumbnail_id: id of created thumbnail
        :type thumbnail_id: :class:`ctypes.wintypes.HANDLE`
        :var ret_val: function returned value indicating error/success status
        :type ret_val: int
        :returns: :class:`ctypes.wintypes.HANDLE`
        """
        thumbnail_id = ctypes.wintypes.HANDLE()
        ret_val = self.helpers._dwm_register_thumbnail(
            root_hwnd, from_hwnd, ctypes.byref(thumbnail_id)
        )
        if ret_val != S_OK:
            logging.info(
                "setup_thumbnail: error -> {}".format(
                    str(ctypes.WinError(ctypes.get_last_error()))
                )
            )
            return None

        return self._update_thumbnail(thumbnail_id, rectangle)

    def title_info_state(self, hwnd, state):
        """Helper function to return title bar info state for window with provided hwnd.

        :param hwnd: window id
        :type hwnd: int
        :param state: title bar info state type
        :type state: int
        :var title_info: title bar information structure
        :type title_info: :class:`TITLEBARINFO`
        :var success: value indicating is call successful
        :type success: bool
        :returns: int
        """
        title_info = TITLEBARINFO()
        title_info.cbSize = ctypes.sizeof(title_info)
        success = self.helpers._get_titlebar_info(hwnd, ctypes.byref(title_info))
        return title_info.rgstate[0] & state if success else None

    def unregister_thumbnail(self, thumbnail_id):
        """Unregisters thumbnail with provided identifier.

        :param thumbnail_id: identifier of thumbnail to unregister
        :type thumbnail_id: :class:`ctypes.wintypes.HANDLE`
        :var ret_val: function returned value indicating error/success status
        :type ret_val: int
        :returns: :class:`ctypes.wintypes.HANDLE`
        """
        ret_val = self.helpers._dwm_unregister_thumbnail(thumbnail_id)
        if ret_val != S_OK:
            logging.info(
                "unregister_thumbnail: error -> {}".format(
                    str(ctypes.WinError(ctypes.get_last_error()))
                )
            )
            return True

    def window_info_extended_style(self, hwnd, style):
        """Helper function to return extended window style for window with given hwnd.

        :param hwnd: window id
        :type hwnd: int
        :param style: extended window style type
        :type style: int
        :var window_info: window information structure
        :type window_info: :class:`WINDOWINFO`
        :var success: value indicating is call successful
        :type success: bool
        :returns: int
        """
        window_info = WINDOWINFO()
        success = self.helpers._get_window_info(hwnd, ctypes.byref(window_info))
        return window_info.dwExStyle & style if success else None
