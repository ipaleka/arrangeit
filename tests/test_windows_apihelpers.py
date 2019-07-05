import ctypes
import ctypes.wintypes
import importlib

import pytest

import arrangeit.windows.apihelpers as apihelpers

from arrangeit.windows.apihelpers import (
    PACKAGE_SUBVERSION,
    PACKAGE_VERSION_U,
    PACKAGE_VERSION,
    PACKAGE_ID,
    PACKAGE_INFO,
    PACKAGE_INFO_REFERENCE,
    TITLEBARINFO,
    WINDOWINFO,
)
from .nested_helper import nested

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


# API helper functions
class TestWindowsApiHelperFunctions(object):
    """Testing class for :py:mod:`arrangeit.windows.apihelpers` win32 functions."""

    # _user32
    def test_windows_apihelpers_calls_WinDLL_user32(self, mocker):
        mocked = mocker.patch("ctypes.WinDLL")
        mocked.reset_mock()
        importlib.reload(apihelpers)
        calls = [mocker.call("user32", use_last_error=True)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_windows_apihelpers_defines__user32(self, mocker):
        mocked = mocker.patch("ctypes.WinDLL")
        mocked.reset_mock()
        importlib.reload(apihelpers)
        assert apihelpers.__dict__.get("_user32") is not None
        assert apihelpers._user32 == mocked.return_value

    # _kernel32
    def test_windows_apihelpers_calls_WinDLL_kernel32(self, mocker):
        mocked = mocker.patch("ctypes.WinDLL")
        mocked.reset_mock()
        importlib.reload(apihelpers)
        calls = [mocker.call("kernel32", use_last_error=True)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_windows_apihelpers_defines__kernel32(self, mocker):
        mocked = mocker.patch("ctypes.WinDLL")
        mocked.reset_mock()
        importlib.reload(apihelpers)
        assert apihelpers.__dict__.get("_kernel32") is not None
        assert apihelpers._kernel32 == mocked.return_value

    # WNDENUMPROC
    def test_windows_apihelpers_calls_WINFUNCTYPE(self, mocker):
        mocked = mocker.patch("ctypes.WINFUNCTYPE")
        mocked.reset_mock()
        importlib.reload(apihelpers)
        calls = [
            mocker.call(
                ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_windows_apihelpers_defines_WNDENUMPROC(self, mocker):
        mocked = mocker.patch("ctypes.WINFUNCTYPE")
        mocked.reset_mock()
        importlib.reload(apihelpers)
        assert apihelpers.__dict__.get("WNDENUMPROC") is not None
        assert apihelpers.WNDENUMPROC == mocked.return_value

    # _get_windows_thread_process_id
    def test_windows_apihelpers_defines__get_windows_thread_process_id(self, mocker):
        assert apihelpers.__dict__.get("_get_windows_thread_process_id") is not None
        assert (
            apihelpers._get_windows_thread_process_id
            == apihelpers._user32.GetWindowThreadProcessId
        )

    def test_windows_apihelpers__get_windows_thread_process_id_argtypes_and_restype(
        self, mocker
    ):
        assert apihelpers._get_windows_thread_process_id.argtypes == (
            ctypes.wintypes.HWND,
            ctypes.POINTER(ctypes.wintypes.DWORD),
        )
        assert (
            apihelpers._get_windows_thread_process_id.restype == ctypes.wintypes.DWORD
        )

    # _enum_windows
    def test_windows_apihelpers_defines__enum_windows(self, mocker):
        assert apihelpers.__dict__.get("_enum_windows") is not None
        assert apihelpers._enum_windows == apihelpers._user32.EnumWindows

    def test_windows_apihelpers__enum_windows_argtypes_and_restype(self, mocker):
        assert apihelpers._enum_windows.argtypes == (
            apihelpers.WNDENUMPROC,
            ctypes.wintypes.LPARAM,
        )
        assert apihelpers._enum_windows.restype == ctypes.wintypes.BOOL

    # _enum_child_windows
    def test_windows_apihelpers_defines__enum_child_windows(self, mocker):
        assert apihelpers.__dict__.get("_enum_child_windows") is not None
        assert apihelpers._enum_child_windows == apihelpers._user32.EnumChildWindows

    def test_windows_apihelpers__enum_child_windows_argtypes_and_restype(self, mocker):
        assert apihelpers._enum_child_windows.argtypes == (
            (ctypes.wintypes.HWND, apihelpers.WNDENUMPROC, ctypes.wintypes.LPARAM)
        )
        assert apihelpers._enum_child_windows.restype == ctypes.wintypes.BOOL

    # _open_process
    def test_windows_apihelpers_defines__open_process(self, mocker):
        assert apihelpers.__dict__.get("_open_process") is not None
        assert apihelpers._open_process == apihelpers._kernel32.OpenProcess

    def test_windows_apihelpers__open_process_argtypes_and_restype(self, mocker):
        assert apihelpers._open_process.argtypes == (
            ctypes.wintypes.DWORD,
            ctypes.wintypes.BOOL,
            ctypes.wintypes.DWORD,
        )
        assert apihelpers._open_process.restype == ctypes.wintypes.HANDLE

    # _close_handle
    def test_windows_apihelpers_defines__close_handle(self, mocker):
        assert apihelpers.__dict__.get("_close_handle") is not None
        assert apihelpers._close_handle == apihelpers._kernel32.CloseHandle

    def test_windows_apihelpers__close_handle_argtypes_and_restype(self, mocker):
        assert apihelpers._close_handle.argtypes == (ctypes.wintypes.HANDLE,)
        assert apihelpers._close_handle.restype == ctypes.wintypes.BOOL

    # _get_package_full_name
    def test_windows_apihelpers_defines__get_package_full_name(self, mocker):
        assert apihelpers.__dict__.get("_get_package_full_name") is not None
        assert (
            apihelpers._get_package_full_name == apihelpers._kernel32.GetPackageFullName
        )

    def test_windows_apihelpers__get_package_full_name_argtypes_and_restype(
        self, mocker
    ):
        assert apihelpers._get_package_full_name.argtypes == (
            ctypes.wintypes.HANDLE,
            ctypes.POINTER(ctypes.c_uint32),
            ctypes.wintypes.LPCWSTR,
        )
        assert apihelpers._get_package_full_name.restype == ctypes.wintypes.LONG


# custom helper functions
class TestWindowsApiCustomHelperFunctions(object):
    """Testing class for :py:mod:`arrangeit.windows.apihelpers` functions."""

    # enum_windows
    def test_apihelpers_enum_windows_nested_append_to_collection(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.WNDENUMPROC")
        mocker.patch("arrangeit.windows.apihelpers._enum_windows")
        nested_func = nested(apihelpers.enum_windows, 'append_to_collection', hwnds=[])
        returned = nested_func("foo", None)
        assert returned is True

    def test_apihelpers_enum_windows_calls_WNDENUMPROC(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers._enum_windows")
        mocked = mocker.patch("arrangeit.windows.apihelpers.WNDENUMPROC")
        apihelpers.enum_windows()
        mocked.assert_called_once()

    def test_apihelpers_enum_windows_calls__enum_windows(self, mocker):
        mocked_enum = mocker.patch("arrangeit.windows.apihelpers.WNDENUMPROC")
        mocked = mocker.patch("arrangeit.windows.apihelpers._enum_windows")
        apihelpers.enum_windows()
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_enum.return_value, 0)

    def test_apihelpers_enum_windows_calls__enum_child_windows(self, mocker):
        mocked_enum = mocker.patch("arrangeit.windows.apihelpers.WNDENUMPROC")
        mocked = mocker.patch("arrangeit.windows.apihelpers._enum_child_windows")
        SAMPLE = 1874
        apihelpers.enum_windows(SAMPLE, enum_children=True)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE, mocked_enum.return_value, 0)

    def test_apihelpers_enum_windows_returns_non_empty_list(self, mocker):
        mocker.patch("arrangeit.windows.apihelpers.WNDENUMPROC")
        mocker.patch("arrangeit.windows.apihelpers._enum_windows")
        assert isinstance(apihelpers.enum_windows(), list)

    # _package_full_name_from_handle
    def test__package_full_name_from_handle_calls_first_time__get_package_full_name(
        self, mocker
    ):
        mocked_byref = mocker.patch("ctypes.byref")
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers._get_package_full_name", return_value=0
        )
        SAMPLE = 520
        apihelpers._package_full_name_from_handle(SAMPLE)
        calls = [mocker.call(SAMPLE, mocked_byref.return_value, None)]
        mocked.assert_has_calls(calls, any_order=True)

    def test__package_full_name_from_handle_returns_None_for_no_package(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch(
            "arrangeit.windows.apihelpers._get_package_full_name",
            return_value=apihelpers.APPMODEL_ERROR_NO_PACKAGE,
        )
        assert apihelpers._package_full_name_from_handle(100) is None

    def test__package_full_name_from_handle_calls_create_unicode_buffer(self, mocker):
        mocker.patch("ctypes.byref")
        mocked_uint = mocker.patch("ctypes.c_uint")
        LENGTH = 10
        mocked_uint.return_value.value = LENGTH
        mocker.patch(
            "arrangeit.windows.apihelpers._get_package_full_name", return_value=0
        )
        mocked = mocker.patch("ctypes.create_unicode_buffer")
        apihelpers._package_full_name_from_handle(100)
        calls = [mocker.call(LENGTH + 1)]
        mocked.assert_has_calls(calls, any_order=True)

    def test__package_full_name_from_handle_calls_second_time__get_package_full_name(
        self, mocker
    ):
        mocked_byref = mocker.patch("ctypes.byref")
        mocked_buffer = mocker.patch("ctypes.create_unicode_buffer")
        mocked = mocker.patch(
            "arrangeit.windows.apihelpers._get_package_full_name", return_value=0
        )
        SAMPLE = 521
        apihelpers._package_full_name_from_handle(SAMPLE)
        calls = [
            mocker.call(SAMPLE, mocked_byref.return_value, mocked_buffer.return_value)
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test__package_full_name_from_handle_calls_WinError_for_no_success(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch(
            "arrangeit.windows.apihelpers._get_package_full_name",
            side_effect=[0, "foo"],
        )
        mocked_last = mocker.patch("ctypes.get_last_error")
        mocked = mocker.patch("ctypes.WinError")
        apihelpers._package_full_name_from_handle(100)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_last.return_value)

    def test__package_full_name_from_handle_returns_None_for_no_success(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch(
            "arrangeit.windows.apihelpers._get_package_full_name",
            side_effect=[0, "foo"],
        )
        assert apihelpers._package_full_name_from_handle(100) is None

    def test__package_full_name_from_handle_returns_full_name(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch(
            "arrangeit.windows.apihelpers._get_package_full_name",
            side_effect=[0, apihelpers.ERROR_SUCCESS],
        )
        mocked_buffer = mocker.patch("ctypes.create_unicode_buffer")
        returned = apihelpers._package_full_name_from_handle(100)
        assert returned == mocked_buffer.return_value
