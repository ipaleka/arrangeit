import ctypes
import ctypes.wintypes
from collections import namedtuple

import pytest
from PIL import Image

import arrangeit.windows.apihelpers as apihelpers
from arrangeit.settings import Settings
from arrangeit.windows.apihelpers import (
    PACKAGE_ID,
    PACKAGE_INFO,
    PACKAGE_INFO_REFERENCE,
    PACKAGE_SUBVERSION,
    PACKAGE_VERSION,
    PACKAGE_VERSION_U,
    TITLEBARINFO,
    WINDOWINFO,
    Api,
    Package,
    platform_supports_packages,
)

from .nested_helper import nested


## custom functions
class TestWindowsApihelpersCustomFunctions(object):
    """Testing class for :py:mod:`arrangeit.windows.apihelpers` custom functions."""

    def test_windows_apihelpers_platform_supports_packages_calls_getwindowsversion(
        self, mocker
    ):
        Version = namedtuple("version", ["major", "minor"])
        mocked = mocker.patch("arrangeit.windows.apihelpers.sys.getwindowsversion", return_value=Version(6, 1))
        platform_supports_packages()
        mocked.assert_called_once()
        mocked.assert_called_with()

    @pytest.mark.parametrize(
        "major,minor,expected",
        [(5, 1, False), (6, 1, False), (6, 2, True), (7, 0, True)],
    )
    def test_windows_apihelpers_platform_supports_packages_functionality(
        self, mocker, major, minor, expected
    ):
        Version = namedtuple("version", ["major", "minor"])
        mocker.patch(
            "arrangeit.windows.apihelpers.sys.getwindowsversion",
            return_value=Version(major, minor),
        )
        assert platform_supports_packages() == expected


## structures
class TestPACKAGE_SUBVERSION(object):
    """Testing class for :py:class:`arrangeit.windows.apihelpers.PACKAGE_SUBVERSION` class."""

    def test_windows_apihelpers_PACKAGE_SUBVERSION_is_Structure_subclass(self):
        assert issubclass(PACKAGE_SUBVERSION, ctypes.Structure)

    def test_windows_apihelpers_PACKAGE_SUBVERSION_inits__fields_(self):
        assert getattr(PACKAGE_SUBVERSION, "_fields_", None) is not None
        assert isinstance(PACKAGE_SUBVERSION._fields_, list)
        for elem in PACKAGE_SUBVERSION._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize(
        "field,typ",
        [
            ("Revision", ctypes.wintypes.USHORT),
            ("Build", ctypes.wintypes.USHORT),
            ("Minor", ctypes.wintypes.USHORT),
            ("Major", ctypes.wintypes.USHORT),
        ],
    )
    def test_windows_apihelpers_PACKAGE_SUBVERSION_field_and_type(self, field, typ):
        assert (field, typ) in PACKAGE_SUBVERSION._fields_


class TestPACKAGE_VERSION_U(object):
    """Testing class for :py:class:`arrangeit.windows.apihelpers.PACKAGE_VERSION_U` class."""

    def test_windows_apihelpers_PACKAGE_VERSION_U_is_Union_subclass(self):
        assert issubclass(PACKAGE_VERSION_U, ctypes.Union)

    def test_windows_apihelpers_PACKAGE_VERSION_U_inits__fields_(self):
        assert getattr(PACKAGE_VERSION_U, "_fields_", None) is not None
        assert isinstance(PACKAGE_VERSION_U._fields_, list)
        for elem in PACKAGE_VERSION_U._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize(
        "field,typ",
        [("Version", ctypes.c_uint64), ("DUMMYSTRUCTNAME", PACKAGE_SUBVERSION)],
    )
    def test_windows_apihelpers_PACKAGE_VERSION_U_field_and_type(self, field, typ):
        assert (field, typ) in PACKAGE_VERSION_U._fields_


class TestPACKAGE_VERSION(object):
    """Testing class for :py:class:`arrangeit.windows.apihelpers.PACKAGE_VERSION` class."""

    def test_windows_apihelpers_PACKAGE_VERSION_is_Structure_subclass(self):
        assert issubclass(PACKAGE_VERSION, ctypes.Structure)

    def test_windows_apihelpers_PACKAGE_VERSION_inits__fields_(self):
        assert getattr(PACKAGE_VERSION, "_fields_", None) is not None
        assert isinstance(PACKAGE_VERSION._fields_, list)
        for elem in PACKAGE_VERSION._fields_:
            assert isinstance(elem, tuple)

    def test_windows_apihelpers_PACKAGE_VERSION_inits__anonymous_(self):
        assert getattr(PACKAGE_VERSION, "_anonymous_", None) is not None
        assert isinstance(PACKAGE_VERSION._anonymous_, tuple)
        assert PACKAGE_VERSION._anonymous_[0] == "u"

    @pytest.mark.parametrize("field,typ", [("u", PACKAGE_VERSION_U)])
    def test_windows_apihelpers_PACKAGE_VERSION_field_and_type(self, field, typ):
        assert (field, typ) in PACKAGE_VERSION._fields_


class TestPACKAGE_ID(object):
    """Testing class for :py:class:`arrangeit.windows.apihelpers.PACKAGE_ID` class."""

    def test_windows_apihelpers_PACKAGE_ID_is_Structure_subclass(self):
        assert issubclass(PACKAGE_ID, ctypes.Structure)

    def test_windows_apihelpers_PACKAGE_ID_inits__fields_(self):
        assert getattr(PACKAGE_ID, "_fields_", None) is not None
        assert isinstance(PACKAGE_ID._fields_, list)
        for elem in PACKAGE_ID._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize(
        "field,typ",
        [
            ("reserved", ctypes.c_uint32),
            ("processorArchitecture", ctypes.c_uint32),
            ("version", PACKAGE_VERSION),
            ("name", ctypes.c_wchar_p),
            ("publisher", ctypes.c_wchar_p),
            ("resourceId", ctypes.c_wchar_p),
            ("publisherId", ctypes.c_wchar_p),
        ],
    )
    def test_windows_apihelpers_PACKAGE_ID_field_and_type(self, field, typ):
        assert (field, typ) in PACKAGE_ID._fields_


class TestPACKAGE_INFO(object):
    """Testing class for :py:class:`arrangeit.windows.apihelpers.PACKAGE_INFO` class."""

    def test_windows_apihelpers_PACKAGE_INFO_is_Structure_subclass(self):
        assert issubclass(PACKAGE_INFO, ctypes.Structure)

    def test_windows_apihelpers_PACKAGE_INFO_inits__fields_(self):
        assert getattr(PACKAGE_INFO, "_fields_", None) is not None
        assert isinstance(PACKAGE_INFO._fields_, list)
        for elem in PACKAGE_INFO._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize(
        "field,typ",
        [
            ("reserved", ctypes.c_uint32),
            ("flags", ctypes.c_uint32),
            ("path", ctypes.c_wchar_p),
            ("packageFullName", ctypes.c_wchar_p),
            ("packageFamilyName", ctypes.c_wchar_p),
            ("packageId", PACKAGE_ID),
        ],
    )
    def test_windows_apihelpers_PACKAGE_INFO_field_and_type(self, field, typ):
        assert (field, typ) in PACKAGE_INFO._fields_


class TestPACKAGE_INFO_REFERENCE(object):
    """Testing class for :py:class:`arrangeit.windows.apihelpers.PACKAGE_INFO_REFERENCE` class."""

    def test_windows_apihelpers_PACKAGE_INFO_REFERENCE_is_Structure_subclass(self):
        assert issubclass(PACKAGE_INFO_REFERENCE, ctypes.Structure)

    def test_windows_apihelpers_PACKAGE_INFO_REFERENCE_inits__fields_(self):
        assert getattr(PACKAGE_INFO_REFERENCE, "_fields_", None) is not None
        assert isinstance(PACKAGE_INFO_REFERENCE._fields_, list)
        for elem in PACKAGE_INFO_REFERENCE._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize("field,typ", [("reserved", ctypes.c_void_p)])
    def test_windows_apihelpers_PACKAGE_INFO_REFERENCE_field_and_type(self, field, typ):
        assert (field, typ) in PACKAGE_INFO_REFERENCE._fields_


class TestTITLEBARINFO(object):
    """Testing class for :py:class:`arrangeit.windows.apihelpers.TITLEBARINFO` class."""

    def test_windows_apihelpers_TITLEBARINFO_is_Structure_subclass(self):
        assert issubclass(TITLEBARINFO, ctypes.Structure)

    def test_windows_apihelpers_TITLEBARINFO_inits__fields_(self):
        assert getattr(TITLEBARINFO, "_fields_", None) is not None
        assert isinstance(TITLEBARINFO._fields_, list)
        for elem in TITLEBARINFO._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize(
        "field,typ",
        [
            ("cbSize", ctypes.wintypes.DWORD),
            ("rcTitleBar", ctypes.wintypes.RECT),
            ("rgstate", ctypes.wintypes.DWORD * 6),
        ],
    )
    def test_windows_apihelpers_TITLEBARINFO_field_and_type(self, field, typ):
        assert (field, typ) in TITLEBARINFO._fields_


class TestWINDOWINFO(object):
    """Testing class for :py:class:`arrangeit.windows.apihelpers.WINDOWINFO` class."""

    def test_windows_apihelpers_WINDOWINFO_is_Structure_subclass(self):
        assert issubclass(WINDOWINFO, ctypes.Structure)

    def test_windows_apihelpers_WINDOWINFO_inits__fields_(self):
        assert getattr(WINDOWINFO, "_fields_", None) is not None
        assert isinstance(WINDOWINFO._fields_, list)
        for elem in WINDOWINFO._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize(
        "field,typ",
        [
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
        ],
    )
    def test_windows_apihelpers_WINDOWINFO_field_and_type(self, field, typ):
        assert (field, typ) in WINDOWINFO._fields_


# windowsapi helper functions
class TestWindowsapiHelperFunctions(object):
    """Testing class for :py:mod:`arrangeit.windows.apihelpers` win32 functions."""

    # _user32
    def test_windows_apihelpers_sets_WinDLL_user32(self):
        assert apihelpers.__dict__.get("_user32") is not None
        assert isinstance(apihelpers._user32, ctypes.WinDLL)
        assert apihelpers._user32._name == "user32"

    # _kernel32
    def test_windows_apihelpers_sets_WinDLL_kernel32(self):
        assert apihelpers.__dict__.get("_kernel32") is not None
        assert isinstance(apihelpers._kernel32, ctypes.WinDLL)
        assert apihelpers._kernel32._name == "kernel32"

    # WNDENUMPROC
    def test_windows_apihelpers_defines_WNDENUMPROC(self):
        assert apihelpers.__dict__.get("WNDENUMPROC") is not None
        assert isinstance(apihelpers.WNDENUMPROC, type(ctypes._CFuncPtr))
        assert apihelpers.WNDENUMPROC._restype_ == ctypes.wintypes.BOOL
        assert apihelpers.WNDENUMPROC._argtypes_[0] == ctypes.wintypes.HWND
        assert apihelpers.WNDENUMPROC._argtypes_[1] == ctypes.wintypes.LPARAM

    # _get_windows_thread_process_id
    def test_windows_apihelpers_defines__get_windows_thread_process_id(self):
        assert apihelpers.__dict__.get("_get_windows_thread_process_id") is not None
        assert (
            apihelpers._get_windows_thread_process_id
            == apihelpers._user32.GetWindowThreadProcessId
        )

    def test_windows_apihelpers__get_windows_thread_process_id_argtypes_and_restype(
        self
    ):
        argtypes = apihelpers._get_windows_thread_process_id.argtypes
        assert argtypes[0] == ctypes.wintypes.HWND
        assert isinstance(argtypes[1], type(ctypes._Pointer))
        assert argtypes[1]._type_ == ctypes.wintypes.DWORD
        assert (
            apihelpers._get_windows_thread_process_id.restype == ctypes.wintypes.DWORD
        )

    # _enum_windows
    def test_windows_apihelpers_defines__enum_windows(self):
        assert apihelpers.__dict__.get("_enum_windows") is not None
        assert apihelpers._enum_windows == apihelpers._user32.EnumWindows

    def test_windows_apihelpers__enum_windows_argtypes_and_restype(self):
        assert apihelpers._enum_windows.argtypes == (
            apihelpers.WNDENUMPROC,
            ctypes.wintypes.LPARAM,
        )
        assert apihelpers._enum_windows.restype == ctypes.wintypes.BOOL

    # _enum_child_windows
    def test_windows_apihelpers_defines__enum_child_windows(self):
        assert apihelpers.__dict__.get("_enum_child_windows") is not None
        assert apihelpers._enum_child_windows == apihelpers._user32.EnumChildWindows

    def test_windows_apihelpers__enum_child_windows_argtypes_and_restype(self):
        assert apihelpers._enum_child_windows.argtypes == (
            (ctypes.wintypes.HWND, apihelpers.WNDENUMPROC, ctypes.wintypes.LPARAM)
        )
        assert apihelpers._enum_child_windows.restype == ctypes.wintypes.BOOL

    # _open_process
    def test_windows_apihelpers_defines__open_process(self):
        assert apihelpers.__dict__.get("_open_process") is not None
        assert apihelpers._open_process == apihelpers._kernel32.OpenProcess

    def test_windows_apihelpers__open_process_argtypes_and_restype(self):
        assert apihelpers._open_process.argtypes == (
            ctypes.wintypes.DWORD,
            ctypes.wintypes.BOOL,
            ctypes.wintypes.DWORD,
        )
        assert apihelpers._open_process.restype == ctypes.wintypes.HANDLE

    # _close_handle
    def test_windows_apihelpers_defines__close_handle(self):
        assert apihelpers.__dict__.get("_close_handle") is not None
        assert apihelpers._close_handle == apihelpers._kernel32.CloseHandle

    def test_windows_apihelpers__close_handle_argtypes_and_restype(self):
        assert apihelpers._close_handle.argtypes == (ctypes.wintypes.HANDLE,)
        assert apihelpers._close_handle.restype == ctypes.wintypes.BOOL


# windowsapi helper functions for Windows >= 8.1
@pytest.mark.skipif(not platform_supports_packages(), reason="Win 8 and 10 only")
class TestWindowsapiHelperFunctionsWin8and10(object):
    """Testing class for :py:mod:`arrangeit.windows.apihelpers` Win8 and 10 functions."""

    # _get_package_full_name
    def test_windows_apihelpers_defines__get_package_full_name(self):
        assert apihelpers.__dict__.get("_get_package_full_name") is not None
        assert (
            apihelpers._get_package_full_name == apihelpers._kernel32.GetPackageFullName
        )

    def test_windows_apihelpers__get_package_full_name_argtypes_and_restype(self):
        argtypes = apihelpers._get_package_full_name.argtypes
        assert argtypes[0] == ctypes.wintypes.HANDLE
        assert isinstance(argtypes[1], type(ctypes._Pointer))
        assert argtypes[1]._type_ == ctypes.c_uint32
        assert argtypes[2] == ctypes.wintypes.LPCWSTR

        assert apihelpers._get_package_full_name.restype == ctypes.wintypes.LONG

    # _open_package_info_by_full_name
    def test_windows_apihelpers_defines__open_package_info_by_full_name(self):
        assert apihelpers.__dict__.get("_open_package_info_by_full_name") is not None
        assert (
            apihelpers._open_package_info_by_full_name
            == apihelpers._kernel32.OpenPackageInfoByFullName
        )

    def test_windows_apihelpers__open_package_info_by_full_name_argtypes_and_restype(
        self
    ):
        argtypes = apihelpers._open_package_info_by_full_name.argtypes
        assert argtypes[0] == ctypes.wintypes.LPCWSTR
        assert argtypes[1] == ctypes.c_uint32
        assert isinstance(argtypes[2], type(ctypes._Pointer))
        assert argtypes[2]._type_ == PACKAGE_INFO_REFERENCE

        assert (
            apihelpers._open_package_info_by_full_name.restype == ctypes.wintypes.LONG
        )

    # _get_package_info
    def test_windows_apihelpers_defines__get_package_info(self):
        assert apihelpers.__dict__.get("_get_package_info") is not None
        assert apihelpers._get_package_info == apihelpers._kernel32.GetPackageInfo

    def test_windows_apihelpers__get_package_info_argtypes_and_restype(self):
        argtypes = apihelpers._get_package_info.argtypes

        assert argtypes[0] == PACKAGE_INFO_REFERENCE
        assert argtypes[1] == ctypes.c_uint32
        assert isinstance(argtypes[2], type(ctypes._Pointer))
        assert argtypes[2]._type_ == ctypes.c_uint32
        assert isinstance(argtypes[3], type(ctypes._Pointer))
        assert argtypes[3]._type_ == ctypes.c_uint8
        assert isinstance(argtypes[4], type(ctypes._Pointer))
        assert argtypes[4]._type_ == ctypes.c_uint32

        assert apihelpers._get_package_info.restype == ctypes.wintypes.LONG

    # _close_package_info
    def test_windows_apihelpers_defines__close_package_info(self):
        assert apihelpers.__dict__.get("_close_package_info") is not None
        assert apihelpers._close_package_info == apihelpers._kernel32.ClosePackageInfo

    def test_windows_apihelpers__close_package_info_argtypes_and_restype(self):
        assert apihelpers._close_package_info.argtypes[0] == PACKAGE_INFO_REFERENCE
        assert apihelpers._close_package_info.restype == ctypes.wintypes.LONG


# Package class
class TestWindowsapiPackage(object):
    """Testing class for :py:class:`arrangeit.windows.apihelpers.Package`."""

    # Package
    @pytest.mark.parametrize("attr", ["path", "app_name"])
    def test_apihelpers_Package_inits_empty_attr(self, attr):
        assert getattr(Package, attr) == ""

    def test_apihelpers_Package_inits_empty_icon(self):
        assert isinstance(Package.icon, Image.Image)

    # Package.__init__
    def test_apihelpers_Package__init__sets_path_attribute_from_provided(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        SAMPLE = "foobar"
        package = Package(SAMPLE)
        assert package.path == SAMPLE

    def test_apihelpers_Package__init__calls_setup_package(self, mocker):
        mocked = mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        Package()
        mocked.assert_called_once()
        mocked.assert_called_with()

    # Package._get_first_image
    def test_apihelpers_Package__get_first_image_calls_product(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        mocked = mocker.patch("arrangeit.windows.apihelpers.product")
        SAMPLE = ["a"]
        Package()._get_first_image(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE, apihelpers.UWP_ICON_SUFFIXES)

    def test_apihelpers_Package__get_first_image_calls_splitext(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        NAME = "foo"
        mocker.patch(
            "arrangeit.windows.apihelpers.product", return_value=[(NAME, "bar")]
        )
        mocker.patch("arrangeit.windows.apihelpers.Image")
        mocker.patch("os.path.join")
        mocked = mocker.patch("os.path.splitext")
        Package()._get_first_image(["b"])
        calls = [mocker.call(NAME)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_apihelpers_Package__get_first_image_calls_os_path_join(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        PATH = "foobar"
        NAME = "foo"
        SUFFIX = "bar"
        SPLIT = ("ABC", "DEF")
        mocker.patch("os.path.splitext", return_value=SPLIT)
        mocker.patch(
            "arrangeit.windows.apihelpers.product", return_value=[(NAME, SUFFIX)]
        )
        mocker.patch("arrangeit.windows.apihelpers.Image")
        mocked = mocker.patch("os.path.join")
        Package(PATH)._get_first_image(["c"])
        calls = [mocker.call(PATH, SPLIT[0] + SUFFIX + SPLIT[1])]
        mocked.assert_has_calls(calls, any_order=True)

    def test_apihelpers_Package__get_first_image_calls_os_path_exists(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        PATH = "foobar"
        NAME = "foo"
        SUFFIX = "bar"
        SPLIT = ("ABC", "DEF")
        mocker.patch("os.path.splitext", return_value=SPLIT)
        mocker.patch(
            "arrangeit.windows.apihelpers.product", return_value=[(NAME, SUFFIX)]
        )
        CHECK_PATH = SPLIT[0] + SUFFIX + SPLIT[1]
        mocker.patch("os.path.join", return_value=CHECK_PATH)
        mocked = mocker.patch("os.path.exists")
        mocker.patch("arrangeit.windows.apihelpers.open_image")
        Package(PATH)._get_first_image(["d"])
        calls = [mocker.call(CHECK_PATH)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_apihelpers_Package__get_first_image_calls_and_returns_resized_Image(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        PATH = "foobar"
        NAME = "foo"
        SUFFIX = "bar"
        SPLIT = ("ABC", "DEF")
        mocker.patch("os.path.splitext", return_value=SPLIT)
        mocker.patch(
            "arrangeit.windows.apihelpers.product", return_value=[(NAME, SUFFIX)]
        )
        CHECK_PATH = SPLIT[0] + SUFFIX + SPLIT[1]
        mocker.patch("os.path.join", return_value=CHECK_PATH)
        mocker.patch("os.path.exists", return_value=True)
        mocked = mocker.patch("arrangeit.windows.apihelpers.Image")
        returned = Package(PATH)._get_first_image(["e"])
        calls = [mocker.call(CHECK_PATH)]
        mocked.open.assert_has_calls(calls, any_order=True)
        calls = [mocker.call((Settings.ICON_SIZE, Settings.ICON_SIZE), mocked.BICUBIC)]
        mocked.open.return_value.resize.assert_has_calls(calls, any_order=True)
        assert returned == mocked.open.return_value.resize.return_value

    def test_apihelpers_Package__get_first_image_catches_exception(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        PATH = "foobar"
        NAME = "foo"
        SUFFIX = "bar"
        SPLIT = ("ABC", "DEF")
        mocker.patch("os.path.splitext", return_value=SPLIT)
        mocker.patch(
            "arrangeit.windows.apihelpers.product", return_value=[(NAME, SUFFIX)]
        )
        CHECK_PATH = SPLIT[0] + SUFFIX + SPLIT[1]
        mocker.patch("os.path.join", return_value=CHECK_PATH)
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("arrangeit.windows.apihelpers.Image.open", side_effect=IOError())
        mocked = mocker.patch("arrangeit.windows.apihelpers.open_image")
        returned = Package(PATH)._get_first_image(["f"])
        calls = [mocker.call("white.png")]
        mocked.assert_has_calls(calls, any_order=True)
        assert returned == mocked.return_value

    def test_apihelpers_Package__get_first_image_calls_open_image_if_not_exists(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        PATH = "foobar"
        NAME = "foo"
        SUFFIX = "bar"
        SPLIT = ("ABC", "DEF")
        mocker.patch("os.path.splitext", return_value=SPLIT)
        mocker.patch(
            "arrangeit.windows.apihelpers.product", return_value=[(NAME, SUFFIX)]
        )
        CHECK_PATH = SPLIT[0] + SUFFIX + SPLIT[1]
        mocker.patch("os.path.join", return_value=CHECK_PATH)
        mocker.patch("os.path.exists", return_value=False)
        mocked = mocker.patch("arrangeit.windows.apihelpers.open_image")
        returned = Package(PATH)._get_first_image(["g"])
        calls = [mocker.call("white.png")]
        mocked.assert_has_calls(calls, any_order=True)
        assert returned == mocked.return_value

    # Package._get_manifest_root
    def test_apihelpers_Package__get_manifest_root_calls_os_path_join(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        mocker.patch("xml.etree.ElementTree.parse")
        PATH = "foobar"
        mocked = mocker.patch("os.path.join")
        Package(PATH)._get_manifest_root()
        calls = [mocker.call(PATH, "AppXManifest.xml")]
        mocked.assert_has_calls(calls, any_order=True)

    def test_apihelpers_Package__get_manifest_root_calls_os_path_exists(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        SAMPLE = "foobar"
        mocker.patch("os.path.join", return_value=SAMPLE)
        mocked = mocker.patch("os.path.exists", return_value=False)
        Package()._get_manifest_root()
        calls = [mocker.call(SAMPLE)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_apihelpers_Package__get_manifest_root_returns_true_if_not_exists(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        mocker.patch("os.path.exists", return_value=False)
        returned = Package()._get_manifest_root()
        assert returned is True

    def test_apihelpers_Package__get_manifest_root_calls_parse(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        SAMPLE = "foobar1"
        mocker.patch("os.path.join", return_value=SAMPLE)
        mocker.patch("os.path.exists", return_value=True)
        mocked = mocker.patch("xml.etree.ElementTree.parse")
        Package()._get_manifest_root()
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE)

    def test_apihelpers_Package__get_manifest_root_calls_and_returns_getroot(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        mocker.patch("os.path.join")
        mocker.patch("os.path.exists", return_value=True)
        mocked = mocker.patch("xml.etree.ElementTree.parse")
        returned = Package()._get_manifest_root()
        mocked.return_value.getroot.assert_called_once()
        mocked.return_value.getroot.assert_called_with()
        assert returned == mocked.return_value.getroot.return_value

    # Package._namespace_for_element
    def test_apihelpers_Package__namespace_for_element_calls_re_match(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        ELEMENT = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.windows.apihelpers.re.match")
        Package()._namespace_for_element(ELEMENT)
        calls = [mocker.call(r"\{.*\}", ELEMENT.tag)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_apihelpers_Package__namespace_for_element_returns_first_group(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        MATCH = mocker.MagicMock()
        mocker.patch("arrangeit.windows.apihelpers.re.match", return_value=MATCH)
        returned = Package()._namespace_for_element(mocker.MagicMock())
        assert returned == MATCH.group(0)

    def test_apihelpers_Package__namespace_for_element_returns_empty_string(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        mocker.patch("arrangeit.windows.apihelpers.re.match", return_value=False)
        returned = Package()._namespace_for_element(mocker.MagicMock())
        assert returned == ""

    # Package._setup_app_name
    def test_apihelpers_Package__setup_app_name_calls__namespace_for_element(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        ROOT = mocker.MagicMock()
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers.Package._namespace_for_element"
        )
        Package()._setup_app_name(ROOT)
        calls = [mocker.call(ROOT)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_apihelpers_Package__setup_app_name_calls_root_iter(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        ROOT = mocker.MagicMock()
        NAMESPACE = "foo"
        mocker.patch(
            "arrangeit.windows.apihelpers.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        Package()._setup_app_name(ROOT)
        ROOT.iter.assert_called_once()
        ROOT.iter.assert_called_with("{}Identity".format(NAMESPACE))

    def test_apihelpers_Package__setup_app_name_calls_next(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        ROOT = mocker.MagicMock()
        NAMESPACE = "foo"
        mocker.patch(
            "arrangeit.windows.apihelpers.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.apihelpers.next")
        Package()._setup_app_name(ROOT)
        mocked.assert_called_once()
        mocked.assert_called_with(ROOT.iter.return_value)

    def test_apihelpers_Package__setup_app_name_calls_iter_on_next(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        ROOT = mocker.MagicMock()
        NAMESPACE = "foo"
        mocker.patch(
            "arrangeit.windows.apihelpers.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.apihelpers.next")
        Package()._setup_app_name(ROOT)
        mocked.return_value.iter.assert_called_once()
        mocked.return_value.iter.assert_called_with()

    def test_apihelpers_Package__setup_app_name_sets_app_name_attr(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        SAMPLE = "bar"
        IDENTITY = mocker.MagicMock()
        IDENTITY.attrib = {"Name": "foo.{}".format(SAMPLE)}
        NAMESPACE = "foo"
        mocker.patch(
            "arrangeit.windows.apihelpers.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.apihelpers.next")
        mocked.return_value.iter.return_value = [IDENTITY,]
        package = Package()
        package._setup_app_name(mocker.MagicMock())
        assert package.app_name == SAMPLE

    # Package._setup_icon
    def test_apihelpers_Package__setup_icon_calls__namespace_for_element(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        ROOT = mocker.MagicMock()
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers.Package._namespace_for_element"
        )
        Package()._setup_icon(ROOT)
        calls = [mocker.call(ROOT)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_apihelpers_Package__setup_icon_calls_root_iter(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        ROOT = mocker.MagicMock()
        NAMESPACE = "bar"
        mocker.patch(
            "arrangeit.windows.apihelpers.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        Package()._setup_icon(ROOT)
        calls = [mocker.call("{}Applications".format(NAMESPACE))]
        ROOT.iter.assert_has_calls(calls, any_order=True)

    def test_apihelpers_Package__setup_icon_calls_next(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        ROOT = mocker.MagicMock()
        NAMESPACE = "bar"
        mocker.patch(
            "arrangeit.windows.apihelpers.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.apihelpers.next")
        Package()._setup_icon(ROOT)
        calls = [mocker.call(ROOT.iter.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_apihelpers_Package__setup_icon_calls_iter_on_next(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        ROOT = mocker.MagicMock()
        NAMESPACE = "bar"
        mocker.patch(
            "arrangeit.windows.apihelpers.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.apihelpers.next")
        Package()._setup_icon(ROOT)
        calls = [mocker.call()]
        mocked.return_value.iter.assert_has_calls(calls, any_order=True)

    def test_apihelpers_Package__setup_icon_appends_once_to_sources_from_Applications(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        SAMPLE = "foo1bar"
        SUBELEM = mocker.MagicMock()
        SUBELEM.tag = "VisualElements"
        SUBELEM.attrib = {"Square44x44Logo": SAMPLE, "Square150x150Logo": SAMPLE}
        NAMESPACE = "barfoo"
        mocker.patch(
            "arrangeit.windows.apihelpers.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.apihelpers.next")
        mocked_first = mocker.patch("arrangeit.windows.apihelpers.Package._get_first_image")
        mocked.return_value.iter.return_value = [SUBELEM,]
        Package()._setup_icon(mocker.MagicMock())
        mocked_first.assert_called_with([SAMPLE,])

    def test_apihelpers_Package__setup_icon_appends_to_sources_from_Properties(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.Package.setup_package")
        SAMPLE = "foo1bar4"
        PROP = mocker.MagicMock()
        PROP.tag = "Logo"
        PROP.text = SAMPLE
        NAMESPACE = "barfoo"
        mocker.patch(
            "arrangeit.windows.apihelpers.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.apihelpers.next")
        mocked_first = mocker.patch("arrangeit.windows.apihelpers.Package._get_first_image")
        mocked.return_value.iter.return_value = [PROP,]
        package = Package()
        package._setup_icon(mocker.MagicMock())
        mocked_first.assert_called_with([SAMPLE,])
        assert package.icon == mocked_first.return_value

    # Package.setup_package
    def test_apihelpers_Package_setup_package_calls__get_manifest_root(self, mocker):
        mocked = mocker.patch("arrangeit.windows.apihelpers.Package._get_manifest_root")
        mocker.patch("arrangeit.windows.apihelpers.Package._setup_app_name")
        mocker.patch("arrangeit.windows.apihelpers.Package._setup_icon")
        package = Package()
        mocked.reset_mock()        
        package.setup_package()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_apihelpers_Package_setup_package_calls__setup_app_name(self, mocker):
        mocked_root = mocker.patch("arrangeit.windows.apihelpers.Package._get_manifest_root")
        mocked = mocker.patch("arrangeit.windows.apihelpers.Package._setup_app_name")
        mocker.patch("arrangeit.windows.apihelpers.Package._setup_icon")
        package = Package()
        mocked.reset_mock()        
        package.setup_package()
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_root.return_value)

    def test_apihelpers_Package_setup_package_calls__setup_icon(self, mocker):
        mocked_root = mocker.patch("arrangeit.windows.apihelpers.Package._get_manifest_root")
        mocker.patch("arrangeit.windows.apihelpers.Package._setup_app_name")
        mocked = mocker.patch("arrangeit.windows.apihelpers.Package._setup_icon")
        package = Package()
        mocked.reset_mock()
        package.setup_package()
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_root.return_value)

# Api class public methods
class TestWindowsapiApiPublic(object):
    """Testing class for :py:class:`arrangeit.windows.apihelpers.Api` public methods."""

    # Api
    @pytest.mark.parametrize("attr", ["packages"])
    def test_apihelpers_Api_inits_empty_attr(self, attr):
        assert getattr(Api, attr) == {}

    # enum_windows
    def test_apihelpers_Api_enum_windows_nested_append_to_collection(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.WNDENUMPROC")
        mocker.patch("arrangeit.windows.apihelpers._enum_windows")
        nested_func = nested(Api().enum_windows, "append_to_collection", hwnds=[])
        returned = nested_func("foo", None)
        assert returned is True

    def test_apihelpers_Api_enum_windows_calls_WNDENUMPROC(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers._enum_windows")
        mocked = mocker.patch("arrangeit.windows.apihelpers.WNDENUMPROC")
        Api().enum_windows()
        mocked.assert_called_once()

    def test_apihelpers_Api_enum_windows_calls__enum_windows(self, mocker):
        mocked_enum = mocker.patch("arrangeit.windows.apihelpers.WNDENUMPROC")
        mocked = mocker.patch("arrangeit.windows.apihelpers._enum_windows")
        Api().enum_windows()
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_enum.return_value, 0)

    def test_apihelpers_Api_enum_windows_calls__enum_child_windows(self, mocker):
        mocked_enum = mocker.patch("arrangeit.windows.apihelpers.WNDENUMPROC")
        mocked = mocker.patch("arrangeit.windows.apihelpers._enum_child_windows")
        SAMPLE = 1874
        Api().enum_windows(SAMPLE, enum_children=True)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE, mocked_enum.return_value, 0)

    def test_apihelpers_Api_enum_windows_returns_non_empty_list(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.WNDENUMPROC")
        mocker.patch("arrangeit.windows.apihelpers._enum_windows")
        assert isinstance(Api().enum_windows(), list)


# Api class public methods for Windows >= 8.1
@pytest.mark.skipif(not platform_supports_packages(), reason="Win 8 and 10 only")
class TestWindowsapiApiPublicWin8and10(object):
    """Testing class for :py:class:`arrangeit.windows.apihelpers.Api` Win8 and 10 public methods."""

    # get_package
    def test_apihelpers_Api_get_package_calls__package_full_name_from_hwnd(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.apihelpers.Package")
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_full_name_from_hwnd",
            return_value=False,
        )
        SAMPLE = 5241
        Api().get_package(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE)

    def test_apihelpers_Api_get_package_returns_empty_Package(self, mocker):
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_full_name_from_hwnd",
            return_value=False,
        )
        mocked = mocker.patch("arrangeit.windows.apihelpers.Package")
        SAMPLE = 5242
        returned = Api().get_package(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with("")
        assert returned == mocked.return_value

    def test_apihelpers_Api_get_package_calls__package_info_reference_from_full_name(
        self, mocker
    ):
        FULL_NAME = "foobar"
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_info_buffer_from_reference"
        )
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_full_name_from_hwnd",
            return_value=FULL_NAME,
        )
        mocker.patch("arrangeit.windows.apihelpers.PACKAGE_INFO")
        mocker.patch("arrangeit.windows.apihelpers._close_package_info")
        mocker.patch("arrangeit.windows.apihelpers.Package")
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_info_reference_from_full_name"
        )
        Api().get_package(5243)
        mocked.assert_called_once()
        mocked.assert_called_with(FULL_NAME)

    def test_apihelpers_Api_get_package_calls__package_info_buffer_from_reference(
        self, mocker
    ):
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_full_name_from_hwnd",
            return_value="foo",
        )
        mocked_ref = mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_info_reference_from_full_name"
        )
        mocker.patch("arrangeit.windows.apihelpers.PACKAGE_INFO")
        mocker.patch("arrangeit.windows.apihelpers._close_package_info")
        mocker.patch("arrangeit.windows.apihelpers.Package")
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_info_buffer_from_reference"
        )
        Api().get_package(5244)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_ref.return_value)

    def test_apihelpers_Api_get_package_calls_PACKAGE_INFO_from_buffer(self, mocker):
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_full_name_from_hwnd",
            return_value="foo",
        )
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_info_reference_from_full_name"
        )
        mocker.patch("arrangeit.windows.apihelpers.PACKAGE_INFO")
        mocker.patch("arrangeit.windows.apihelpers._close_package_info")
        mocker.patch("arrangeit.windows.apihelpers.Package")
        SAMPLE = 109
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_info_buffer_from_reference",
            return_value=SAMPLE,
        )
        mocked = mocker.patch("arrangeit.windows.apihelpers.PACKAGE_INFO")
        Api().get_package(5245)
        mocked.from_buffer.assert_called_once()
        mocked.from_buffer.assert_called_with(SAMPLE)

    def test_apihelpers_Api_get_package_calls__close_package_info(self, mocker):
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_full_name_from_hwnd",
            return_value="foo",
        )
        mocked_ref = mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_info_reference_from_full_name"
        )
        mocker.patch("arrangeit.windows.apihelpers.Package")
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_info_buffer_from_reference"
        )
        mocker.patch("arrangeit.windows.apihelpers.PACKAGE_INFO")
        mocked = mocker.patch("arrangeit.windows.apihelpers._close_package_info")
        Api().get_package(5246)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_ref.return_value.contents)

    def test_apihelpers_Api_get_package_calls_Package(self, mocker):
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_full_name_from_hwnd",
            return_value="foo",
        )
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_info_reference_from_full_name"
        )
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_info_buffer_from_reference"
        )
        mocked_info = mocker.patch("arrangeit.windows.apihelpers.PACKAGE_INFO")
        mocker.patch("arrangeit.windows.apihelpers._close_package_info")
        mocked = mocker.patch("arrangeit.windows.apihelpers.Package")
        returned = Api().get_package(5247)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_info.from_buffer.return_value.path)
        assert returned == mocked.return_value


# Api class private methods
@pytest.mark.skipif(not platform_supports_packages(), reason="Win 8 and 10 only")
class TestWindowsapiApiPrivateWin8and10(object):
    """Testing class for :py:class:`arrangeit.windows.apihelpers.Api` private methods."""

    # _package_full_name_from_handle
    def test_Api__package_full_name_from_handle_calls_first_time__get_package_full_name(
        self, mocker
    ):
        mocked_byref = mocker.patch("ctypes.byref")
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers._get_package_full_name", return_value=0
        )
        SAMPLE = 520
        Api()._package_full_name_from_handle(SAMPLE)
        calls = [mocker.call(SAMPLE, mocked_byref.return_value, None)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_full_name_from_handle_returns_None_for_no_package(
        self, mocker
    ):
        mocker.patch("ctypes.byref")
        mocker.patch(
            "arrangeit.windows.apihelpers._get_package_full_name",
            return_value=apihelpers.APPMODEL_ERROR_NO_PACKAGE,
        )
        assert Api()._package_full_name_from_handle(100) is None

    def test_Api__package_full_name_from_handle_calls_create_unicode_buffer(
        self, mocker
    ):
        mocker.patch("ctypes.byref")
        mocked_uint = mocker.patch("ctypes.c_uint")
        LENGTH = 10
        mocked_uint.return_value.value = LENGTH
        mocker.patch(
            "arrangeit.windows.apihelpers._get_package_full_name", return_value=0
        )
        mocked = mocker.patch("ctypes.create_unicode_buffer")
        Api()._package_full_name_from_handle(100)
        calls = [mocker.call(LENGTH + 1)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_full_name_from_handle_calls_again__get_package_full_name(
        self, mocker
    ):
        mocked_byref = mocker.patch("ctypes.byref")
        mocked_buffer = mocker.patch("ctypes.create_unicode_buffer")
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers._get_package_full_name", return_value=0
        )
        SAMPLE = 521
        Api()._package_full_name_from_handle(SAMPLE)
        calls = [
            mocker.call(SAMPLE, mocked_byref.return_value, mocked_buffer.return_value)
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_full_name_from_handle_returns_None_for_no_success(
        self, mocker
    ):
        mocker.patch("ctypes.byref")
        mocker.patch(
            "arrangeit.windows.apihelpers._get_package_full_name",
            side_effect=[0, "foo"],
        )
        assert Api()._package_full_name_from_handle(100) is None

    def test_Api__package_full_name_from_handle_returns_full_name(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch(
            "arrangeit.windows.apihelpers._get_package_full_name",
            side_effect=[0, apihelpers.ERROR_SUCCESS],
        )
        mocked_buffer = mocker.patch("ctypes.create_unicode_buffer")
        returned = Api()._package_full_name_from_handle(100)
        assert returned == mocked_buffer.return_value

    # _package_full_name_from_hwnd
    def test_Api__package_full_name_from_hwnd_calls_enum_windows(self, mocker):
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers.Api.enum_windows", return_value=()
        )
        mocked.reset_mock()
        SAMPLE = 2840
        Api()._package_full_name_from_hwnd(SAMPLE)
        calls = [mocker.call(SAMPLE, enum_children=True)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_full_name_from_hwnd_calls__wintypes_DWORD(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers._open_process")
        mocker.patch("arrangeit.windows.apihelpers._close_handle")
        mocker.patch("arrangeit.windows.apihelpers.Api._package_full_name_from_handle")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch(
            "arrangeit.windows.apihelpers.Api.enum_windows", return_value=(5841,)
        )
        mocker.patch("arrangeit.windows.apihelpers._get_windows_thread_process_id")
        Api()._package_full_name_from_hwnd(2842)
        calls = [mocker.call(0)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_full_name_from_hwnd_calls__get_windows_thread_process_id(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.apihelpers._open_process")
        mocker.patch("arrangeit.windows.apihelpers._close_handle")
        mocker.patch("arrangeit.windows.apihelpers.Api._package_full_name_from_handle")
        mocker.patch("ctypes.wintypes.DWORD")
        mocked_byref = mocker.patch("ctypes.byref")
        CHILD = 5840
        mocker.patch(
            "arrangeit.windows.apihelpers.Api.enum_windows", return_value=(CHILD,)
        )
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers._get_windows_thread_process_id"
        )
        Api()._package_full_name_from_hwnd(2843)
        calls = [mocker.call(CHILD, mocked_byref.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_full_name_from_hwnd_calls__open_process(self, mocker):
        mocked = mocker.patch("arrangeit.windows.apihelpers._open_process")
        mocked_dword = mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("arrangeit.windows.apihelpers._close_handle")
        mocker.patch("arrangeit.windows.apihelpers.Api._package_full_name_from_handle")
        mocker.patch("ctypes.byref")
        mocker.patch(
            "arrangeit.windows.apihelpers.Api.enum_windows", return_value=(5842,)
        )
        mocker.patch("arrangeit.windows.apihelpers._get_windows_thread_process_id")
        Api()._package_full_name_from_hwnd(2844)
        calls = [
            mocker.call(
                apihelpers.PROCESS_QUERY_LIMITED_INFORMATION,
                False,
                mocked_dword.return_value,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_full_name_from_hwnd_calls__package_full_name_from_handle(
        self, mocker
    ):
        mocked_process = mocker.patch("arrangeit.windows.apihelpers._open_process")
        mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("arrangeit.windows.apihelpers._close_handle")
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_full_name_from_handle"
        )
        mocker.patch("ctypes.byref")
        mocker.patch(
            "arrangeit.windows.apihelpers.Api.enum_windows", return_value=(5843,)
        )
        mocker.patch("arrangeit.windows.apihelpers._get_windows_thread_process_id")
        Api()._package_full_name_from_hwnd(2845)
        calls = [mocker.call(mocked_process.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_full_name_from_hwnd_calls__close_handle(self, mocker):
        mocked_process = mocker.patch("arrangeit.windows.apihelpers._open_process")
        mocker.patch("ctypes.wintypes.DWORD")
        mocked = mocker.patch("arrangeit.windows.apihelpers._close_handle")
        mocker.patch("arrangeit.windows.apihelpers.Api._package_full_name_from_handle")
        mocker.patch("ctypes.byref")
        mocked_api = mocker.patch(
            "arrangeit.windows.apihelpers.Api.enum_windows", return_value=(5844,)
        )
        mocked_api.reset_mock()
        mocker.patch("arrangeit.windows.apihelpers._get_windows_thread_process_id")
        Api()._package_full_name_from_hwnd(2846)
        calls = [mocker.call(mocked_process.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_full_name_from_hwnd_returns_full_name(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers._open_process")
        mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("arrangeit.windows.apihelpers._close_handle")
        FULL_NAME = "foobar"
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_full_name_from_handle",
            return_value=FULL_NAME,
        )
        mocker.patch("ctypes.byref")
        mocker.patch(
            "arrangeit.windows.apihelpers.Api.enum_windows", return_value=[5845]
        )
        mocker.patch("arrangeit.windows.apihelpers._get_windows_thread_process_id")
        returned = Api()._package_full_name_from_hwnd(2847)
        assert returned == FULL_NAME

    def test_Api__package_full_name_from_hwnd_returns_None(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers._open_process")
        mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("arrangeit.windows.apihelpers._close_handle")
        mocker.patch(
            "arrangeit.windows.apihelpers.Api._package_full_name_from_handle",
            return_value=None,
        )
        mocker.patch("ctypes.byref")
        mocker.patch(
            "arrangeit.windows.apihelpers.Api.enum_windows", return_value=[5845]
        )
        mocker.patch("arrangeit.windows.apihelpers._get_windows_thread_process_id")
        returned = Api()._package_full_name_from_hwnd(2847)
        assert returned is None

    # _package_info_buffer_from_reference
    def test_Api__package_info_buffer_from_reference_calls_first_time__get_package_info(
        self, mocker
    ):
        mocked_byref = mocker.patch("ctypes.byref")
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers._get_package_info", return_value=0
        )
        mocked_ref = mocker.MagicMock()
        Api()._package_info_buffer_from_reference(mocked_ref)
        calls = [
            mocker.call(
                mocked_ref.contents,
                apihelpers.PACKAGE_FILTER_HEAD,
                mocked_byref.return_value,
                None,
                mocked_byref.return_value,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_info_buffer_from_reference_returns_None_for_not_insufficient(
        self, mocker
    ):
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.apihelpers._get_package_info", return_value=0)
        assert Api()._package_info_buffer_from_reference(mocker.MagicMock()) is None

    def test_Api__package_info_buffer_from_reference_calls_create_string_buffer(
        self, mocker
    ):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.cast")
        mocked_uint = mocker.patch("ctypes.c_uint")
        LENGTH = 20
        mocked_uint.return_value.value = LENGTH
        mocker.patch(
            "arrangeit.windows.apihelpers._get_package_info",
            return_value=apihelpers.ERROR_INSUFFICIENT_BUFFER,
        )
        mocked = mocker.patch("ctypes.create_string_buffer")
        Api()._package_info_buffer_from_reference(mocker.MagicMock())
        calls = [mocker.call(LENGTH)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_info_buffer_from_reference_calls_cast(self, mocker):
        mocker.patch("ctypes.byref")
        mocked_buffer = mocker.patch("ctypes.create_string_buffer")
        mocker.patch(
            "arrangeit.windows.apihelpers._get_package_info",
            return_value=apihelpers.ERROR_INSUFFICIENT_BUFFER,
        )
        mocked = mocker.patch("ctypes.cast")
        Api()._package_info_buffer_from_reference(mocker.MagicMock())
        calls = [
            mocker.call(mocked_buffer.return_value, ctypes.POINTER(ctypes.c_uint8))
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_info_buffer_from_reference_calls_again__get_package_info(
        self, mocker
    ):
        mocked_byref = mocker.patch("ctypes.byref")
        mocker.patch("ctypes.create_string_buffer")
        mocked_bytes = mocker.patch("ctypes.cast")
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers._get_package_info",
            return_value=apihelpers.ERROR_INSUFFICIENT_BUFFER,
        )
        mocked_ref = mocker.MagicMock()
        Api()._package_info_buffer_from_reference(mocked_ref)
        calls = [
            mocker.call(
                mocked_ref.contents,
                apihelpers.PACKAGE_FILTER_HEAD,
                mocked_byref.return_value,
                mocked_bytes.return_value,
                mocked_byref.return_value,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_info_buffer_from_reference_returns_None_for_no_success(
        self, mocker
    ):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.create_string_buffer")
        mocker.patch("ctypes.cast")
        mocker.patch(
            "arrangeit.windows.apihelpers._get_package_info",
            side_effect=[apihelpers.ERROR_INSUFFICIENT_BUFFER, "foo"],
        )
        assert Api()._package_info_buffer_from_reference(mocker.MagicMock()) is None

    def test_Api__package_info_buffer_from_reference_returns_buffer(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.cast")
        mocker.patch(
            "arrangeit.windows.apihelpers._get_package_info",
            side_effect=[
                apihelpers.ERROR_INSUFFICIENT_BUFFER,
                apihelpers.ERROR_SUCCESS,
            ],
        )
        mocked_buffer = mocker.patch("ctypes.create_string_buffer")
        returned = Api()._package_info_buffer_from_reference(mocker.MagicMock())
        assert returned == mocked_buffer.return_value

    # _package_info_reference_from_full_name
    def test_Api__package_info_reference_from_full_name_calls_PACKAGE_INFO_REFERENCE(
        self, mocker
    ):
        mocker.patch("ctypes.pointer")
        mocked = mocker.patch("arrangeit.windows.apihelpers.PACKAGE_INFO_REFERENCE")
        mocker.patch(
            "arrangeit.windows.apihelpers._open_package_info_by_full_name",
            return_value=apihelpers.ERROR_SUCCESS,
        )
        Api()._package_info_reference_from_full_name("foobar")
        mocked.assert_called_once()
        calls = [mocker.call()]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_info_reference_from_full_name_calls_pointer(self, mocker):
        mocked = mocker.patch("ctypes.pointer")
        mocked_ref = mocker.patch("arrangeit.windows.apihelpers.PACKAGE_INFO_REFERENCE")
        mocker.patch(
            "arrangeit.windows.apihelpers._open_package_info_by_full_name",
            return_value=apihelpers.ERROR_SUCCESS,
        )
        Api()._package_info_reference_from_full_name("foobar")
        mocked.assert_called_once()
        calls = [mocker.call(mocked_ref.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_info_ref_from_full_name_calls__open_package_info_by_full_name(
        self, mocker
    ):
        mocked_pointer = mocker.patch("ctypes.pointer")
        mocker.patch("arrangeit.windows.apihelpers.PACKAGE_INFO_REFERENCE")
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers._open_package_info_by_full_name",
            return_value=apihelpers.ERROR_SUCCESS,
        )
        FULL_NAME = "foobar"
        Api()._package_info_reference_from_full_name(FULL_NAME)
        mocked.assert_called_once()
        calls = [mocker.call(FULL_NAME, 0, mocked_pointer.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_info_reference_from_full_name_returns_package_info_reference(
        self, mocker
    ):
        mocked = mocker.patch("ctypes.pointer")
        mocker.patch("arrangeit.windows.apihelpers.PACKAGE_INFO_REFERENCE")
        mocker.patch(
            "arrangeit.windows.apihelpers._open_package_info_by_full_name",
            return_value=apihelpers.ERROR_SUCCESS,
        )
        returned = Api()._package_info_reference_from_full_name("foobar")
        assert returned == mocked.return_value

    def test_Api__package_info_reference_from_full_name_returns_None(self, mocker):
        mocker.patch("ctypes.pointer")
        mocker.patch("arrangeit.windows.apihelpers.PACKAGE_INFO_REFERENCE")
        mocker.patch(
            "arrangeit.windows.apihelpers._open_package_info_by_full_name",
            return_value="foo",
        )
        returned = Api()._package_info_reference_from_full_name("foobar")
        assert returned is None
