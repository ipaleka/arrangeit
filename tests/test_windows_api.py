import ctypes
import ctypes.wintypes
from collections import namedtuple

import pytest
from PIL import Image

import arrangeit.windows.api as api
from arrangeit.settings import Settings
from arrangeit.windows.api import (
    DWM_THUMBNAIL_PROPERTIES,
    PACKAGE_ID,
    PACKAGE_INFO,
    PACKAGE_INFO_REFERENCE,
    PACKAGE_SUBVERSION,
    PACKAGE_VERSION,
    PACKAGE_VERSION_U,
    TITLEBARINFO,
    WINDOWINFO,
    Api,
    Helpers,
    Package,
    platform_supports_packages,
)

from .nested_helper import nested


## custom functions
class TestWindowsapiCustomFunctions(object):
    """Testing class for :py:mod:`arrangeit.windows.api` custom functions."""

    # platform_supports_packages
    def test_windows_api_platform_supports_packages_calls_getwindowsversion(
        self, mocker
    ):
        Version = namedtuple("version", ["major", "minor"])
        mocked = mocker.patch(
            "arrangeit.windows.api.sys.getwindowsversion", return_value=Version(6, 1)
        )
        platform_supports_packages()
        mocked.assert_called_once()
        mocked.assert_called_with()

    @pytest.mark.parametrize(
        "major,minor,expected",
        [(5, 1, False), (6, 1, False), (6, 2, True), (7, 0, True)],
    )
    def test_windows_api_platform_supports_packages_functionality(
        self, mocker, major, minor, expected
    ):
        Version = namedtuple("version", ["major", "minor"])
        mocker.patch(
            "arrangeit.windows.api.sys.getwindowsversion",
            return_value=Version(major, minor),
        )
        assert platform_supports_packages() == expected


## structures
class TestPACKAGE_SUBVERSION(object):
    """Testing class for :py:class:`arrangeit.windows.api.PACKAGE_SUBVERSION` class."""

    def test_windows_api_PACKAGE_SUBVERSION_is_Structure_subclass(self):
        assert issubclass(PACKAGE_SUBVERSION, ctypes.Structure)

    def test_windows_api_PACKAGE_SUBVERSION_inits__fields_(self):
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
    def test_windows_api_PACKAGE_SUBVERSION_field_and_type(self, field, typ):
        assert (field, typ) in PACKAGE_SUBVERSION._fields_


class TestPACKAGE_VERSION_U(object):
    """Testing class for :py:class:`arrangeit.windows.api.PACKAGE_VERSION_U` class."""

    def test_windows_api_PACKAGE_VERSION_U_is_Union_subclass(self):
        assert issubclass(PACKAGE_VERSION_U, ctypes.Union)

    def test_windows_api_PACKAGE_VERSION_U_inits__fields_(self):
        assert getattr(PACKAGE_VERSION_U, "_fields_", None) is not None
        assert isinstance(PACKAGE_VERSION_U._fields_, list)
        for elem in PACKAGE_VERSION_U._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize(
        "field,typ",
        [("Version", ctypes.c_uint64), ("DUMMYSTRUCTNAME", PACKAGE_SUBVERSION)],
    )
    def test_windows_api_PACKAGE_VERSION_U_field_and_type(self, field, typ):
        assert (field, typ) in PACKAGE_VERSION_U._fields_


class TestPACKAGE_VERSION(object):
    """Testing class for :py:class:`arrangeit.windows.api.PACKAGE_VERSION` class."""

    def test_windows_api_PACKAGE_VERSION_is_Structure_subclass(self):
        assert issubclass(PACKAGE_VERSION, ctypes.Structure)

    def test_windows_api_PACKAGE_VERSION_inits__fields_(self):
        assert getattr(PACKAGE_VERSION, "_fields_", None) is not None
        assert isinstance(PACKAGE_VERSION._fields_, list)
        for elem in PACKAGE_VERSION._fields_:
            assert isinstance(elem, tuple)

    def test_windows_api_PACKAGE_VERSION_inits__anonymous_(self):
        assert getattr(PACKAGE_VERSION, "_anonymous_", None) is not None
        assert isinstance(PACKAGE_VERSION._anonymous_, tuple)
        assert PACKAGE_VERSION._anonymous_[0] == "u"

    @pytest.mark.parametrize("field,typ", [("u", PACKAGE_VERSION_U)])
    def test_windows_api_PACKAGE_VERSION_field_and_type(self, field, typ):
        assert (field, typ) in PACKAGE_VERSION._fields_


class TestPACKAGE_ID(object):
    """Testing class for :py:class:`arrangeit.windows.api.PACKAGE_ID` class."""

    def test_windows_api_PACKAGE_ID_is_Structure_subclass(self):
        assert issubclass(PACKAGE_ID, ctypes.Structure)

    def test_windows_api_PACKAGE_ID_inits__fields_(self):
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
    def test_windows_api_PACKAGE_ID_field_and_type(self, field, typ):
        assert (field, typ) in PACKAGE_ID._fields_


class TestPACKAGE_INFO(object):
    """Testing class for :py:class:`arrangeit.windows.api.PACKAGE_INFO` class."""

    def test_windows_api_PACKAGE_INFO_is_Structure_subclass(self):
        assert issubclass(PACKAGE_INFO, ctypes.Structure)

    def test_windows_api_PACKAGE_INFO_inits__fields_(self):
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
    def test_windows_api_PACKAGE_INFO_field_and_type(self, field, typ):
        assert (field, typ) in PACKAGE_INFO._fields_


class TestPACKAGE_INFO_REFERENCE(object):
    """Testing class for :py:class:`arrangeit.windows.api.PACKAGE_INFO_REFERENCE` class."""

    def test_windows_api_PACKAGE_INFO_REFERENCE_is_Structure_subclass(self):
        assert issubclass(PACKAGE_INFO_REFERENCE, ctypes.Structure)

    def test_windows_api_PACKAGE_INFO_REFERENCE_inits__fields_(self):
        assert getattr(PACKAGE_INFO_REFERENCE, "_fields_", None) is not None
        assert isinstance(PACKAGE_INFO_REFERENCE._fields_, list)
        for elem in PACKAGE_INFO_REFERENCE._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize("field,typ", [("reserved", ctypes.c_void_p)])
    def test_windows_api_PACKAGE_INFO_REFERENCE_field_and_type(self, field, typ):
        assert (field, typ) in PACKAGE_INFO_REFERENCE._fields_


class TestTITLEBARINFO(object):
    """Testing class for :py:class:`arrangeit.windows.api.TITLEBARINFO` class."""

    def test_windows_api_TITLEBARINFO_is_Structure_subclass(self):
        assert issubclass(TITLEBARINFO, ctypes.Structure)

    def test_windows_api_TITLEBARINFO_inits__fields_(self):
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
    def test_windows_api_TITLEBARINFO_field_and_type(self, field, typ):
        assert (field, typ) in TITLEBARINFO._fields_


class TestWINDOWINFO(object):
    """Testing class for :py:class:`arrangeit.windows.api.WINDOWINFO` class."""

    def test_windows_api_WINDOWINFO_is_Structure_subclass(self):
        assert issubclass(WINDOWINFO, ctypes.Structure)

    def test_windows_api_WINDOWINFO_inits__fields_(self):
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
            ("wCreatorVersion", ctypes.wintypes.DWORD),
        ],
    )
    def test_windows_api_WINDOWINFO_field_and_type(self, field, typ):
        assert (field, typ) in WINDOWINFO._fields_


class TestDWM_THUMBNAIL_PROPERTIES(object):
    """Testing class for :py:class:`arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES` class."""

    def test_windows_api_DWM_THUMBNAIL_PROPERTIES_is_Structure_subclass(self):
        assert issubclass(DWM_THUMBNAIL_PROPERTIES, ctypes.Structure)

    def test_windows_api_DWM_THUMBNAIL_PROPERTIES_inits__fields_(self):
        assert getattr(DWM_THUMBNAIL_PROPERTIES, "_fields_", None) is not None
        assert isinstance(DWM_THUMBNAIL_PROPERTIES._fields_, list)
        for elem in DWM_THUMBNAIL_PROPERTIES._fields_:
            assert isinstance(elem, tuple)

    @pytest.mark.parametrize(
        "field,typ",
        [
            ("dwFlags", ctypes.wintypes.DWORD),
            ("rcDestination", ctypes.wintypes.RECT),
            ("rcSource", ctypes.wintypes.RECT),
            ("opacity", ctypes.wintypes.BYTE),
            ("fVisible", ctypes.wintypes.BOOL),
            ("fSourceClientAreaOnly", ctypes.wintypes.BOOL),
        ],
    )
    def test_windows_api_DWM_THUMBNAIL_PROPERTIES_field_and_type(self, field, typ):
        assert (field, typ) in DWM_THUMBNAIL_PROPERTIES._fields_


# Helpers class
class TestWindowsApiHelpersCommon(object):
    """Testing class for :class:`arrangeit.windows.api.Helpers` common methods."""

    # Helpers.__init__
    def test_windows_api_Helpers___init___calls__setup_base(self, mocker):
        mocked = mocker.patch("arrangeit.windows.api.Helpers._setup_base")
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        Helpers()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_windows_api_Helpers___init___calls__setup_common_helpers(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_base")
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocked = mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        Helpers()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_windows_api_Helpers___init___calls_platform_supports_packages(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_base")
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocked = mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        Helpers()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_windows_api_Helpers___init___calls__setup_thumbnail_helpers(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_base")
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=True
        )
        mocked = mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        Helpers()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_windows_api_Helpers___init___calls__setup_win8_helpers(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_base")
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=True
        )
        mocked = mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        Helpers()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_windows_api_Helpers___init__not_calling__setup_win8_helpers(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_base")
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocked = mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        Helpers()
        mocked.assert_not_called()

    # _setup_base
    def test_windows_api_Helpers__setup_base_sets_WinDLL_user32(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        assert isinstance(helpers._user32, ctypes.WinDLL)
        assert helpers._user32._name == "user32"

    def test_windows_api_Helpers__setup_base_sets_WinDLL_kernel32(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        assert isinstance(helpers._kernel32, ctypes.WinDLL)
        assert helpers._kernel32._name == "kernel32"

    def test_windows_api_Helpers__setup_base_sets_WinDLL_psapi(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        assert isinstance(helpers._psapi, ctypes.WinDLL)
        assert helpers._psapi._name == "psapi"

    def test_windows_api_Helpers__setup_base_sets_WinDLL_dwmapi(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        assert isinstance(helpers._dwmapi, ctypes.WinDLL)
        assert helpers._dwmapi._name == "dwmapi"

    def test_windows_api_Helpers__setup_base_sets_WNDENUMPROC(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        assert isinstance(helpers.WNDENUMPROC, type(ctypes._CFuncPtr))
        assert helpers.WNDENUMPROC._restype_ == ctypes.wintypes.BOOL
        assert helpers.WNDENUMPROC._argtypes_[0] == ctypes.wintypes.HWND
        assert helpers.WNDENUMPROC._argtypes_[1] == ctypes.wintypes.LPARAM

    # Helpers._setup_helper
    def test_windows_api_Helpers__setup_helper_returns_attr_method(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        name = "foobar"
        mocked_helper = mocker.MagicMock()
        mocked_section = mocker.MagicMock()
        mocked_section.foobar = mocked_helper
        returned = helpers._setup_helper(mocked_section, name, 0, 0)
        assert returned == mocked_helper

    def test_windows_api_Helpers__setup_helper_sets_argtypes(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        mocked_argtypes = mocker.MagicMock()
        returned = helpers._setup_helper(
            mocker.MagicMock(), "barfoo", mocked_argtypes, 0
        )
        assert returned.argtypes == mocked_argtypes

    def test_windows_api_Helpers__setup_helper_sets_restype(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        mocked_restype = mocker.MagicMock()
        returned = helpers._setup_helper(
            mocker.MagicMock(), "barfoo1", 0, mocked_restype
        )
        assert returned.restype == mocked_restype

    # _setup_common_helpers
    def test_windows_api_Helpers__setup_common_helpers__get_ancestor(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert (
            helpers._get_ancestor == helpers._user32.GetAncestor
        )
        argtypes = helpers._get_ancestor.argtypes
        assert argtypes == (ctypes.wintypes.HWND, ctypes.wintypes.UINT)
        assert helpers._get_ancestor.restype == ctypes.wintypes.HWND

    def test_windows_api_Helpers__setup_common_helpers__get_last_active_popup(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert (
            helpers._get_last_active_popup == helpers._user32.GetLastActivePopup
        )
        argtypes = helpers._get_last_active_popup.argtypes
        assert argtypes == (ctypes.wintypes.HWND, )
        assert helpers._get_last_active_popup.restype == ctypes.wintypes.HWND

    def test_windows_api_Helpers__setup_common_helpers__get_titlebar_info(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert (
            helpers._get_titlebar_info == helpers._user32.GetTitleBarInfo
        )
        argtypes = helpers._get_titlebar_info.argtypes
        assert argtypes[0] == ctypes.wintypes.HWND
        assert isinstance(argtypes[1], type(ctypes._Pointer))
        assert argtypes[1]._type_ == TITLEBARINFO
        assert helpers._get_titlebar_info.restype == ctypes.wintypes.BOOL

    def test_windows_api_Helpers__setup_common_helpers__get_window_info(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert (
            helpers._get_window_info == helpers._user32.GetWindowInfo
        )
        argtypes = helpers._get_window_info.argtypes
        assert argtypes[0] == ctypes.wintypes.HWND
        assert isinstance(argtypes[1], type(ctypes._Pointer))
        assert argtypes[1]._type_ == WINDOWINFO
        assert helpers._get_window_info.restype == ctypes.wintypes.BOOL

    def test_windows_api_Helpers__setup_common__get_windows_thread_process_id(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert (
            helpers._get_windows_thread_process_id
            == helpers._user32.GetWindowThreadProcessId
        )
        argtypes = helpers._get_windows_thread_process_id.argtypes
        assert argtypes[0] == ctypes.wintypes.HWND
        assert isinstance(argtypes[1], type(ctypes._Pointer))
        assert argtypes[1]._type_ == ctypes.wintypes.DWORD
        assert helpers._get_windows_thread_process_id.restype == ctypes.wintypes.DWORD

    def test_windows_api_Helpers__setup_common_helpers__enum_windows(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert helpers._enum_windows == helpers._user32.EnumWindows
        argtypes = helpers._enum_windows.argtypes
        assert argtypes == (helpers.WNDENUMPROC, ctypes.wintypes.LPARAM)
        assert helpers._enum_windows.restype == ctypes.wintypes.BOOL

    def test_windows_api_Helpers__setup_common_helpers__enum_child_windows(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert helpers._enum_child_windows == helpers._user32.EnumChildWindows
        argtypes = helpers._enum_child_windows.argtypes
        assert argtypes == (
            ctypes.wintypes.HWND,
            helpers.WNDENUMPROC,
            ctypes.wintypes.LPARAM,
        )
        assert helpers._enum_child_windows.restype == ctypes.wintypes.BOOL

    def test_windows_api_Helpers__setup_common_helpers__open_process(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert helpers._open_process == helpers._kernel32.OpenProcess
        argtypes = helpers._open_process.argtypes
        assert argtypes == (
            ctypes.wintypes.DWORD,
            ctypes.wintypes.BOOL,
            ctypes.wintypes.DWORD,
        )
        assert helpers._open_process.restype == ctypes.wintypes.HANDLE

    def test_windows_api_Helpers__setup_common_helpers__close_handle(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert helpers._close_handle == helpers._kernel32.CloseHandle
        argtypes = helpers._close_handle.argtypes
        assert argtypes == (ctypes.wintypes.HANDLE,)
        assert helpers._close_handle.restype == ctypes.wintypes.BOOL

    def test_windows_api_Helpers__setup_common_helpers__get_process_image_file_name(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert (
            helpers._get_process_image_file_name
            == helpers._psapi.GetProcessImageFileNameA
        )
        argtypes = helpers._get_process_image_file_name.argtypes
        assert argtypes == (
            ctypes.wintypes.HANDLE,
            ctypes.wintypes.LPSTR,
            ctypes.wintypes.DWORD,
        )
        assert helpers._get_process_image_file_name.restype == ctypes.wintypes.DWORD

    def test_windows_api_Helpers__setup_common_helpers__dwm_get_window_attribute(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert (
            helpers._dwm_get_window_attribute == helpers._dwmapi.DwmGetWindowAttribute
        )
        argtypes = helpers._dwm_get_window_attribute.argtypes
        assert argtypes == (
            ctypes.wintypes.HWND,
            ctypes.wintypes.DWORD,
            ctypes.wintypes.LPVOID,
            ctypes.wintypes.DWORD,
        )
        assert helpers._dwm_get_window_attribute.restype == ctypes.wintypes.DWORD

    # _setup_thumbnail_helpers
    def test_windows_api_Helpers__setup_thumbnail_helpers__dwm_register_thumbnail(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_thumbnail_helpers()
        assert helpers._dwm_register_thumbnail == helpers._dwmapi.DwmRegisterThumbnail
        argtypes = helpers._dwm_register_thumbnail.argtypes
        assert argtypes[0] == ctypes.wintypes.HANDLE
        assert argtypes[1] == ctypes.wintypes.HANDLE
        assert isinstance(argtypes[2], type(ctypes._Pointer))
        assert argtypes[2]._type_ == ctypes.wintypes.HANDLE
        assert helpers._dwm_register_thumbnail.restype == ctypes.wintypes.DWORD

    def test_windows_api_Helpers__setup_thumbnail_help__dwm_update_thumbnail_properties(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_thumbnail_helpers()
        assert (
            helpers._dwm_update_thumbnail_properties
            == helpers._dwmapi.DwmUpdateThumbnailProperties
        )
        argtypes = helpers._dwm_update_thumbnail_properties.argtypes
        assert argtypes[0] == ctypes.wintypes.HANDLE
        assert isinstance(argtypes[1], type(ctypes._Pointer))
        assert argtypes[1]._type_ == DWM_THUMBNAIL_PROPERTIES
        assert helpers._dwm_update_thumbnail_properties.restype == ctypes.wintypes.DWORD

    def test_windows_api_Helpers__setup_thumbnail_helpers__dwm_unregister_thumbnail(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_thumbnail_helpers()
        assert (
            helpers._dwm_unregister_thumbnail == helpers._dwmapi.DwmUnregisterThumbnail
        )
        argtypes = helpers._dwm_unregister_thumbnail.argtypes
        assert argtypes == (ctypes.wintypes.HANDLE,)
        assert helpers._dwm_unregister_thumbnail.restype == ctypes.wintypes.DWORD


# windows.api.Helpers functions for Windows >= 8.1
@pytest.mark.skipif(not platform_supports_packages(), reason="Win 8 and 10 only")
class TestWindowsApiHelpersWin8(object):
    """Testing class for :class:`arrangeit.windows.api.Helpers` Win8+ functions."""

    # _setup_win8_helpers
    def test_windows_api_Helpers__setup_win8_helpers__get_package_full_name(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        helpers = Helpers()
        helpers._setup_win8_helpers()
        assert helpers._get_package_full_name == helpers._kernel32.GetPackageFullName
        argtypes = helpers._get_package_full_name.argtypes
        assert argtypes[0] == ctypes.wintypes.HANDLE
        assert isinstance(argtypes[1], type(ctypes._Pointer))
        assert argtypes[1]._type_ == ctypes.c_uint32
        assert argtypes[2] == ctypes.wintypes.LPCWSTR
        assert helpers._get_package_full_name.restype == ctypes.wintypes.LONG

    def test_windows_api_Helpers__setup_win8_helpers__open_package_info_by_full_name(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        helpers = Helpers()
        helpers._setup_win8_helpers()
        assert (
            helpers._open_package_info_by_full_name
            == helpers._kernel32.OpenPackageInfoByFullName
        )
        argtypes = helpers._open_package_info_by_full_name.argtypes
        assert argtypes[0] == ctypes.wintypes.LPCWSTR
        assert argtypes[1] == ctypes.c_uint32
        assert isinstance(argtypes[2], type(ctypes._Pointer))
        assert argtypes[2]._type_ == PACKAGE_INFO_REFERENCE
        assert helpers._open_package_info_by_full_name.restype == ctypes.wintypes.LONG

    def test_windows_api_Helpers__setup_win8_helpers__get_package_info(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        helpers = Helpers()
        helpers._setup_win8_helpers()
        assert helpers._get_package_info == helpers._kernel32.GetPackageInfo
        argtypes = helpers._get_package_info.argtypes
        assert argtypes[0] == PACKAGE_INFO_REFERENCE
        assert argtypes[1] == ctypes.c_uint32
        assert isinstance(argtypes[2], type(ctypes._Pointer))
        assert argtypes[2]._type_ == ctypes.c_uint32
        assert isinstance(argtypes[3], type(ctypes._Pointer))
        assert argtypes[3]._type_ == ctypes.c_uint8
        assert isinstance(argtypes[4], type(ctypes._Pointer))
        assert argtypes[4]._type_ == ctypes.c_uint32
        assert helpers._get_package_info.restype == ctypes.wintypes.LONG

    def test_windows_api_Helpers__setup_win8_helpers__close_package_info(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_common_helpers")
        helpers = Helpers()
        helpers._setup_win8_helpers()
        assert helpers._close_package_info == helpers._kernel32.ClosePackageInfo
        argtypes = helpers._close_package_info.argtypes
        assert argtypes == (PACKAGE_INFO_REFERENCE,)
        assert helpers._close_package_info.restype == ctypes.wintypes.LONG


# Package class
class TestWindowsApiPackage(object):
    """Testing class for :py:class:`arrangeit.windows.api.Package`."""

    # Package
    @pytest.mark.parametrize("attr", ["path", "app_name"])
    def test_api_Package_inits_empty_attr(self, attr):
        assert getattr(Package, attr) == ""

    def test_api_Package_inits_empty_icon(self):
        assert isinstance(Package.icon, Image.Image)

    # Package.__init__
    def test_api_Package__init__sets_path_attribute_from_provided(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        SAMPLE = "foobar"
        package = Package(SAMPLE)
        assert package.path == SAMPLE

    def test_api_Package__init__calls_setup_package(self, mocker):
        mocked = mocker.patch("arrangeit.windows.api.Package.setup_package")
        Package()
        mocked.assert_called_once()
        mocked.assert_called_with()

    # Package._get_first_image
    def test_api_Package__get_first_image_calls_product(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        mocked = mocker.patch("arrangeit.windows.api.product")
        SAMPLE = ["a"]
        Package()._get_first_image(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE, api.UWP_ICON_SUFFIXES)

    def test_api_Package__get_first_image_calls_splitext(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        NAME = "foo"
        mocker.patch("arrangeit.windows.api.product", return_value=[(NAME, "bar")])
        mocker.patch("arrangeit.windows.api.Image")
        mocker.patch("os.path.join")
        mocked = mocker.patch("os.path.splitext")
        Package()._get_first_image(["b"])
        calls = [mocker.call(NAME)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_api_Package__get_first_image_calls_os_path_join(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        PATH = "foobar"
        NAME = "foo"
        SUFFIX = "bar"
        SPLIT = ("ABC", "DEF")
        mocker.patch("os.path.splitext", return_value=SPLIT)
        mocker.patch("arrangeit.windows.api.product", return_value=[(NAME, SUFFIX)])
        mocker.patch("arrangeit.windows.api.Image")
        mocked = mocker.patch("os.path.join")
        Package(PATH)._get_first_image(["c"])
        calls = [mocker.call(PATH, SPLIT[0] + SUFFIX + SPLIT[1])]
        mocked.assert_has_calls(calls, any_order=True)

    def test_api_Package__get_first_image_calls_os_path_exists(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        PATH = "foobar"
        NAME = "foo"
        SUFFIX = "bar"
        SPLIT = ("ABC", "DEF")
        mocker.patch("os.path.splitext", return_value=SPLIT)
        mocker.patch("arrangeit.windows.api.product", return_value=[(NAME, SUFFIX)])
        CHECK_PATH = SPLIT[0] + SUFFIX + SPLIT[1]
        mocker.patch("os.path.join", return_value=CHECK_PATH)
        mocked = mocker.patch("os.path.exists")
        mocker.patch("arrangeit.windows.api.open_image")
        Package(PATH)._get_first_image(["d"])
        calls = [mocker.call(CHECK_PATH)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_api_Package__get_first_image_calls_and_returns_resized_Image(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        PATH = "foobar"
        NAME = "foo"
        SUFFIX = "bar"
        SPLIT = ("ABC", "DEF")
        mocker.patch("os.path.splitext", return_value=SPLIT)
        mocker.patch("arrangeit.windows.api.product", return_value=[(NAME, SUFFIX)])
        CHECK_PATH = SPLIT[0] + SUFFIX + SPLIT[1]
        mocker.patch("os.path.join", return_value=CHECK_PATH)
        mocker.patch("os.path.exists", return_value=True)
        mocked = mocker.patch("arrangeit.windows.api.Image")
        returned = Package(PATH)._get_first_image(["e"])
        calls = [mocker.call(CHECK_PATH)]
        mocked.open.assert_has_calls(calls, any_order=True)
        calls = [mocker.call((Settings.ICON_SIZE, Settings.ICON_SIZE), mocked.BICUBIC)]
        mocked.open.return_value.resize.assert_has_calls(calls, any_order=True)
        assert returned == mocked.open.return_value.resize.return_value

    def test_api_Package__get_first_image_catches_exception(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        PATH = "foobar"
        NAME = "foo"
        SUFFIX = "bar"
        SPLIT = ("ABC", "DEF")
        mocker.patch("os.path.splitext", return_value=SPLIT)
        mocker.patch("arrangeit.windows.api.product", return_value=[(NAME, SUFFIX)])
        CHECK_PATH = SPLIT[0] + SUFFIX + SPLIT[1]
        mocker.patch("os.path.join", return_value=CHECK_PATH)
        mocker.patch("os.path.exists", return_value=True)
        mocker.patch("arrangeit.windows.api.Image.open", side_effect=IOError())
        mocked = mocker.patch("arrangeit.windows.api.open_image")
        returned = Package(PATH)._get_first_image(["f"])
        calls = [mocker.call("white.png")]
        mocked.assert_has_calls(calls, any_order=True)
        assert returned == mocked.return_value

    def test_api_Package__get_first_image_calls_open_image_if_not_exists(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        PATH = "foobar"
        NAME = "foo"
        SUFFIX = "bar"
        SPLIT = ("ABC", "DEF")
        mocker.patch("os.path.splitext", return_value=SPLIT)
        mocker.patch("arrangeit.windows.api.product", return_value=[(NAME, SUFFIX)])
        CHECK_PATH = SPLIT[0] + SUFFIX + SPLIT[1]
        mocker.patch("os.path.join", return_value=CHECK_PATH)
        mocker.patch("os.path.exists", return_value=False)
        mocked = mocker.patch("arrangeit.windows.api.open_image")
        returned = Package(PATH)._get_first_image(["g"])
        calls = [mocker.call("white.png")]
        mocked.assert_has_calls(calls, any_order=True)
        assert returned == mocked.return_value

    # Package._get_manifest_root
    def test_api_Package__get_manifest_root_calls_os_path_join(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        mocker.patch("xml.etree.ElementTree.parse")
        PATH = "foobar"
        mocked = mocker.patch("os.path.join")
        Package(PATH)._get_manifest_root()
        calls = [mocker.call(PATH, "AppXManifest.xml")]
        mocked.assert_has_calls(calls, any_order=True)

    def test_api_Package__get_manifest_root_calls_os_path_exists(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        SAMPLE = "foobar"
        mocker.patch("os.path.join", return_value=SAMPLE)
        mocked = mocker.patch("os.path.exists", return_value=False)
        Package()._get_manifest_root()
        calls = [mocker.call(SAMPLE)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_api_Package__get_manifest_root_returns_true_if_not_exists(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        mocker.patch("os.path.exists", return_value=False)
        returned = Package()._get_manifest_root()
        assert returned is True

    def test_api_Package__get_manifest_root_calls_parse(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        SAMPLE = "foobar1"
        mocker.patch("os.path.join", return_value=SAMPLE)
        mocker.patch("os.path.exists", return_value=True)
        mocked = mocker.patch("xml.etree.ElementTree.parse")
        Package()._get_manifest_root()
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE)

    def test_api_Package__get_manifest_root_calls_and_returns_getroot(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        mocker.patch("os.path.join")
        mocker.patch("os.path.exists", return_value=True)
        mocked = mocker.patch("xml.etree.ElementTree.parse")
        returned = Package()._get_manifest_root()
        mocked.return_value.getroot.assert_called_once()
        mocked.return_value.getroot.assert_called_with()
        assert returned == mocked.return_value.getroot.return_value

    # Package._namespace_for_element
    def test_api_Package__namespace_for_element_calls_re_match(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        ELEMENT = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.windows.api.re.match")
        Package()._namespace_for_element(ELEMENT)
        calls = [mocker.call(r"\{.*\}", ELEMENT.tag)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_api_Package__namespace_for_element_returns_first_group(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        MATCH = mocker.MagicMock()
        mocker.patch("arrangeit.windows.api.re.match", return_value=MATCH)
        returned = Package()._namespace_for_element(mocker.MagicMock())
        assert returned == MATCH.group(0)

    def test_api_Package__namespace_for_element_returns_empty_string(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        mocker.patch("arrangeit.windows.api.re.match", return_value=False)
        returned = Package()._namespace_for_element(mocker.MagicMock())
        assert returned == ""

    # Package._setup_app_name
    def test_api_Package__setup_app_name_calls__namespace_for_element(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        ROOT = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.windows.api.Package._namespace_for_element")
        Package()._setup_app_name(ROOT)
        calls = [mocker.call(ROOT)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_api_Package__setup_app_name_calls_root_iter(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        ROOT = mocker.MagicMock()
        NAMESPACE = "foo"
        mocker.patch(
            "arrangeit.windows.api.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        Package()._setup_app_name(ROOT)
        ROOT.iter.assert_called_once()
        ROOT.iter.assert_called_with("{}Identity".format(NAMESPACE))

    def test_api_Package__setup_app_name_calls_next(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        ROOT = mocker.MagicMock()
        NAMESPACE = "foo"
        mocker.patch(
            "arrangeit.windows.api.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.api.next")
        Package()._setup_app_name(ROOT)
        mocked.assert_called_once()
        mocked.assert_called_with(ROOT.iter.return_value)

    def test_api_Package__setup_app_name_calls_iter_on_next(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        ROOT = mocker.MagicMock()
        NAMESPACE = "foo"
        mocker.patch(
            "arrangeit.windows.api.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.api.next")
        Package()._setup_app_name(ROOT)
        mocked.return_value.iter.assert_called_once()
        mocked.return_value.iter.assert_called_with()

    def test_api_Package__setup_app_name_sets_app_name_attr(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        SAMPLE = "bar"
        IDENTITY = mocker.MagicMock()
        IDENTITY.attrib = {"Name": "foo.{}".format(SAMPLE)}
        NAMESPACE = "foo"
        mocker.patch(
            "arrangeit.windows.api.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.api.next")
        mocked.return_value.iter.return_value = [IDENTITY]
        package = Package()
        package._setup_app_name(mocker.MagicMock())
        assert package.app_name == SAMPLE

    # Package._setup_icon
    def test_api_Package__setup_icon_calls__namespace_for_element(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        ROOT = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.windows.api.Package._namespace_for_element")
        Package()._setup_icon(ROOT)
        calls = [mocker.call(ROOT)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_api_Package__setup_icon_calls_root_iter(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        ROOT = mocker.MagicMock()
        NAMESPACE = "bar"
        mocker.patch(
            "arrangeit.windows.api.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        Package()._setup_icon(ROOT)
        calls = [mocker.call("{}Applications".format(NAMESPACE))]
        ROOT.iter.assert_has_calls(calls, any_order=True)

    def test_api_Package__setup_icon_calls_next(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        ROOT = mocker.MagicMock()
        NAMESPACE = "bar"
        mocker.patch(
            "arrangeit.windows.api.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.api.next")
        Package()._setup_icon(ROOT)
        calls = [mocker.call(ROOT.iter.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_api_Package__setup_icon_calls_iter_on_next(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        ROOT = mocker.MagicMock()
        NAMESPACE = "bar"
        mocker.patch(
            "arrangeit.windows.api.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.api.next")
        Package()._setup_icon(ROOT)
        calls = [mocker.call()]
        mocked.return_value.iter.assert_has_calls(calls, any_order=True)

    def test_api_Package__setup_icon_appends_once_to_sources_from_Applications(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        SAMPLE = "foo1bar"
        SUBELEM = mocker.MagicMock()
        SUBELEM.tag = "VisualElements"
        SUBELEM.attrib = {"Square44x44Logo": SAMPLE, "Square150x150Logo": SAMPLE}
        NAMESPACE = "barfoo"
        mocker.patch(
            "arrangeit.windows.api.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.api.next")
        mocked_first = mocker.patch("arrangeit.windows.api.Package._get_first_image")
        mocked.return_value.iter.return_value = [SUBELEM]
        Package()._setup_icon(mocker.MagicMock())
        mocked_first.assert_called_with([SAMPLE])

    def test_api_Package__setup_icon_appends_to_sources_from_Properties(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        SAMPLE = "foo1bar4"
        PROP = mocker.MagicMock()
        PROP.tag = "Logo"
        PROP.text = SAMPLE
        NAMESPACE = "barfoo"
        mocker.patch(
            "arrangeit.windows.api.Package._namespace_for_element",
            return_value=NAMESPACE,
        )
        mocked = mocker.patch("arrangeit.windows.api.next")
        mocked_first = mocker.patch("arrangeit.windows.api.Package._get_first_image")
        mocked.return_value.iter.return_value = [PROP]
        package = Package()
        package._setup_icon(mocker.MagicMock())
        mocked_first.assert_called_with([SAMPLE])
        assert package.icon == mocked_first.return_value

    # Package.setup_package
    def test_api_Package_setup_package_calls__get_manifest_root(self, mocker):
        mocked = mocker.patch("arrangeit.windows.api.Package._get_manifest_root")
        mocker.patch("arrangeit.windows.api.Package._setup_app_name")
        mocker.patch("arrangeit.windows.api.Package._setup_icon")
        package = Package()
        mocked.reset_mock()
        package.setup_package()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_api_Package_setup_package_calls__setup_app_name(self, mocker):
        mocked_root = mocker.patch("arrangeit.windows.api.Package._get_manifest_root")
        mocked = mocker.patch("arrangeit.windows.api.Package._setup_app_name")
        mocker.patch("arrangeit.windows.api.Package._setup_icon")
        package = Package()
        mocked.reset_mock()
        package.setup_package()
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_root.return_value)

    def test_api_Package_setup_package_calls__setup_icon(self, mocker):
        mocked_root = mocker.patch("arrangeit.windows.api.Package._get_manifest_root")
        mocker.patch("arrangeit.windows.api.Package._setup_app_name")
        mocked = mocker.patch("arrangeit.windows.api.Package._setup_icon")
        package = Package()
        mocked.reset_mock()
        package.setup_package()
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_root.return_value)


# Api class public methods
class TestWindowsApiApiPublic(object):
    """Testing class for :py:class:`arrangeit.windows.api.Api` public methods."""

    # Api
    @pytest.mark.parametrize("attr", ["packages"])
    def test_api_Api_inits_empty_attr(self, attr):
        assert getattr(Api, attr) == {}

    @pytest.mark.parametrize("attr", ["helpers"])
    def test_api_Api_inits_attr_as_None(self, attr):
        assert getattr(Api, attr) is None

    # Api.__init__
    def test_api_Api__init__initializes_and_sets_helpers(self, mocker):
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        api = Api()
        mocked.assert_called_once()
        mocked.assert_called_with()
        assert api.helpers == mocked.return_value

    # dwm_window_attribute_value
    def test_Api_dwm_window_attribute_value_calls__wintypes_DWORD(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.sizeof")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.wintypes.DWORD")
        Api().dwm_window_attribute_value(5070, 14)
        calls = [mocker.call()]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api_dwm_window_attribute_value_calls_ctypes_byref(self, mocker):
        mocked_value = mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("ctypes.sizeof")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.byref")
        Api().dwm_window_attribute_value(5071, 14)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_value.return_value)

    def test_Api_dwm_window_attribute_value_calls_ctypes_sizeof(self, mocker):
        mocked_value = mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.sizeof")
        Api().dwm_window_attribute_value(5072, 14)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_value.return_value)

    def test_Api_dwm_window_attribute_value_calls__dwm_get_window_attribute(
        self, mocker
    ):
        mocker.patch("ctypes.wintypes.DWORD")
        mocked_byref = mocker.patch("ctypes.byref")
        mocked_sizeof = mocker.patch("ctypes.sizeof")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        HWND, ATTRIBUTE = 5073, 14
        Api().dwm_window_attribute_value(HWND, ATTRIBUTE)
        mocked_helpers.return_value._dwm_get_window_attribute.assert_called_once()
        mocked_helpers.return_value._dwm_get_window_attribute.assert_called_with(
            HWND, ATTRIBUTE, mocked_byref.return_value, mocked_sizeof.return_value
        )

    def test_Api_dwm_window_attribute_value_returns_value(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.sizeof")
        mocker.patch("ctypes.create_string_buffer")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.wintypes.DWORD")
        returned = Api().dwm_window_attribute_value(5074, 14)
        assert returned is mocked.return_value.value

    # enum_windows
    def test_api_Api_enum_windows_nested_append_to_collection(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers")
        nested_func = nested(Api().enum_windows, "append_to_collection", hwnds=[])
        returned = nested_func("foo", None)
        assert returned is True

    def test_api_Api_enum_windows_calls_WNDENUMPROC(self, mocker):
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        Api().enum_windows()
        mocked.return_value.WNDENUMPROC.assert_called_once()

    def test_api_Api_enum_windows_calls__enum_windows(self, mocker):
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        Api().enum_windows()
        mocked.return_value._enum_windows.assert_called_once()
        mocked.return_value._enum_windows.assert_called_with(
            mocked.return_value.WNDENUMPROC.return_value, 0
        )

    def test_api_Api_enum_windows_calls__enum_child_windows(self, mocker):
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        SAMPLE = 1874
        Api().enum_windows(SAMPLE, enum_children=True)
        mocked.return_value._enum_child_windows.assert_called_once()
        mocked.return_value._enum_child_windows.assert_called_with(
            SAMPLE, mocked.return_value.WNDENUMPROC.return_value, 0
        )

    def test_api_Api_enum_windows_returns_non_empty_list(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers")
        assert isinstance(Api().enum_windows(), list)

    # executable_name_for_hwnd
    def test_Api_executable_name_for_hwnd_calls__wintypes_DWORD(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.create_string_buffer")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_process_image_file_name.return_value = False
        mocked = mocker.patch("ctypes.wintypes.DWORD")
        Api().executable_name_for_hwnd(2080)
        calls = [mocker.call()]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api_executable_name_for_hwnd_calls__get_windows_thread_process_id(
        self, mocker
    ):
        mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("ctypes.create_string_buffer")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_process_image_file_name.return_value = False
        mocked_byref = mocker.patch("ctypes.byref")
        HWND = 2081
        Api().executable_name_for_hwnd(HWND)
        calls = [mocker.call(HWND, mocked_byref.return_value)]
        mocked_helpers.return_value._get_windows_thread_process_id.assert_has_calls(
            calls, any_order=True
        )

    def test_Api_executable_name_for_hwnd_calls__open_process(self, mocker):
        mocked_dword = mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("ctypes.create_string_buffer")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_process_image_file_name.return_value = False
        mocker.patch("ctypes.byref")
        Api().executable_name_for_hwnd(2082)
        calls = [
            mocker.call(
                api.PROCESS_QUERY_LIMITED_INFORMATION, False, mocked_dword.return_value
            )
        ]
        mocked_helpers.return_value._open_process.assert_has_calls(
            calls, any_order=True
        )

    def test_Api_executable_name_for_hwnd_calls_create_string_buffer(self, mocker):
        mocker.patch("ctypes.wintypes.DWORD")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_process_image_file_name.return_value = False
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("ctypes.create_string_buffer")
        Api().executable_name_for_hwnd(2083)
        calls = [mocker.call(500)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api_executable_name_for_hwnd_calls__get_process_image_file_name(
        self, mocker
    ):
        mocker.patch("ctypes.wintypes.DWORD")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.byref")
        mocked_buffer = mocker.patch("ctypes.create_string_buffer")
        mocked_helpers.return_value._get_process_image_file_name.return_value = False
        Api().executable_name_for_hwnd(2084)
        calls = [
            mocker.call(
                mocked_helpers.return_value._open_process.return_value,
                mocked_buffer.return_value,
                500,
            )
        ]
        mocked_helpers.return_value._get_process_image_file_name.assert_has_calls(
            calls, any_order=True
        )

    def test_Api_executable_name_for_hwnd_calls__close_handle(self, mocker):
        mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("ctypes.byref")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.create_string_buffer")
        mocked_helpers.return_value._get_process_image_file_name.return_value = False
        Api().executable_name_for_hwnd(2085)
        calls = [mocker.call(mocked_helpers.return_value._open_process.return_value)]
        mocked_helpers.return_value._close_handle.assert_has_calls(
            calls, any_order=True
        )

    def test_Api_executable_name_for_hwnd_calls_and_returns_extract_name_from_bytes_path(
        self, mocker
    ):
        mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("ctypes.byref")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_buffer = mocker.patch("ctypes.create_string_buffer")
        mocked_helpers.return_value._get_process_image_file_name.return_value = True
        mocked = mocker.patch("arrangeit.windows.api.extract_name_from_bytes_path")
        returned = Api().executable_name_for_hwnd(2086)
        calls = [mocker.call(mocked_buffer.return_value.value)]
        mocked.assert_has_calls(calls, any_order=True)
        assert returned == mocked.return_value

    def test_Api_executable_name_for_hwnd_returns_None(self, mocker):
        mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.create_string_buffer")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_process_image_file_name.return_value = False
        mocked = mocker.patch("arrangeit.windows.api.extract_name_from_bytes_path")
        returned = Api().executable_name_for_hwnd(2087)
        mocked.assert_not_called()
        assert returned is None

    # get_ancestor_by_type
    def test_Api_get_ancestor_by_type_calls_and_returns__get_ancestor(
        self, mocker
    ):
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        HWND, TYPE = 50020, 1
        returned = Api().get_ancestor_by_type(HWND, TYPE)
        mocked_helpers.return_value._get_ancestor.assert_called_once()
        mocked_helpers.return_value._get_ancestor.assert_called_with(
            HWND, TYPE
        )
        assert returned == mocked_helpers.return_value._get_ancestor.return_value

    # get_last_active_popup
    def test_Api_get_last_active_popup_calls_and_returns__get_ancestor(
        self, mocker
    ):
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        HWND = 50021
        returned = Api().get_last_active_popup(HWND)
        mocked_helpers.return_value._get_last_active_popup.assert_called_once()
        mocked_helpers.return_value._get_last_active_popup.assert_called_with(
            HWND
        )
        assert returned == mocked_helpers.return_value._get_last_active_popup.return_value

    # title_info_state
    def test_Api_title_info_state_calls_TITLEBARINFO(self, mocker):
        mocker.patch("ctypes.sizeof")
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("arrangeit.windows.api.TITLEBARINFO")
        Api().title_info_state(30040, 1)
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_Api_title_info_state_calls_ctypes_sizeof(self, mocker):
        mocked_info = mocker.patch("arrangeit.windows.api.TITLEBARINFO")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("ctypes.sizeof")
        Api().title_info_state(30041, 1)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_info.return_value)

    def test_Api_title_info_state_calls_ctypes_byref(self, mocker):
        mocked_info = mocker.patch("arrangeit.windows.api.TITLEBARINFO")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.sizeof")
        mocked = mocker.patch("ctypes.byref")
        Api().title_info_state(30042, 1)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_info.return_value)

    def test_Api_title_info_state_calls__get_titlebar_info(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.TITLEBARINFO")
        mocker.patch("ctypes.sizeof")
        mocked_byref = mocker.patch("ctypes.byref")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        HWND = 30043
        Api().title_info_state(HWND, 1)
        mocked_helpers.return_value._get_titlebar_info.assert_called_once()
        mocked_helpers.return_value._get_titlebar_info.assert_called_with(
            HWND, mocked_byref.return_value
        )

    def test_Api_title_info_state_returns_value(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.sizeof")
        mocked_info = mocker.patch("arrangeit.windows.api.TITLEBARINFO")
        RGSTATE = 40
        mocked_info.return_value.rgstate = [RGSTATE, ]
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_titlebar_info.return_value = True
        STATE = 50
        returned = Api().title_info_state(30044, STATE)
        assert returned == RGSTATE & STATE

    def test_Api_title_info_state_returns_None(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.sizeof")
        mocker.patch("arrangeit.windows.api.TITLEBARINFO")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_titlebar_info.return_value = False
        returned = Api().title_info_state(30045, 1)
        assert returned is None

    # window_info_extended_style
    def test_Api_window_info_extended_style_calls_WINDOWINFO(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("arrangeit.windows.api.WINDOWINFO")
        Api().window_info_extended_style(20040, 1)
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_Api_window_info_extended_style_calls_ctypes_byref(self, mocker):
        mocked_info = mocker.patch("arrangeit.windows.api.WINDOWINFO")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.byref")
        Api().window_info_extended_style(20041, 1)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_info.return_value)

    def test_Api_window_info_extended_style_calls__get_window_info(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.WINDOWINFO")
        mocked_byref = mocker.patch("ctypes.byref")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        HWND = 20042
        Api().window_info_extended_style(HWND, 1)
        mocked_helpers.return_value._get_window_info.assert_called_once()
        mocked_helpers.return_value._get_window_info.assert_called_with(
            HWND, mocked_byref.return_value
        )

    def test_Api_window_info_extended_style_returns_value(self, mocker):
        mocker.patch("ctypes.byref")
        mocked_info = mocker.patch("arrangeit.windows.api.WINDOWINFO")
        DWEXSTYLE = 40
        mocked_info.return_value.dwExStyle = DWEXSTYLE
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_window_info.return_value = True
        STYLE = 50
        returned = Api().window_info_extended_style(20043, STYLE)
        assert returned == DWEXSTYLE & STYLE

    def test_Api_window_info_extended_style_returns_None(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.WINDOWINFO")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_window_info.return_value = False
        returned = Api().window_info_extended_style(20044, 1)
        assert returned is None


# Api class public methods for Windows >= 8.1
@pytest.mark.skipif(not platform_supports_packages(), reason="Win 8 and 10 only")
class TestWindowsApiApiPublicWin8(object):
    """Testing class for :py:class:`arrangeit.windows.api.Api` Win8 and 10 public methods."""

    # get_package
    def test_api_Api_get_package_calls__package_full_name_from_hwnd(self, mocker):
        mocker.patch("arrangeit.windows.api.Package")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("arrangeit.windows.api.Api._package_full_name_from_hwnd")
        mocker.patch("arrangeit.windows.api.Api._package_info_buffer_from_reference")
        mocker.patch("arrangeit.windows.api.PACKAGE_INFO")
        mocker.patch("arrangeit.windows.api.Api._package_info_reference_from_full_name")
        SAMPLE = 5241
        Api().get_package(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE)

    def test_api_Api_get_package_returns_empty_Package(self, mocker):
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._package_full_name_from_hwnd.return_value = False
        mocked = mocker.patch("arrangeit.windows.api.Package")
        SAMPLE = 5242
        returned = Api().get_package(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with("")
        assert returned == mocked.return_value

    def test_api_Api_get_package_calls__package_info_reference_from_full_name(
        self, mocker
    ):
        FULL_NAME = "foobar"
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch(
            "arrangeit.windows.api.Api._package_info_reference_from_full_name"
        )
        mocker.patch(
            "arrangeit.windows.api.Api._package_full_name_from_hwnd",
            return_value=FULL_NAME,
        )
        mocker.patch("arrangeit.windows.api.PACKAGE_INFO")
        mocker.patch("arrangeit.windows.api.Package")
        Api().get_package(5243)
        mocked.assert_called_once()
        mocked.assert_called_with(FULL_NAME)

    def test_api_Api_get_package_calls__package_info_buffer_from_reference(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch(
            "arrangeit.windows.api.Api._package_full_name_from_hwnd", return_value="foo"
        )
        mocked_ref = mocker.patch(
            "arrangeit.windows.api.Api._package_info_reference_from_full_name"
        )
        mocker.patch("arrangeit.windows.api.PACKAGE_INFO")
        mocker.patch("arrangeit.windows.api.Package")
        mocked = mocker.patch(
            "arrangeit.windows.api.Api._package_info_buffer_from_reference"
        )
        Api().get_package(5244)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_ref.return_value)

    def test_api_Api_get_package_calls_PACKAGE_INFO_from_buffer(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch(
            "arrangeit.windows.api.Api._package_full_name_from_hwnd", return_value="foo"
        )
        mocker.patch("arrangeit.windows.api.Api._package_info_reference_from_full_name")
        mocker.patch("arrangeit.windows.api.PACKAGE_INFO")
        mocker.patch("arrangeit.windows.api.Package")
        SAMPLE = 109
        mocker.patch(
            "arrangeit.windows.api.Api._package_info_buffer_from_reference",
            return_value=SAMPLE,
        )
        mocked = mocker.patch("arrangeit.windows.api.PACKAGE_INFO")
        Api().get_package(5245)
        mocked.from_buffer.assert_called_once()
        mocked.from_buffer.assert_called_with(SAMPLE)

    def test_api_Api_get_package_calls__close_package_info(self, mocker):
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch(
            "arrangeit.windows.api.Api._package_full_name_from_hwnd", return_value="foo"
        )
        mocked_ref = mocker.patch(
            "arrangeit.windows.api.Api._package_info_reference_from_full_name"
        )
        mocker.patch("arrangeit.windows.api.Api._package_info_buffer_from_reference")
        mocker.patch("arrangeit.windows.api.Package")
        mocker.patch("arrangeit.windows.api.PACKAGE_INFO")
        Api().get_package(5246)
        mocked_helpers.return_value._close_package_info.assert_called_once()
        mocked_helpers.return_value._close_package_info.assert_called_with(
            mocked_ref.return_value.contents
        )

    def test_api_Api_get_package_calls_Package(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch(
            "arrangeit.windows.api.Api._package_full_name_from_hwnd", return_value="foo"
        )
        mocker.patch("arrangeit.windows.api.Api._package_info_reference_from_full_name")
        mocked_info = mocker.patch("arrangeit.windows.api.PACKAGE_INFO")
        mocked = mocker.patch("arrangeit.windows.api.Package")
        returned = Api().get_package(5247)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_info.from_buffer.return_value.path)
        assert returned == mocked.return_value


# Api class private methods
@pytest.mark.skipif(not platform_supports_packages(), reason="Win 8 and 10 only")
class TestWindowsApiApiPrivateWin8(object):
    """Testing class for :py:class:`arrangeit.windows.api.Api` Win8+ private methods."""

    # _package_full_name_from_handle
    def test_Api__package_full_name_from_handle_calls_first_time__get_package_full_name(
        self, mocker
    ):
        mocked_byref = mocker.patch("ctypes.byref")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_package_full_name.return_value = 0
        SAMPLE = 520
        Api()._package_full_name_from_handle(SAMPLE)
        calls = [mocker.call(SAMPLE, mocked_byref.return_value, None)]
        mocked_helpers.return_value._get_package_full_name.assert_has_calls(
            calls, any_order=True
        )

    def test_Api__package_full_name_from_handle_returns_None_for_no_package(
        self, mocker
    ):
        mocker.patch("ctypes.byref")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_package_full_name.return_value = (
            api.APPMODEL_ERROR_NO_PACKAGE
        )
        assert Api()._package_full_name_from_handle(100) is None

    def test_Api__package_full_name_from_handle_calls_create_unicode_buffer(
        self, mocker
    ):
        mocker.patch("ctypes.byref")
        mocked_uint = mocker.patch("ctypes.c_uint")
        LENGTH = 10
        mocked_uint.return_value.value = LENGTH
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_package_full_name.return_value = 0
        mocked = mocker.patch("ctypes.create_unicode_buffer")
        Api()._package_full_name_from_handle(100)
        calls = [mocker.call(LENGTH + 1)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_full_name_from_handle_calls_again__get_package_full_name(
        self, mocker
    ):
        mocked_byref = mocker.patch("ctypes.byref")
        mocked_buffer = mocker.patch("ctypes.create_unicode_buffer")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_package_full_name.return_value = 0
        SAMPLE = 521
        Api()._package_full_name_from_handle(SAMPLE)
        calls = [
            mocker.call(SAMPLE, mocked_byref.return_value, mocked_buffer.return_value)
        ]
        mocked_helpers.return_value._get_package_full_name.assert_has_calls(
            calls, any_order=True
        )

    def test_Api__package_full_name_from_handle_returns_None_for_no_success(
        self, mocker
    ):
        mocker.patch("ctypes.byref")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_package_full_name.side_effect = [0, "foo"]
        assert Api()._package_full_name_from_handle(100) is None

    def test_Api__package_full_name_from_handle_returns_full_name(self, mocker):
        mocker.patch("ctypes.byref")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_package_full_name.side_effect = [
            0,
            api.ERROR_SUCCESS,
        ]
        mocked_buffer = mocker.patch("ctypes.create_unicode_buffer")
        returned = Api()._package_full_name_from_handle(100)
        assert returned == mocked_buffer.return_value

    # _package_full_name_from_hwnd
    def test_Api__package_full_name_from_hwnd_calls_enum_windows(self, mocker):
        mocked = mocker.patch("arrangeit.windows.api.Api.enum_windows", return_value=())
        mocked.reset_mock()
        SAMPLE = 2840
        Api()._package_full_name_from_hwnd(SAMPLE)
        calls = [mocker.call(SAMPLE, enum_children=True)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_full_name_from_hwnd_calls__wintypes_DWORD(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("arrangeit.windows.api.Api.enum_windows", return_value=(5841,))
        Api()._package_full_name_from_hwnd(2842)
        calls = [mocker.call(0)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_full_name_from_hwnd_calls__get_windows_thread_process_id(
        self, mocker
    ):
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.wintypes.DWORD")
        mocked_byref = mocker.patch("ctypes.byref")
        CHILD = 5840
        mocker.patch("arrangeit.windows.api.Api.enum_windows", return_value=(CHILD,))
        Api()._package_full_name_from_hwnd(2843)
        calls = [mocker.call(CHILD, mocked_byref.return_value)]
        mocked_helpers.return_value._get_windows_thread_process_id.assert_has_calls(
            calls, any_order=True
        )

    def test_Api__package_full_name_from_hwnd_calls__open_process(self, mocker):
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_dword = mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.Api.enum_windows", return_value=(5842,))
        Api()._package_full_name_from_hwnd(2844)
        calls = [
            mocker.call(
                api.PROCESS_QUERY_LIMITED_INFORMATION, False, mocked_dword.return_value
            )
        ]
        mocked_helpers.return_value._open_process.assert_has_calls(
            calls, any_order=True
        )

    def test_Api__package_full_name_from_hwnd_calls__package_full_name_from_handle(
        self, mocker
    ):
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.Api.enum_windows", return_value=(5843,))
        mocked = mocker.patch(
            "arrangeit.windows.api.Api._package_full_name_from_handle"
        )
        Api()._package_full_name_from_hwnd(2845)
        calls = [mocker.call(mocked_helpers.return_value._open_process.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_full_name_from_hwnd_calls__close_handle(self, mocker):
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("ctypes.byref")
        mocked_api = mocker.patch(
            "arrangeit.windows.api.Api.enum_windows", return_value=(5844,)
        )
        mocked_api.reset_mock()
        Api()._package_full_name_from_hwnd(2846)
        calls = [mocker.call(mocked_helpers.return_value._open_process.return_value)]
        mocked_helpers.return_value._close_handle.assert_has_calls(
            calls, any_order=True
        )

    def test_Api__package_full_name_from_hwnd_returns_full_name(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.wintypes.DWORD")
        FULL_NAME = "foobar"
        mocker.patch(
            "arrangeit.windows.api.Api._package_full_name_from_handle",
            return_value=FULL_NAME,
        )
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.Api.enum_windows", return_value=[5845])
        returned = Api()._package_full_name_from_hwnd(2847)
        assert returned == FULL_NAME

    def test_Api__package_full_name_from_hwnd_returns_None(self, mocker):
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.wintypes.DWORD")
        mocked_helpers.return_value._package_full_name_from_handle.return_value = None
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.Api.enum_windows", return_value=[5845])
        returned = Api()._package_full_name_from_hwnd(2847)
        assert returned is None

    # _package_info_buffer_from_reference
    def test_Api__package_info_buffer_from_reference_calls_first_time__get_package_info(
        self, mocker
    ):
        mocked_byref = mocker.patch("ctypes.byref")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_package_info.return_value = 0
        mocked_ref = mocker.MagicMock()
        Api()._package_info_buffer_from_reference(mocked_ref)
        calls = [
            mocker.call(
                mocked_ref.contents,
                api.PACKAGE_FILTER_HEAD,
                mocked_byref.return_value,
                None,
                mocked_byref.return_value,
            )
        ]
        mocked_helpers.return_value._get_package_info.assert_has_calls(
            calls, any_order=True
        )

    def test_Api__package_info_buffer_from_reference_returns_None_for_not_insufficient(
        self, mocker
    ):
        mocker.patch("ctypes.byref")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_package_info.return_value = 0
        assert Api()._package_info_buffer_from_reference(mocker.MagicMock()) is None

    def test_Api__package_info_buffer_from_reference_calls_create_string_buffer(
        self, mocker
    ):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.cast")
        mocked_uint = mocker.patch("ctypes.c_uint")
        LENGTH = 20
        mocked_uint.return_value.value = LENGTH
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_package_info.return_value = (
            api.ERROR_INSUFFICIENT_BUFFER
        )
        mocked = mocker.patch("ctypes.create_string_buffer")
        Api()._package_info_buffer_from_reference(mocker.MagicMock())
        calls = [mocker.call(LENGTH)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_info_buffer_from_reference_calls_cast(self, mocker):
        mocker.patch("ctypes.byref")
        mocked_buffer = mocker.patch("ctypes.create_string_buffer")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_package_info.return_value = (
            api.ERROR_INSUFFICIENT_BUFFER
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
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_package_info.return_value = (
            api.ERROR_INSUFFICIENT_BUFFER
        )
        mocked_ref = mocker.MagicMock()
        Api()._package_info_buffer_from_reference(mocked_ref)
        calls = [
            mocker.call(
                mocked_ref.contents,
                api.PACKAGE_FILTER_HEAD,
                mocked_byref.return_value,
                mocked_bytes.return_value,
                mocked_byref.return_value,
            )
        ]
        mocked_helpers.return_value._get_package_info.assert_has_calls(
            calls, any_order=True
        )

    def test_Api__package_info_buffer_from_reference_returns_None_for_no_success(
        self, mocker
    ):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.create_string_buffer")
        mocker.patch("ctypes.cast")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_package_info.side_effect = [
            api.ERROR_INSUFFICIENT_BUFFER,
            "foo",
        ]
        assert Api()._package_info_buffer_from_reference(mocker.MagicMock()) is None

    def test_Api__package_info_buffer_from_reference_returns_buffer(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.cast")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._get_package_info.side_effect = [
            api.ERROR_INSUFFICIENT_BUFFER,
            api.ERROR_SUCCESS,
        ]
        mocked_buffer = mocker.patch("ctypes.create_string_buffer")
        returned = Api()._package_info_buffer_from_reference(mocker.MagicMock())
        assert returned == mocked_buffer.return_value

    # _package_info_reference_from_full_name
    def test_Api__package_info_reference_from_full_name_calls_PACKAGE_INFO_REFERENCE(
        self, mocker
    ):
        mocker.patch("ctypes.pointer")
        mocked = mocker.patch("arrangeit.windows.api.PACKAGE_INFO_REFERENCE")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._open_package_info_by_full_name.return_value = (
            api.ERROR_SUCCESS
        )
        Api()._package_info_reference_from_full_name("foobar")
        mocked.assert_called_once()
        calls = [mocker.call()]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_info_reference_from_full_name_calls_pointer(self, mocker):
        mocked = mocker.patch("ctypes.pointer")
        mocked_ref = mocker.patch("arrangeit.windows.api.PACKAGE_INFO_REFERENCE")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._open_package_info_by_full_name.return_value = (
            api.ERROR_SUCCESS
        )
        Api()._package_info_reference_from_full_name("foobar")
        mocked.assert_called_once()
        calls = [mocker.call(mocked_ref.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api__package_info_ref_from_full_name_calls__open_package_info_by_full_name(
        self, mocker
    ):
        mocked_pointer = mocker.patch("ctypes.pointer")
        mocker.patch("arrangeit.windows.api.PACKAGE_INFO_REFERENCE")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._open_package_info_by_full_name.return_value = (
            api.ERROR_SUCCESS
        )
        FULL_NAME = "foobar"
        Api()._package_info_reference_from_full_name(FULL_NAME)
        mocked_helpers.return_value._open_package_info_by_full_name.assert_called_once()
        calls = [mocker.call(FULL_NAME, 0, mocked_pointer.return_value)]
        mocked_helpers.return_value._open_package_info_by_full_name.assert_has_calls(
            calls, any_order=True
        )

    def test_Api__package_info_reference_from_full_name_returns_package_info_reference(
        self, mocker
    ):
        mocked = mocker.patch("ctypes.pointer")
        mocker.patch("arrangeit.windows.api.PACKAGE_INFO_REFERENCE")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._open_package_info_by_full_name.return_value = (
            api.ERROR_SUCCESS
        )
        returned = Api()._package_info_reference_from_full_name("foobar")
        assert returned == mocked.return_value

    def test_Api__package_info_reference_from_full_name_returns_None(self, mocker):
        mocker.patch("ctypes.pointer")
        mocker.patch("arrangeit.windows.api.PACKAGE_INFO_REFERENCE")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_helpers.return_value._open_package_info_by_full_name.return_value = "foo"
        returned = Api()._package_info_reference_from_full_name("foobar")
        assert returned is None
