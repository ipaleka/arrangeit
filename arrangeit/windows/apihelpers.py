import ctypes
import ctypes.wintypes
import logging

APPMODEL_ERROR_NO_PACKAGE = 15700
ERROR_SUCCESS = 0x0
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000


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

_close_handle = _kernel32.CloseHandle
_close_handle.argtypes = (ctypes.wintypes.HANDLE,)
_close_handle.restype = ctypes.wintypes.BOOL

_get_package_full_name = _kernel32.GetPackageFullName
_get_package_full_name.argtypes = (
    ctypes.wintypes.HANDLE,
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.wintypes.LPCWSTR,
)
_get_package_full_name.restype = ctypes.wintypes.LONG


def _package_full_name_from_handle(handle):
    """Returns full name of the package associated with provided process handle.

    :param hwnd: process handle
    :type hwnd: int
    """
    length = ctypes.c_uint()
    ret_val = _get_package_full_name(handle, ctypes.byref(length), None)
    if ret_val == APPMODEL_ERROR_NO_PACKAGE:
        logging.info(
            "_package_full_name_from_handle: handle {} has no package.".format(handle)
        )
        return None

    full_name = ctypes.create_unicode_buffer(length.value + 1)
    ret_val = _get_package_full_name(handle, ctypes.byref(length), full_name)
    if ret_val != ERROR_SUCCESS:
        err = ctypes.WinError(ctypes.get_last_error())
        logging.info("_package_full_name_from_handle: error -> {}".format(str(err)))
        return None

    return full_name


def enum_windows(hwnd=None, enum_children=False):
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
        hwnds.append(element)
        return True

    func = WNDENUMPROC(append_to_collection)
    if enum_children:
        _enum_child_windows(hwnd, func, 0)
    else:
        _enum_windows(func, 0)

    return hwnds


def get_child_process_with_different_pid(hwnd):
    """Returns first child process with different process id for the window

    identified by provided hwnd.

    :param hwnd: window id
    :type hwnd: int
    :var hprocess: process handle
    :type hprocess: int
    :var pid: process identifier
    :type pid: int
    :var child: child window identifier
    :type child: int
    :var child_pid: child process identifier
    :type child_pid: int
    :returns: int
    """
    hprocess = None

    pid = ctypes.wintypes.DWORD()
    _get_windows_thread_process_id(hwnd, ctypes.byref(pid))

    for child in enum_windows(hwnd, enum_children=True):
        child_pid = ctypes.wintypes.DWORD(0)
        _get_windows_thread_process_id(child, ctypes.byref(child_pid))
        if child_pid != pid:
            hprocess = _open_process(
                PROCESS_QUERY_LIMITED_INFORMATION, False, child_pid
            )
            break

    return hprocess
