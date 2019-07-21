import ctypes
import ctypes.wintypes

import pytest

import arrangeit.windows.api as api
from arrangeit.windows.api import (
    DWM_TNP_OPACITY,
    DWM_TNP_RECTDESTINATION,
    DWM_TNP_RECTSOURCE,
    DWM_TNP_SOURCECLIENTAREAONLY,
    DWM_TNP_VISIBLE,
    DWMWA_CLOAKED,
    DWMWA_EXTENDED_FRAME_BOUNDS,
    S_OK,
    Api,
    Rectangle,
    platform_supports_packages,
)

from .nested_helper import nested


# Api class private methods
class TestWindowsApiApiPrivate(object):
    """Testing class for :py:class:`arrangeit.windows.api.Api` private methods."""

    # Api._rectangle_to_wintypes_rect
    def test_api_Api__rectangle_to_wintypes_rect_calls_and_returns_wintypes_RECT(
        self, mocker
    ):
        mocked = mocker.patch("ctypes.wintypes.RECT")
        returned = Api()._rectangle_to_wintypes_rect(Rectangle(0, 0, 0, 0))
        mocked.assert_called_once()
        mocked.assert_called_with()
        assert returned == mocked.return_value

    def test_api_Api__rectangle_to_wintypes_rect_sets_attributtes(self):
        returned = Api()._rectangle_to_wintypes_rect(Rectangle(1, 2, 3, 4))
        assert returned.left == 1
        assert returned.top == 2
        assert returned.right == 3
        assert returned.bottom == 4

    # Api._update_thumbnail
    def test_api_Api__update_thumbnail_calls_DWM_THUMBNAIL_PROPERTIES(self, mocker):
        mocker.patch("arrangeit.windows.api.Api._rectangle_to_wintypes_rect")
        mocker.patch("ctypes.wintypes.BYTE")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES")
        Api()._update_thumbnail(10, Rectangle(0, 0, 0, 0))
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_api_Api__update_thumbnail_sets_dwFlags(self, mocker):
        mocker.patch("arrangeit.windows.api.Api._rectangle_to_wintypes_rect")
        mocker.patch("ctypes.wintypes.BYTE")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES")
        Api()._update_thumbnail(11, Rectangle(0, 0, 0, 0))
        assert mocked.return_value.dwFlags == (
            DWM_TNP_RECTDESTINATION
            | DWM_TNP_RECTSOURCE
            | DWM_TNP_OPACITY
            | DWM_TNP_VISIBLE
            | DWM_TNP_SOURCECLIENTAREAONLY
        )

    def test_api_Api__update_thumbnail_calls__rectangle_to_wintypes_rect(self, mocker):
        mocker.patch("arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES")
        mocker.patch("ctypes.wintypes.BYTE")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("arrangeit.windows.api.Api._rectangle_to_wintypes_rect")
        RECT = Rectangle(0, 0, 0, 0)
        Api()._update_thumbnail(20, RECT)
        mocked.assert_called_once()
        mocked.assert_called_with(RECT)

    def test_api_Api__update_thumbnail_sets_rcDestination(self, mocker):
        mocked_rect = mocker.patch(
            "arrangeit.windows.api.Api._rectangle_to_wintypes_rect"
        )
        mocker.patch("ctypes.wintypes.BYTE")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES")
        Api()._update_thumbnail(12, Rectangle(0, 0, 0, 0))
        assert mocked.return_value.rcDestination == mocked_rect.return_value

    def test_api_Api__update_thumbnail_sets_rcSource(self, mocker):
        mocked_rect = mocker.patch(
            "arrangeit.windows.api.Api._rectangle_to_wintypes_rect"
        )
        mocker.patch("ctypes.wintypes.BYTE")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES")
        Api()._update_thumbnail(13, Rectangle(0, 0, 0, 0))
        assert mocked.return_value.rcSource == mocked_rect.return_value

    def test_api_Api__update_thumbnail_sets_opacity(self, mocker):
        mocker.patch(
            "arrangeit.windows.api.Api._rectangle_to_wintypes_rect"
        )
        mocked_byte = mocker.patch("ctypes.wintypes.BYTE")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES")
        Api()._update_thumbnail(14, Rectangle(0, 0, 0, 0))
        assert mocked.return_value.opacity == mocked_byte.return_value

    def test_api_Api__update_thumbnail_sets_fVisible(self, mocker):
        mocker.patch("arrangeit.windows.api.Api._rectangle_to_wintypes_rect")
        mocker.patch("ctypes.wintypes.BYTE")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES")
        Api()._update_thumbnail(15, Rectangle(0, 0, 0, 0))
        assert mocked.return_value.fVisible is True

    def test_api_Api__update_thumbnail_sets_fSourceClientAreaOnly(self, mocker):
        mocker.patch("arrangeit.windows.api.Api._rectangle_to_wintypes_rect")
        mocker.patch("ctypes.wintypes.BYTE")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES")
        Api()._update_thumbnail(16, Rectangle(0, 0, 0, 0))
        assert mocked.return_value.fSourceClientAreaOnly is False

    def test_api_Api__update_thumbnail_calls_wintypes_BYTE(self, mocker):
        mocker.patch("arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.Api._rectangle_to_wintypes_rect")
        mocked = mocker.patch("ctypes.wintypes.BYTE")
        Api()._update_thumbnail(30, Rectangle(0, 0, 0, 0))
        mocked.assert_called_once()
        mocked.assert_called_with(255)

    def test_api_Api__update_thumbnail_calls_wintypes_byref(self, mocker):
        mocked_prop = mocker.patch("arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("ctypes.wintypes.BYTE")
        mocker.patch("arrangeit.windows.api.Api._rectangle_to_wintypes_rect")
        mocked = mocker.patch("ctypes.byref")
        Api()._update_thumbnail(40, Rectangle(0, 0, 0, 0))
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_prop.return_value)

    def test_api_Api__update_thumbnail_calls__dwm_update_thumbnail_properties(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES")
        mocker.patch("ctypes.wintypes.BYTE")
        mocker.patch("arrangeit.windows.api.Api._rectangle_to_wintypes_rect")
        mocked_byref = mocker.patch("ctypes.byref")
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        THUMBNAIL_ID = 50
        Api()._update_thumbnail(THUMBNAIL_ID, Rectangle(0, 0, 0, 0))
        mocked.return_value._dwm_update_thumbnail_properties.assert_called_once()
        mocked.return_value._dwm_update_thumbnail_properties.assert_called_with(
            THUMBNAIL_ID, mocked_byref.return_value
        )

    def test_api_Api__update_thumbnail_calls_returns_None(self, mocker):
        mocker.patch("arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES")
        mocker.patch("ctypes.wintypes.BYTE")
        mocker.patch("arrangeit.windows.api.Api._rectangle_to_wintypes_rect")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        returned = Api()._update_thumbnail(60, Rectangle(0, 0, 0, 0))
        mocked.return_value._dwm_update_thumbnail_properties.return_value = 1
        assert returned is None

    def test_api_Api__update_thumbnail_calls_returns_thumbnail_id(self, mocker):
        mocker.patch("arrangeit.windows.api.DWM_THUMBNAIL_PROPERTIES")
        mocker.patch("ctypes.wintypes.BYTE")
        mocker.patch("arrangeit.windows.api.Api._rectangle_to_wintypes_rect")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        THUMBNAIL_ID = 70
        mocked.return_value._dwm_update_thumbnail_properties.return_value = S_OK
        returned = Api()._update_thumbnail(THUMBNAIL_ID, Rectangle(0, 0, 0, 0))
        assert returned is THUMBNAIL_ID

    # Api._wintypes_rect_to_rectangle
    def test_api_Api__wintypes_rect_to_rectangle_calls_and_returns_Rectangle(
        self, mocker
    ):
        winrect = ctypes.wintypes.RECT()
        winrect.left = 100
        winrect.top = 200
        winrect.right = 700
        winrect.bottom = 800
        returned = Api()._wintypes_rect_to_rectangle(winrect)
        assert isinstance(returned, Rectangle)
        assert tuple(returned) == (100, 200, 700, 800)


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

    # cloaked_value
    def test_Api_cloaked_value_calls_wintypes_DWORD(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.sizeof")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.wintypes.DWORD")
        Api().cloaked_value(5070)
        calls = [mocker.call()]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api_cloaked_value_calls_ctypes_byref(self, mocker):
        mocked_value = mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("ctypes.sizeof")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.byref")
        Api().cloaked_value(5071)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_value.return_value)

    def test_Api_cloaked_value_calls_ctypes_sizeof(self, mocker):
        mocked_value = mocker.patch("ctypes.wintypes.DWORD")
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.sizeof")
        Api().cloaked_value(5072)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_value.return_value)

    def test_Api_cloaked_value_calls__dwm_get_window_attribute(
        self, mocker
    ):
        mocker.patch("ctypes.wintypes.DWORD")
        mocked_byref = mocker.patch("ctypes.byref")
        mocked_sizeof = mocker.patch("ctypes.sizeof")
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        HWND = 5073
        Api().cloaked_value(HWND)
        mocked.return_value._dwm_get_window_attribute.assert_called_once()
        mocked.return_value._dwm_get_window_attribute.assert_called_with(
            HWND, DWMWA_CLOAKED, mocked_byref.return_value, mocked_sizeof.return_value
        )

    def test_Api_cloaked_value_returns_0(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.sizeof")
        mocker.patch("ctypes.create_string_buffer")
        mocker.patch("ctypes.wintypes.DWORD")
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        mocked.return_value._dwm_get_window_attribute.return_value = 1
        returned = Api().cloaked_value(5075)
        assert returned == 0

    def test_Api_cloaked_value_returns_value(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.sizeof")
        mocker.patch("ctypes.create_string_buffer")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.wintypes.DWORD")
        mocked_helpers.return_value._dwm_get_window_attribute.return_value = S_OK
        returned = Api().cloaked_value(5076)
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
    def test_Api_executable_name_for_hwnd_calls_wintypes_DWORD(self, mocker):
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

    # extended_frame_rect
    def test_Api_extended_frame_rect_calls_wintypes_RECT(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.sizeof")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.wintypes.RECT")
        Api().extended_frame_rect(7070)
        calls = [mocker.call()]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Api_extended_frame_rect_calls_ctypes_byref(self, mocker):
        mocked_value = mocker.patch("ctypes.wintypes.RECT")
        mocker.patch("ctypes.sizeof")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.byref")
        Api().extended_frame_rect(7071)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_value.return_value)

    def test_Api_extended_frame_rect_calls_ctypes_sizeof(self, mocker):
        mocked_value = mocker.patch("ctypes.wintypes.RECT")
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.sizeof")
        Api().extended_frame_rect(7072)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_value.return_value)

    def test_Api_extended_frame_rect_calls__dwm_get_window_attribute(
        self, mocker
    ):
        mocker.patch("ctypes.wintypes.RECT")
        mocked_byref = mocker.patch("ctypes.byref")
        mocked_sizeof = mocker.patch("ctypes.sizeof")
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        HWND = 7073
        Api().extended_frame_rect(HWND)
        mocked.return_value._dwm_get_window_attribute.assert_called_once()
        mocked.return_value._dwm_get_window_attribute.assert_called_with(
            HWND, DWMWA_EXTENDED_FRAME_BOUNDS, mocked_byref.return_value, mocked_sizeof.return_value
        )

    def test_Api_extended_frame_rect_returns_None(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.sizeof")
        mocker.patch("ctypes.create_string_buffer")
        mocker.patch("ctypes.wintypes.RECT")
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        mocked.return_value._dwm_get_window_attribute.return_value = 1
        returned = Api().extended_frame_rect(7075)
        assert returned is None

    def test_Api_extended_frame_rect_calls_and_returns_wintypes_rect_to_rectangle(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("ctypes.sizeof")
        mocker.patch("ctypes.create_string_buffer")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        mocked_rect = mocker.patch("ctypes.wintypes.RECT")
        mocked = mocker.patch("arrangeit.windows.api.Api._wintypes_rect_to_rectangle")
        mocked_helpers.return_value._dwm_get_window_attribute.return_value = S_OK
        returned = Api().extended_frame_rect(7076)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_rect.return_value)
        assert returned == mocked.return_value

    # get_ancestor_by_type
    def test_Api_get_ancestor_by_type_calls_and_returns__get_ancestor(self, mocker):
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        HWND, TYPE = 50020, 1
        returned = Api().get_ancestor_by_type(HWND, TYPE)
        mocked_helpers.return_value._get_ancestor.assert_called_once()
        mocked_helpers.return_value._get_ancestor.assert_called_with(HWND, TYPE)
        assert returned == mocked_helpers.return_value._get_ancestor.return_value

    # get_last_active_popup
    def test_Api_get_last_active_popup_calls_and_returns__get_ancestor(self, mocker):
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        HWND = 50021
        returned = Api().get_last_active_popup(HWND)
        mocked_helpers.return_value._get_last_active_popup.assert_called_once()
        mocked_helpers.return_value._get_last_active_popup.assert_called_with(HWND)
        assert (
            returned == mocked_helpers.return_value._get_last_active_popup.return_value
        )

    # is_dwm_composition_enabled
    def test_Api_is_dwm_composition_enabled_calls_wintypes_BOOL(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.wintypes.BOOL")
        Api().is_dwm_composition_enabled()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_Api_is_dwm_composition_enabled_calls_ctypes_byref(self, mocker):
        mocked_enabled = mocker.patch("ctypes.wintypes.BOOL")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.byref")
        Api().is_dwm_composition_enabled()
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_enabled.return_value)

    def test_Api_is_dwm_composition_enabled_calls__dwm_is_composition_enabled(
        self, mocker
    ):
        mocker.patch("ctypes.wintypes.BOOL")
        mocked_byref = mocker.patch("ctypes.byref")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        Api().is_dwm_composition_enabled()
        mocked_helpers.return_value._dwm_is_composition_enabled.assert_called_once()
        mocked_helpers.return_value._dwm_is_composition_enabled.assert_called_with(
            mocked_byref.return_value
        )

    def test_Api_is_dwm_composition_enabled_returns_value(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocked = mocker.patch("ctypes.wintypes.BOOL")
        returned = Api().is_dwm_composition_enabled()
        assert returned is mocked.return_value.value

    # setup_thumbnail
    def test_Api_setup_thumbnail_calls_wintypes_HANDLE(self, mocker):
        mocker.patch("ctypes.byref")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("arrangeit.windows.api.Api._update_thumbnail")
        mocked = mocker.patch("ctypes.wintypes.HANDLE")
        Api().setup_thumbnail(270, 370, None)
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_Api_setup_thumbnail_calls_wintypes_byref(self, mocker):
        mocked_handle = mocker.patch("ctypes.wintypes.HANDLE")
        mocker.patch("arrangeit.windows.api.Helpers")
        mocker.patch("arrangeit.windows.api.Api._update_thumbnail")
        mocked = mocker.patch("ctypes.byref")
        Api().setup_thumbnail(271, 371, None)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_handle.return_value)

    def test_Api_setup_thumbnail_calls__dwm_register_thumbnail(self, mocker):
        mocker.patch("ctypes.wintypes.HANDLE")
        mocker.patch("arrangeit.windows.api.Api._update_thumbnail")
        mocked_byref = mocker.patch("ctypes.byref")
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        FROM, ROOT = 272, 372
        Api().setup_thumbnail(FROM, ROOT, None)
        mocked.return_value._dwm_register_thumbnail.assert_called_once()
        mocked.return_value._dwm_register_thumbnail.assert_called_with(
            ROOT, FROM, mocked_byref.return_value
        )

    def test_Api_setup_thumbnail_returns_None(self, mocker):
        mocker.patch("ctypes.wintypes.HANDLE")
        mocker.patch("arrangeit.windows.api.Api._update_thumbnail")
        mocker.patch("ctypes.byref")
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        mocked.return_value._dwm_register_thumbnail.return_value = 1
        returned = Api().setup_thumbnail(273, 373, None)
        assert returned is None

    def test_Api_setup_thumbnail_calls_and_returns__update_thumbnail(self, mocker):
        mocked_handle = mocker.patch("ctypes.wintypes.HANDLE")
        mocker.patch("ctypes.byref")
        mocked_helpers = mocker.patch("arrangeit.windows.api.Helpers")
        RECTANGLE = "foo"
        mocked_helpers.return_value._dwm_register_thumbnail.return_value = S_OK
        mocked = mocker.patch("arrangeit.windows.api.Api._update_thumbnail")
        returned = Api().setup_thumbnail(273, 373, RECTANGLE)
        mocked.assert_called_once()
        mocked.assert_called_with(
            mocked_handle.return_value, RECTANGLE
        )
        assert returned is mocked.return_value

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

    def test_Api_title_info_state_calls__get_titlebar_info(self, mocker):
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
        mocked_info.return_value.rgstate = [RGSTATE]
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

    # unregister_thumbnail
    def test_Api_unregister_thumbnail_calls__dwm_unregister_thumbnail(self, mocker):
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        THUMBNAIL_ID = 100
        Api().unregister_thumbnail(THUMBNAIL_ID)
        mocked.return_value._dwm_unregister_thumbnail.assert_called_once()
        mocked.return_value._dwm_unregister_thumbnail.assert_called_with(THUMBNAIL_ID)

    def test_Api_unregister_thumbnail_returns_True_on_error(self, mocker):
        mocked = mocker.patch("arrangeit.windows.api.Helpers")
        mocked.return_value._dwm_unregister_thumbnail.return_value = 1
        assert Api().unregister_thumbnail(101) is True

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

    def test_Api_window_info_extended_style_calls__get_window_info(self, mocker):
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

    def test_Api__package_full_name_from_hwnd_calls_wintypes_DWORD(self, mocker):
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
