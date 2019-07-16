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
from arrangeit.utils import open_image
from arrangeit.windows.utils import extract_name_from_bytes_path

APPMODEL_ERROR_NO_PACKAGE = 15700
ERROR_INSUFFICIENT_BUFFER = 0x7A
ERROR_SUCCESS = 0x0
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PACKAGE_FILTER_HEAD = 0x00000010

UWP_ICON_SUFFIXES = (
    ".targetsize-256_altform-fullcolor",
    ".targetsize-96_altform-unplated",
    ".scale-200",
    "",  # as is
    ".scale-100",
)


def platform_supports_packages():
    """Returns Boolean indicating if Windows version supports packages.

    :var version: platform version data
    :type version: named tuple
    :returns: Boolean
    """
    version = sys.getwindowsversion()
    if version.major > 6 or (version.major == 6 and version.minor > 1):
        return True
    return False


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
        ("win32conreatorVersion", ctypes.wintypes.DWORD),
    ]


_user32 = ctypes.WinDLL("user32", use_last_error=True)
_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
_psapi = ctypes.WinDLL("psapi", use_last_error=True)

WNDENUMPROC = ctypes.WINFUNCTYPE(
    ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM
)

_get_windows_thread_process_id = _user32.GetWindowThreadProcessId
_get_windows_thread_process_id.argtypes = (
    ctypes.wintypes.HWND,
    ctypes.POINTER(ctypes.wintypes.DWORD),
)
_get_windows_thread_process_id.restype = ctypes.wintypes.DWORD

_enum_windows = _user32.EnumWindows
_enum_windows.argtypes = (WNDENUMPROC, ctypes.wintypes.LPARAM)
_enum_windows.restype = ctypes.wintypes.BOOL

_enum_child_windows = _user32.EnumChildWindows
_enum_child_windows.argtypes = (
    ctypes.wintypes.HWND,
    WNDENUMPROC,
    ctypes.wintypes.LPARAM,
)
_enum_child_windows.restype = ctypes.wintypes.BOOL

_open_process = _kernel32.OpenProcess
_open_process.argtypes = (
    ctypes.wintypes.DWORD,
    ctypes.wintypes.BOOL,
    ctypes.wintypes.DWORD,
)
_open_process.restype = ctypes.wintypes.HANDLE

_get_process_image_file_name = _psapi.GetProcessImageFileNameA
_get_process_image_file_name.argtypes = (
    ctypes.wintypes.HANDLE,
    ctypes.wintypes.LPSTR,
    ctypes.wintypes.DWORD,
)
_get_process_image_file_name.restype = ctypes.wintypes.DWORD

_close_handle = _kernel32.CloseHandle
_close_handle.argtypes = (ctypes.wintypes.HANDLE,)
_close_handle.restype = ctypes.wintypes.BOOL

"""Windows 8.1 and Windows 10 specific API to retrieve UWP packages."""
if platform_supports_packages():
    _get_package_full_name = _kernel32.GetPackageFullName
    _get_package_full_name.argtypes = (
        ctypes.wintypes.HANDLE,
        ctypes.POINTER(ctypes.c_uint32),
        ctypes.wintypes.LPCWSTR,
    )
    _get_package_full_name.restype = ctypes.wintypes.LONG

    _open_package_info_by_full_name = _kernel32.OpenPackageInfoByFullName
    _open_package_info_by_full_name.argtypes = (
        ctypes.wintypes.LPCWSTR,
        ctypes.c_uint32,
        ctypes.POINTER(PACKAGE_INFO_REFERENCE),
    )
    _open_package_info_by_full_name.restype = ctypes.wintypes.LONG

    _get_package_info = _kernel32.GetPackageInfo
    _get_package_info.argtypes = (
        PACKAGE_INFO_REFERENCE,
        ctypes.c_uint32,
        ctypes.POINTER(ctypes.c_uint32),
        ctypes.POINTER(ctypes.c_uint8),
        ctypes.POINTER(ctypes.c_uint32),
    )
    _get_package_info.restype = ctypes.wintypes.LONG

    _close_package_info = _kernel32.ClosePackageInfo
    _close_package_info.argtypes = (PACKAGE_INFO_REFERENCE,)
    _close_package_info.restype = ctypes.wintypes.LONG


class Package(object):
    """Helper class for calls to Windows API.

    :var path: filesystem path to package directory
    :type path: str
    :var app_name: name of package's first application
    :type app_name: str
    :var icon: application icon
    :type icon: :class:`PIL.Image`
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

        TODO add call to this method if window is minimized

        :var root: root element of XML document
        :type root: :class:`xml.etree.ElementTree.Element`
        """
        root = self._get_manifest_root()
        self._setup_app_name(root)
        self._setup_icon(root)


class Api(object):
    """Helper class for calls to Windows API.

    :var packages: cached collection of packages distincted by windows handles
    :type packages: dictionary of :class:`Package`
    """

    packages = {}

    def _package_full_name_from_handle(self, handle):
        """Returns full name of the package associated with provided process handle.

        First we call :func:`_get_package_full_name` helper function to fill ``length``
        variable, and afterwards to fill ``full_name`` variable.

        :param handle: process handle
        :type handle: int
        :var length: buffer size in characters
        :type length: :class:`ctypes.c_uint`
        :var ret_val: function return value indicating error/success status
        :type ret_val: int
        :var full_name: buffer holding package full name
        :type full_name: array of :class:`ctypes.c_wchar`
        :returns: array of :class:`ctypes.c_wchar`
        """
        length = ctypes.c_uint()
        ret_val = _get_package_full_name(handle, ctypes.byref(length), None)
        if ret_val == APPMODEL_ERROR_NO_PACKAGE:
            return None

        full_name = ctypes.create_unicode_buffer(length.value + 1)
        ret_val = _get_package_full_name(handle, ctypes.byref(length), full_name)
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
            _get_windows_thread_process_id(child, ctypes.byref(child_pid))
            hprocess = _open_process(
                PROCESS_QUERY_LIMITED_INFORMATION, False, child_pid
            )
            full_name = self._package_full_name_from_handle(hprocess)
            _close_handle(hprocess)
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
        :var ret_val: function return value indicating error/success status
        :type ret_val: int
        :var buffer: buffer holding reference to package info structure
        :type buffer: array of :class:`ctypes.c_char`
        :var buffer_bytes: size of package info structure data
        :type buffer_bytes: array of bytes
        :returns: array of :class:`ctypes.c_char`
        """
        length = ctypes.c_uint(0)
        count = ctypes.c_uint()

        ret_val = _get_package_info(
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
        ret_val = _get_package_info(
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
        :var ret_val: function return value indicating error/success status
        :type ret_val: int
        :returns: int
        """
        package_info_reference = ctypes.pointer(PACKAGE_INFO_REFERENCE())
        ret_val = _open_package_info_by_full_name(full_name, 0, package_info_reference)
        if ret_val != ERROR_SUCCESS:
            logging.info(
                "_package_info_reference_from_full_name: error -> {}".format(
                    str(ctypes.WinError(ctypes.get_last_error()))
                )
            )
            return None

        return package_info_reference

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

        func = WNDENUMPROC(append_to_collection)
        if enum_children:
            _enum_child_windows(hwnd, func, 0)
        else:
            _enum_windows(func, 0)

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
        :var ret_val: return value indicating success for value > 0
        :type ret_val: int
        :returns: str
        """
        pid = ctypes.wintypes.DWORD()
        _get_windows_thread_process_id(hwnd, ctypes.byref(pid))
        hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        path_buffer = ctypes.create_string_buffer(500)
        ret_val = _get_process_image_file_name(hprocess, path_buffer, 500)
        _close_handle(hprocess)
        if ret_val:
            return extract_name_from_bytes_path(path_buffer.value)

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
        _close_package_info(package_info_reference.contents)
        return Package(package_info.path)


# _psapi = ctypes.WinDLL("psapi", use_last_error=True)
# _get_module_file_name_ex_a = _psapi.GetModuleFileNameExA
# _get_module_file_name_ex_a.argtypes = (
#     ctypes.wintypes.HANDLE,
#     ctypes.wintypes.HMODULE,
#     ctypes.wintypes.LPSTR,
#     ctypes.wintypes.DWORD,
# )
# _get_module_file_name_ex_a.restype = ctypes.wintypes.DWORD


# def _module_file_name(hwnd):

#     pid = ctypes.wintypes.DWORD()
#     _get_windows_thread_process_id(hwnd, ctypes.byref(pid))
#     hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
#     buffer = ctypes.create_string_buffer(800)
#     # buffer_bytes = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_uint8))
#     ret_val = _get_module_file_name_ex_a(hprocess, None, buffer, 800)
#     _close_handle(hprocess)
#     if ret_val:
#         return buffer.value

#     for child in Api().enum_windows(hwnd, enum_children=True):
#         child_pid = ctypes.wintypes.DWORD(0)
#         _get_windows_thread_process_id(child, ctypes.byref(child_pid))
#         hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, child_pid)

#         buffer = ctypes.create_string_buffer(255)
#         # buffer_bytes = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_uint8))
#         ret_val = _get_module_file_name_ex_a(hprocess, None, buffer, 255)

#         _close_handle(hprocess)
#         if ret_val:
#             return buffer.value
