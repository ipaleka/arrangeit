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
    DummyVirtualDesktops,
    Helpers,
    Package,
    platform_supports_packages,
    platform_supports_virtual_desktops,
)


## custom functions
class TestWindowsApiCustomFunctions(object):
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

    def test_windows_api_platform_supports_packages_for_exception(self, mocker):
        mocker.patch(
            "arrangeit.windows.api.sys.getwindowsversion", side_effect=AttributeError()
        )
        assert platform_supports_packages() is None


    # platform_supports_virtual_desktops
    def test_windows_api_platform_supports_virtual_desktops_calls_getwindowsversion(
        self, mocker
    ):
        Version = namedtuple("version", ["major", "minor"])
        mocked = mocker.patch(
            "arrangeit.windows.api.sys.getwindowsversion", return_value=Version(6, 1)
        )
        platform_supports_virtual_desktops()
        mocked.assert_called_once()
        mocked.assert_called_with()

    @pytest.mark.parametrize(
        "major,minor,expected",
        [(5, 1, False), (6, 2, False), (7, 0, False), (10, 0, True)],
    )
    def test_windows_api_platform_supports_virtual_desktops_functionality(
        self, mocker, major, minor, expected
    ):
        Version = namedtuple("version", ["major", "minor"])
        mocker.patch(
            "arrangeit.windows.api.sys.getwindowsversion",
            return_value=Version(major, minor),
        )
        assert platform_supports_virtual_desktops() == expected

    def test_windows_api_platform_supports_virtual_desktops_for_exception(self, mocker):
        mocker.patch(
            "arrangeit.windows.api.sys.getwindowsversion", side_effect=AttributeError()
        )
        assert platform_supports_virtual_desktops() is None


## basic structures
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


## packages structures
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
    def test_windows_api_Helpers__setup_common_helpers__get_ancestor(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert helpers._get_ancestor == helpers._user32.GetAncestor
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
        assert helpers._get_last_active_popup == helpers._user32.GetLastActivePopup
        argtypes = helpers._get_last_active_popup.argtypes
        assert argtypes == (ctypes.wintypes.HWND,)
        assert helpers._get_last_active_popup.restype == ctypes.wintypes.HWND

    def test_windows_api_Helpers__setup_common_helpers__get_titlebar_info(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert helpers._get_titlebar_info == helpers._user32.GetTitleBarInfo
        argtypes = helpers._get_titlebar_info.argtypes
        assert argtypes[0] == ctypes.wintypes.HWND
        assert isinstance(argtypes[1], type(ctypes._Pointer))
        assert argtypes[1]._type_ == TITLEBARINFO
        assert helpers._get_titlebar_info.restype == ctypes.wintypes.BOOL

    def test_windows_api_Helpers__setup_common_helpers__get_window_info(self, mocker):
        mocker.patch("arrangeit.windows.api.Helpers._setup_thumbnail_helpers")
        mocker.patch(
            "arrangeit.windows.api.platform_supports_packages", return_value=False
        )
        mocker.patch("arrangeit.windows.api.Helpers._setup_win8_helpers")
        helpers = Helpers()
        helpers._setup_common_helpers()
        assert helpers._get_window_info == helpers._user32.GetWindowInfo
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
    def test_windows_api_Helpers__setup_thumbnail_helpers__dwm_is_composition_enabled(
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
            helpers._dwm_is_composition_enabled
            == helpers._dwmapi.DwmIsCompositionEnabled
        )
        argtypes = helpers._dwm_is_composition_enabled.argtypes
        assert isinstance(argtypes[0], type(ctypes._Pointer))
        assert argtypes[0]._type_ == ctypes.wintypes.BOOL
        assert helpers._dwm_is_composition_enabled.restype == ctypes.wintypes.DWORD

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


# DummyVirtualDesktops class
class TestDummyVirtualDesktops(object):
    """Testing class for :py:class:`arrangeit.windows.api.DummyVirtualDesktops`."""

    def test_api_DummyVirtualDesktops_defines_get_desktops(self, mocker):
        assert hasattr(DummyVirtualDesktops, "get_desktops")
        assert callable(DummyVirtualDesktops.get_desktops)
        assert DummyVirtualDesktops().get_desktops() == [(0, ""),]

    def test_api_DummyVirtualDesktops_defines_get_window_desktop(self, mocker):
        assert hasattr(DummyVirtualDesktops, "get_window_desktop")
        assert callable(DummyVirtualDesktops.get_window_desktop)
        assert DummyVirtualDesktops().get_window_desktop(1) == (0, "")

    def test_api_DummyVirtualDesktops_defines_move_window_to_desktop(self, mocker):
        assert hasattr(DummyVirtualDesktops, "move_window_to_desktop")
        assert callable(DummyVirtualDesktops.move_window_to_desktop)
        assert DummyVirtualDesktops().move_window_to_desktop(1, 0) is None
