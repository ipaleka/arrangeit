import ctypes
import ctypes.wintypes
import logging

APPMODEL_ERROR_NO_PACKAGE = 15700
ERROR_SUCCESS = 0x0
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PACKAGE_FILTER_HEAD = 0x00000010

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

_open_package_info_by_full_name = _kernel32.OpenPackageInfoByFullName
_open_package_info_by_full_name.argtypes = (
    ctypes.wintypes.LPCWSTR,
    ctypes.c_uint32,
    ctypes.POINTER(PACKAGE_INFO_REFERENCE)
)
_open_package_info_by_full_name.restype = ctypes.wintypes.LONG

_get_package_info = _kernel32.GetPackageInfo
_get_package_info.argtypes = (
    PACKAGE_INFO_REFERENCE,
    ctypes.c_uint32,
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint32)
)
_get_package_info.restype = ctypes.wintypes.LONG

_close_package_info = _kernel32.ClosePackageInfo
_close_package_info.argtypes = (
    PACKAGE_INFO_REFERENCE,
)
_close_package_info.restype = ctypes.wintypes.LONG


def _package_full_name_from_handle(handle):
    """Returns full name of the package associated with provided process handle.

    :param hwnd: process handle
    :type hwnd: int
    """
    length = ctypes.c_uint()
    ret_val = _get_package_full_name(handle, ctypes.byref(length), None)
    if ret_val == APPMODEL_ERROR_NO_PACKAGE:
        logging.info(
            "_package_full_name_from_handle: handle {} has no package.".format(
                hex(handle)
            )
        )
        return None

    full_name = ctypes.create_unicode_buffer(length.value + 1)
    ret_val = _get_package_full_name(handle, ctypes.byref(length), full_name)
    if ret_val != ERROR_SUCCESS:
        err = ctypes.WinError(ctypes.get_last_error())
        logging.info("_package_full_name_from_handle: error -> {}".format(str(err)))
        return None

    return full_name


def package_info_reference_from_full_name(full_name):
    package_info_reference = ctypes.pointer(PACKAGE_INFO_REFERENCE())
    retval = _open_package_info_by_full_name(full_name, 0, package_info_reference)
    if retval != ERROR_SUCCESS:
        raise ctypes.WinError(ctypes.get_last_error())

    return package_info_reference


def package_info_buffer_from_reference(package_info_reference):
    length = ctypes.c_uint(0)
    count = ctypes.c_uint()

    retval = _get_package_info(
        package_info_reference.contents,  # package_info_reference is already a pointer. We want its content.
        PACKAGE_FILTER_HEAD,
        ctypes.byref(length),
        None,
        ctypes.byref(count),
    )
    if retval != ERROR_INSUFFICIENT_BUFFER:
        raise ctypes.WinError(ctypes.get_last_error())

    buffer = ctypes.create_string_buffer(length.value)
    buffer_bytes = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_uint8))
    retval = _get_package_info(
        package_info_reference.contents,
        PACKAGE_FILTER_HEAD,
        ctypes.byref(length),
        buffer_bytes,
        ctypes.byref(count),
    )
    if retval != ERROR_SUCCESS:
        raise ctypes.WinError(ctypes.get_last_error())

    return buffer, length


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


def get_child_with_different_pid(hwnd):
    pid = ctypes.wintypes.DWORD()
    _get_windows_thread_process_id(hwnd, ctypes.byref(pid))

    for child in enum_windows(hwnd, enum_children=True):
        child_pid = ctypes.wintypes.DWORD(0)
        _get_windows_thread_process_id(child, ctypes.byref(child_pid))
        if child_pid != pid:
            return child_pid

    return hwnd


ERROR_INSUFFICIENT_BUFFER = 0x7A

_get_package_id = _kernel32.GetPackageId
_get_package_id.argtypes = (
    ctypes.wintypes.HANDLE,
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.POINTER(ctypes.c_uint8),
)
_get_package_id.restype = ctypes.wintypes.LONG


def _package_id_from_handle(handle):
    length = ctypes.c_uint()

    ret_val = _get_package_id(handle, ctypes.byref(length), None)
    if ret_val == APPMODEL_ERROR_NO_PACKAGE:
        logging.info(
            "_package_id_from_handle: handle {} has no package.".format(hex(handle))
        )
        return None

    buffer = ctypes.create_string_buffer(length.value)
    buffer_bytes = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_uint8))
    ret_val = _get_package_id(handle, ctypes.byref(length), buffer_bytes)
    if ret_val != ERROR_SUCCESS:
        raise ctypes.WinError(ctypes.get_last_error())

    return buffer, length

_get_package_family_name = _kernel32.GetPackageFamilyName
_get_package_family_name.argtypes = (
    ctypes.wintypes.HANDLE,
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.wintypes.LPCWSTR,
)
_get_package_family_name.restype = ctypes.wintypes.LONG


def _package_family_name_from_handle(handle):
    length = ctypes.c_uint()
    ret_val = _get_package_family_name(handle, ctypes.byref(length), None)
    if ret_val == APPMODEL_ERROR_NO_PACKAGE:
        logging.info(
            "_get_package_family_name: handle {} has no package.".format(
                hex(handle)
            )
        )
        return None

    family_name = ctypes.create_unicode_buffer(length.value + 1)
    ret_val = _get_package_family_name(handle, ctypes.byref(length), family_name)
    if ret_val != ERROR_SUCCESS:
        err = ctypes.WinError(ctypes.get_last_error())
        logging.info("_get_package_family_name: error -> {}".format(str(err)))
        return None

    return family_name




def package_full_name_from_hwnd(hwnd):
    for child in enum_windows(hwnd, enum_children=True):
        child_pid = ctypes.wintypes.DWORD(0)
        _get_windows_thread_process_id(child, ctypes.byref(child_pid))
        hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, child_pid)
        full_name = _package_full_name_from_handle(hprocess)
        _close_handle(hprocess)
        if full_name is not None:
            return full_name


def print_family_names(hwnd):
    hprocess = None

    pid = ctypes.wintypes.DWORD()
    _get_windows_thread_process_id(hwnd, ctypes.byref(pid))

    hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)

    family_name = _package_family_name_from_handle(hprocess)
    if family_name is not None:        
        logging.info("family_name.value: {}".format(family_name.value))
    _close_handle(hprocess)

    for child in enum_windows(hwnd, enum_children=True):
        child_pid = ctypes.wintypes.DWORD(0)
        _get_windows_thread_process_id(child, ctypes.byref(child_pid))
        hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, child_pid)
        family_name = _package_family_name_from_handle(hprocess)
        if family_name is not None:        
            logging.info("family_name.value: {}".format(family_name.value))
            logging.info("pid != child_pid: {}".format(pid != child_pid))
            logging.info("     pid {} ; child_pid {}".format(pid, child_pid))
        _close_handle(hprocess)
    logging.info("=" * 79)


def print_package_ids(hwnd):
    hprocess = None

    pid = ctypes.wintypes.DWORD()
    _get_windows_thread_process_id(hwnd, ctypes.byref(pid))

    hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)

    package_id_buffer = _package_id_from_handle(hprocess)
    if package_id_buffer is not None:
        package_id = PACKAGE_ID.from_buffer(package_id_buffer[0])
        logging.info("package_id.name: {}".format(package_id.name))
    _close_handle(hprocess)

    for child in enum_windows(hwnd, enum_children=True):
        child_pid = ctypes.wintypes.DWORD(0)
        _get_windows_thread_process_id(child, ctypes.byref(child_pid))
        hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, child_pid)
        package_id_buffer = _package_id_from_handle(hprocess)
        if package_id_buffer is not None:
            package_id = PACKAGE_ID.from_buffer(package_id_buffer[0])
            logging.info("pid != child_pid: {}".format(pid != child_pid))
            logging.info("child package_id.name: {}".format(package_id.name))
            logging.info("     pid {} ; child_pid {}".format(pid, child_pid))
        _close_handle(hprocess)
    logging.info("=" * 79)

def print_package_full_names(hwnd):
    hprocess = None

    pid = ctypes.wintypes.DWORD()
    _get_windows_thread_process_id(hwnd, ctypes.byref(pid))

    hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)

    full_name = _package_full_name_from_handle(hprocess)
    if full_name is not None:
        logging.info("full_name.value: {}".format(full_name.value))
    _close_handle(hprocess)

    for child in enum_windows(hwnd, enum_children=True):
        child_pid = ctypes.wintypes.DWORD(0)
        _get_windows_thread_process_id(child, ctypes.byref(child_pid))
        hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, child_pid)
        full_name = _package_full_name_from_handle(hprocess)
        if full_name is not None:
            logging.info("child full_name.value: {}".format(full_name.value))
            logging.info("     pid {} ; child_pid {}".format(pid, child_pid))
        _close_handle(hprocess)
    logging.info("=" * 79)


def print_children(hwnd):
    hprocess = None

    logging.info("print_children: hwnd {} : hex {}".format(hwnd, hex(hwnd)))

    pid = ctypes.wintypes.DWORD()
    _get_windows_thread_process_id(hwnd, ctypes.byref(pid))

    logging.info("print_children: pid {}".format(pid))
    hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    logging.info("print_children: hprocess {} : hex {}".format(hprocess, hex(hprocess)))
    _close_handle(hprocess)
    logging.info("\n")

    for child in enum_windows(hwnd, enum_children=True):
        logging.info("print_children: child hwnd {} : hex {}".format(child, hex(child)))
        child_pid = ctypes.wintypes.DWORD(0)
        _get_windows_thread_process_id(child, ctypes.byref(child_pid))
        logging.info("print_children: child_pid {}".format(child_pid))
        hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, child_pid)
        logging.info(
            "print_children: child hprocess {} : hex {}".format(hprocess, hex(hprocess))
        )
        _close_handle(hprocess)
    logging.info("=" * 79)



_get_application_user_model_id = _kernel32.GetApplicationUserModelId
_get_application_user_model_id.argtypes = (
    ctypes.wintypes.HANDLE,
    ctypes.POINTER(ctypes.c_uint32),
    ctypes.wintypes.LPCWSTR,
)
_get_application_user_model_id.restype = ctypes.wintypes.LONG

APPMODEL_ERROR_NO_APPLICATION = 0x3D57
def _application_user_model_id_from_handle(handle):
    length = ctypes.c_uint()
    ret_val = _get_application_user_model_id(handle, ctypes.byref(length), None)
    if ret_val == APPMODEL_ERROR_NO_APPLICATION:
        logging.info(
            "_get_application_user_model_id: handle {} has no package.".format(
                hex(handle)
            )
        )
        return None

    model = ctypes.create_unicode_buffer(length.value + 1)
    ret_val = _get_application_user_model_id(handle, ctypes.byref(length), model)
    if ret_val != ERROR_SUCCESS:
        err = ctypes.WinError(ctypes.get_last_error())
        logging.info("_get_application_user_model_id: error -> {}".format(str(err)))
        return None

    return model


def print_model_ids(hwnd):
    hprocess = None

    pid = ctypes.wintypes.DWORD()
    _get_windows_thread_process_id(hwnd, ctypes.byref(pid))

    hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)

    model = _application_user_model_id_from_handle(hprocess)
    if model is not None:        
        logging.info("model.value: {}".format(model.value))
    _close_handle(hprocess)

    for child in enum_windows(hwnd, enum_children=True):
        child_pid = ctypes.wintypes.DWORD(0)
        _get_windows_thread_process_id(child, ctypes.byref(child_pid))
        hprocess = _open_process(PROCESS_QUERY_LIMITED_INFORMATION, False, child_pid)
        model = _application_user_model_id_from_handle(hprocess)
        if model is not None:        
            logging.info("model.value: {}".format(model.value))
            logging.info("pid != child_pid: {}".format(pid != child_pid))
            logging.info("     pid {} ; child_pid {}".format(pid, child_pid))
        _close_handle(hprocess)
    logging.info("=" * 79)


    # def get_package(self, hwnd):
    #     # from arrangeit.windows.apihelpers import print_children
    #     # print_children(hwnd)
    #     # from arrangeit.windows.apihelpers import print_package_ids
    #     # print_package_ids(hwnd)
    #     # from arrangeit.windows.apihelpers import print_family_names
    #     # print_family_names(hwnd)
    #     # from arrangeit.windows.apihelpers import print_model_ids
    #     # print_model_ids(hwnd)
    #     # from arrangeit.windows.apihelpers import print_package_full_names
    #     # print_package_full_names(hwnd)
    #     # hprocess = get_child_process_with_different_pid(hwnd)
    #     # if hprocess is None:
    #     #     logging.info(
    #     #         "get_package: hwnd {} has no different child process id.".format(hwnd)
    #     #     )
    #     #     return None

    #     # full_name = _package_full_name_from_handle(hprocess)
    #     # if not full_name:
    #     #     return
    #     # else:
    #     #     print(full_name.value)

    #     # hprocess = get_child_process_with_different_pid(hwnd)
    #     # if hprocess is None:
    #     #     logging.info(
    #     #         "get_package: hwnd {} has no different child process id.".format(hwnd)
    #     #     )
    #     #     return None

    #     full_name = package_full_name_from_hwnd(hwnd)
    #     if not full_name:
    #         logging.info(
    #             "get_package: hwnd {} has no full_name.".format(hwnd)
    #         )
    #         return
    #     # else:
    #     #     print(full_name.value)

    #     package_info_reference = package_info_reference_from_full_name(full_name)
    #     logging.info(
    #         "info reference: {} reserved.".format(package_info_reference.contents.reserved)
    #     )

    #     package_info_buffer, length = package_info_buffer_from_reference(package_info_reference)
    #     package_info = PACKAGE_INFO.from_buffer(package_info_buffer)
    #     logging.info(
    #         "package_info.packageFullName: {}".format(package_info.packageFullName)
    #     )

    #     manifest_file = os.path.join(package_info.path, "AppXManifest.xml")
    #     tree = ET.parse(manifest_file)
    #     root = tree.getroot()
    #     # schema = "http://schemas.microsoft.com/appx/2010/manifest"

    #     namespace = self.api.namespace_for_element(root)

    #     print(package_info.path)

    #     # app = root.iter("{}Applications".format(namespace))
    #     # print("## {} {} ".format(app.tag, app.attrib))
    #     sources = set()
    #     for prop in next(root.iter("{}Properties".format(namespace))).iter():
    #         if "Logo" in prop.tag:
    #             # print("Properties/Logo ## {} {} ".format(prop.tag, prop.attrib))
    #             sources.add(prop.text)

    #     for subelem in next(root.iter("{}Applications".format(namespace))).iter():
    #         # print("#### {} {} ".format(subelem.tag, subelem.attrib))
    #         if "VisualElements" in subelem.tag:
    #             # print("Applications/VisualElements #### {} {} ".format(subelem.tag, subelem.attrib))
    #             sources.add(subelem.attrib.get("Square44x44Logo"))
    #             sources.add(subelem.attrib.get("Square150x150Logo"))

    #         # MicrosoftEdgeSquare44x44.scale-100.png

    #     print(sources)
    #     print("\n")
    #     # Square150x150Logo and Square44x44Logo

    #     # for app in root.iter("{}Applications".format(namespace)):
    #     #     print("## {} ".format(app.text,))

    #     #     for subelem in app.iter():
    #     #         print("#### {} {} ".format(subelem.tag, subelem.attrib))

    #         # for visual in root.iter("{}VisualElements".format(namespace)):
    #         #     print("## {} {} ".format(visual.tag, visual.attrib))

    #     # print("{} {} ".format(root.tag, root.attrib))
    #     # for elem in root:
    #     #     print("## {} {} ".format(elem.tag, elem.attrib))
    #     #     for subelem in elem:
    #     #         print("#### {} {} ".format(subelem.tag, subelem.attrib))

    #     # _close_handle(hprocess)
    #     _close_package_info(package_info_reference.contents)

    #     # from arrangeit.windows.apihelpers import PACKAGE_ID
    #     # package_id_buffer = _package_id_from_handle(hprocess)
    #     # if package_id_buffer is not None:
    #     #     package_id = PACKAGE_ID.from_buffer(package_id_buffer[0])
    #     #     print("package_id.name:", package_id.name)

    #     # family_name = _package_family_name_from_handle(hprocess)
    #     # if not family_name:
    #     #     return
    #     # else:
    #     #     print(family_name.value)

    #     # full_name = _package_full_name_from_handle(hprocess)
    #     # if not full_name:
    #     #     return
    #     # else:
    #     #     print(full_name.value)    