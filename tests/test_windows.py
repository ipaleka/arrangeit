import pytest

from arrangeit.settings import Settings
from arrangeit.windows.api import Package
from arrangeit.windows.app import App
from arrangeit.windows.collector import DWMWA_CLOAKED, GCL_HICON, WM_GETICON, Collector
from arrangeit.windows.controller import Controller
from arrangeit.windows.utils import extract_name_from_bytes_path, user_data_path
from win32con import (
    GA_ROOTOWNER,
    STATE_SYSTEM_INVISIBLE,
    SW_MINIMIZE,
    SW_RESTORE,
    WS_EX_NOACTIVATE,
    WS_EX_TOOLWINDOW,
    WS_THICKFRAME,
)

SAMPLE_HWND = 1001


## arrangeit.windows.app
class TestWindowsApp(object):
    """Testing class for :class:`arrangeit.windowe.app.App` class."""

    ## WindowsApp.activate_root
    def test_WindowsApp_activate_root_calls_SetActiveWindow(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.windows.app.SetActiveWindow")
        app = App()
        app.activate_root(SAMPLE_HWND)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE_HWND)

    ## WindowsApp.move
    def test_WindowsApp_move_calls_move_and_resize(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.windows.app.App.move_and_resize")
        app = App()
        app.move(SAMPLE_HWND)
        mocked.assert_called()
        mocked.assert_called_with(SAMPLE_HWND)

    ## WindowsApp.move_and_resize
    def test_WindowsApp_move_and_resize_calls_get_model_by_wid(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        type(mocked.return_value).is_changed = mocker.PropertyMock(return_value=False)
        app = App()
        SAMPLE = 8001
        app.move_and_resize(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE)

    def test_WindowsApp_move_and_resize_calls_move_to_workspace(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.windows.app.App.move_to_workspace")
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        type(mocked_model.return_value).is_ws_changed = mocker.PropertyMock(
            return_value=True
        )
        type(mocked_model.return_value).is_changed = mocker.PropertyMock(
            return_value=False
        )
        SAMPLE_WS, SAMPLE_WID = 1005, 7002
        type(mocked_model.return_value).changed_ws = mocker.PropertyMock(
            return_value=SAMPLE_WS
        )
        app = App()
        app.move_and_resize(SAMPLE_WID)
        mocked.assert_called_with(SAMPLE_WID, SAMPLE_WS)

    def test_WindowsApp_move_and_resize_not_calling_move_to_workspace(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked = mocker.patch("arrangeit.windows.app.App.move_to_workspace")
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        type(mocked_model.return_value).is_ws_changed = mocker.PropertyMock(
            return_value=False
        )
        type(mocked_model.return_value).is_changed = mocker.PropertyMock(
            return_value=False
        )
        app = App()
        app.move_and_resize(100)
        mocked.assert_not_called()

    def test_WindowsApp_move_and_resize_calls_IsIconic(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        type(mocked_model.return_value).changed = mocker.PropertyMock(
            return_value=(72, 82, 501, 501)
        )
        mocker.patch("arrangeit.windows.app.MoveWindow")
        mocked = mocker.patch("arrangeit.windows.app.IsIconic")
        app = App()
        SAMPLE = 7402
        app.move_and_resize(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE)

    def test_WindowsApp_move_and_resize_calls_ShowWindow_if_iconic(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        type(mocked_model.return_value).changed = mocker.PropertyMock(
            return_value=(73, 83, 501, 501)
        )
        mocker.patch("arrangeit.windows.app.MoveWindow")
        mocker.patch("arrangeit.windows.app.IsIconic", return_value=True)
        mocked = mocker.patch("arrangeit.windows.app.ShowWindow")
        app = App()
        SAMPLE = 7403
        app.move_and_resize(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE, SW_RESTORE)

    def test_WindowsApp_move_and_resize_not_calling_ShowWindow_if_not_iconic(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        type(mocked_model.return_value).changed = mocker.PropertyMock(
            return_value=(74, 84, 501, 501)
        )
        mocker.patch("arrangeit.windows.app.MoveWindow")
        mocker.patch("arrangeit.windows.app.IsIconic", return_value=False)
        mocked = mocker.patch("arrangeit.windows.app.ShowWindow")
        app = App()
        app.move_and_resize(7404)
        mocked.assert_not_called()

    def test_WindowsApp_move_and_resize_calls_MoveWindow(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        CHANGED = (71, 81, 501, 501)
        type(mocked_model.return_value).changed = mocker.PropertyMock(
            return_value=CHANGED
        )
        mocked = mocker.patch("arrangeit.windows.app.MoveWindow")
        app = App()
        SAMPLE = 7401
        app.move_and_resize(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE, *CHANGED, True)

    def test_WindowsApp_move_and_resize_not_calling_MoveWindow(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        type(mocked_model.return_value).is_changed = mocker.PropertyMock(
            return_value=False
        )
        mocked = mocker.patch("arrangeit.windows.app.MoveWindow")
        app = App()
        app.move_and_resize(100)
        mocked.assert_not_called()

    def test_WindowsApp_move_and_resize_calls_ShowWindow_minimized(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.windows.app.MoveWindow")
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        mocker.patch("arrangeit.windows.app.IsIconic", return_value=False)
        type(mocked_model.return_value).changed = mocker.PropertyMock(
            return_value=(79, 89, 509, 509)
        )
        type(mocked_model.return_value).restored = mocker.PropertyMock(
            return_value=False
        )
        mocked = mocker.patch("arrangeit.windows.app.ShowWindow")
        app = App()
        SAMPLE = 7405
        app.move_and_resize(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE, SW_MINIMIZE)

    def test_WindowsApp_move_and_resize_not_calling_ShowWindow_minimized(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.windows.app.MoveWindow")
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        mocker.patch("arrangeit.windows.app.IsIconic", return_value=False)
        type(mocked_model.return_value).changed = mocker.PropertyMock(
            return_value=(89, 99, 409, 409)
        )
        type(mocked_model.return_value).restored = mocker.PropertyMock(
            return_value=True
        )
        mocked = mocker.patch("arrangeit.windows.app.ShowWindow")
        app = App()
        app.move_and_resize(7518)
        mocked.assert_not_called()

    def test_WindowsApp_move_and_resize_returns_False(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        mocker.patch("arrangeit.windows.app.MoveWindow")
        app = App()
        assert app.move_and_resize(100) is False

    def test_WindowsApp_move_and_resize_returns_True(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        type(mocked_model.return_value).is_changed = mocker.PropertyMock(
            return_value=False
        )
        app = App()
        assert app.move_and_resize(100) is True

    ## WindowsApp.move_to_workspace
    @pytest.mark.skip("Research how to deal with workspaces in MS Windows")
    def test_WindowsApp_move_to_workspace_(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")

    ## WindowsApp._window_area_desktop_screenshot
    def test_WindowsApp__window_area_desktop_screenshot_calls_GetWindowRect(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.BaseApp.setup_collector")
        mocker.patch("arrangeit.windows.app.ImageGrab")
        mocked = mocker.patch("arrangeit.windows.app.GetWindowRect")
        HWND = 101
        App()._window_area_desktop_screenshot(HWND)
        mocked.assert_called_once()
        mocked.assert_called_with(HWND)

    def test_WindowsApp__window_area_desktop_screenshot_calls_and_returns_grab(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.base.BaseApp.setup_collector")
        mocked_rect = mocker.patch("arrangeit.windows.app.GetWindowRect")
        mocked = mocker.patch("arrangeit.windows.app.ImageGrab")
        returned = App()._window_area_desktop_screenshot(102)
        mocked.grab.assert_called_once()
        mocked.grab.assert_called_with(mocked_rect.return_value)
        assert returned == mocked.grab.return_value

    ## WindowsApp.grab_window_screen
    def test_WindowsApp_grab_window_screen_calls_dwm_is_composition_enabled(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.windows.app.App._screenshot_with_thumbnails")
        mocker.patch("arrangeit.windows.app.get_prepared_screenshot")
        mocker.patch("arrangeit.windows.app.ImageTk")
        mocked = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        App().grab_window_screen(None, None)
        mocked.return_value.return_value.api.dwm_is_composition_enabled.assert_called_once()
        mocked.return_value.return_value.api.dwm_is_composition_enabled.assert_called_with()

    def test_WindowsApp_grab_window_screen_calls__screenshot_with_thumbnails(
        self, mocker
    ):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.windows.app.get_prepared_screenshot")
        mocker.patch("arrangeit.windows.app.ImageTk")
        mocked_collector = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        mocked_collector.return_value.return_value.api.dwm_is_composition_enabled.return_value = True
        mocked = mocker.patch("arrangeit.windows.app.App._screenshot_with_thumbnails")
        MODEL, ROOT_WID = 1, 2
        App().grab_window_screen(MODEL, ROOT_WID)
        mocked.assert_called_once()
        mocked.assert_called_with(MODEL, ROOT_WID)

    def test_WindowsApp_grab_window_screen_calls_get_prepared_screenshot(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked_screenhot = mocker.patch(
            "arrangeit.windows.app.App._screenshot_with_thumbnails"
        )
        mocker.patch("arrangeit.windows.app.ImageTk")
        mocked_collector = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        mocked_collector.return_value.return_value.api.dwm_is_composition_enabled.return_value = True
        mocked = mocker.patch("arrangeit.windows.app.get_prepared_screenshot")
        returned = App().grab_window_screen(2, 3)
        mocked.assert_called_once()
        mocked.assert_called_with(
            mocked_screenhot.return_value,
            blur_size=Settings.SCREENSHOT_BLUR_PIXELS,
            grayscale=Settings.SCREENSHOT_TO_GRAYSCALE,
        )
        assert returned == (mocked.return_value, (0, 0))

    def test_WindowsApp_grab_window_screen_returns_blank(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocker.patch("arrangeit.windows.app.App._screenshot_with_thumbnails")
        mocker.patch("arrangeit.windows.app.get_prepared_screenshot")
        mocked_collector = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        mocked_collector.return_value.return_value.api.dwm_is_composition_enabled.return_value = False
        mocked = mocker.patch("arrangeit.windows.app.ImageTk")
        returned = App().grab_window_screen(None, None)
        mocked.PhotoImage.assert_called_once()
        mocked.PhotoImage.assert_called_with(Settings.BLANK_ICON)
        assert returned == (mocked.PhotoImage.return_value, (0, 0))

    ## WindowsApp._screenshot_with_thumbnails
    def test_WindowsApp__screenshot_with_thumbnails_calls_Rectangle_lower(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_collector")
        mocker.patch("arrangeit.windows.app.App._window_area_desktop_screenshot")
        mocked_controller = mocker.patch("arrangeit.base.BaseApp.setup_controller")
        WIDTH, HEIGHT = 200, 300
        mocked_controller.return_value.return_value.default_size = (WIDTH, HEIGHT)
        mocked = mocker.patch("arrangeit.windows.app.Rectangle")
        model = mocker.MagicMock()
        App()._screenshot_with_thumbnails(model, 2050)
        calls = [mocker.call(0, HEIGHT, WIDTH, model.h)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_WindowsApp__screenshot_with_thumbnails_calls_setup_thumbnail_lower(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.app.App._window_area_desktop_screenshot")
        mocked_controller = mocker.patch("arrangeit.base.BaseApp.setup_controller")
        ROOT_WID = 2051
        mocked_controller.return_value.return_value.default_size = (3201, 301)
        mocked_rect = mocker.patch("arrangeit.windows.app.Rectangle")
        model = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        App()._screenshot_with_thumbnails(model, ROOT_WID)
        calls = [mocker.call(model.wid, ROOT_WID, mocked_rect.return_value)]
        mocked.return_value.return_value.api.setup_thumbnail.assert_has_calls(
            calls, any_order=True
        )

    def test_WindowsApp__screenshot_with_thumbnails_returns_blank_lower(self, mocker):
        mocker.patch("arrangeit.windows.app.App._window_area_desktop_screenshot")
        mocked_controller = mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked_controller.return_value.return_value.default_size = (3202, 302)
        mocker.patch("arrangeit.windows.app.Rectangle")
        mocked = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        mocked.return_value.return_value.api.setup_thumbnail.side_effect = [None, "foo"]
        assert App()._screenshot_with_thumbnails(mocker.MagicMock(), 2052) is Settings.BLANK_ICON

    def test_WindowsApp__screenshot_with_thumbnails_calls_Rectangle_right(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_collector")
        mocker.patch("arrangeit.windows.app.App._window_area_desktop_screenshot")
        mocked_controller = mocker.patch("arrangeit.base.BaseApp.setup_controller")
        WIDTH = 205
        mocked_controller.return_value.return_value.default_size = (WIDTH, 305)
        mocked = mocker.patch("arrangeit.windows.app.Rectangle")
        model = mocker.MagicMock()
        App()._screenshot_with_thumbnails(model, 2070)
        calls = [mocker.call(WIDTH, 0, model.w, model.h)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_WindowsApp__screenshot_with_thumbnails_calls_setup_thumbnail_right(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.app.App._window_area_desktop_screenshot")
        mocked_controller = mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked_controller.return_value.return_value.default_size = (3207, 321)
        mocker.patch("arrangeit.windows.app.Rectangle")
        model = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        App()._screenshot_with_thumbnails(model, 2088)
        assert mocked.return_value.return_value.api.setup_thumbnail.call_count == 2

    def test_WindowsApp__screenshot_with_thumbnails_returns_blank_right(self, mocker):
        mocker.patch("arrangeit.windows.app.App._window_area_desktop_screenshot")
        mocked_controller = mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked_controller.return_value.return_value.default_size = (202, 304)
        mocker.patch("arrangeit.windows.app.Rectangle")
        mocked = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        mocked.return_value.return_value.api.setup_thumbnail.side_effect = ["foo", None]
        assert App()._screenshot_with_thumbnails(mocker.MagicMock(), 2094) is Settings.BLANK_ICON

    def test_WindowsApp__screenshot_with_thumbnails_calls__window_area_desktop_scsh(
        self, mocker
    ):
        mocked_controller = mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked_controller.return_value.return_value.default_size = (587, 785)
        mocker.patch("arrangeit.windows.app.Rectangle")
        mocked_collector = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        mocked_collector.return_value.return_value.api.setup_thumbnail.side_effect = [
            "foo",
            "foo",
        ]
        mocked = mocker.patch(
            "arrangeit.windows.app.App._window_area_desktop_screenshot"
        )
        ROOT_WID = 5095
        App()._screenshot_with_thumbnails(mocker.MagicMock(), ROOT_WID)
        mocked.assert_called_once()
        mocked.assert_called_with(ROOT_WID)

    def test_WindowsApp__screenshot_with_thumbnails_calls_unregister_thumbnail(
        self, mocker
    ):
        mocked_controller = mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked_controller.return_value.return_value.default_size = (588, 795)
        mocker.patch("arrangeit.windows.app.Rectangle")
        mocked = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        THUMBNAIL1, THUMBNAIL2 = 500, 501
        mocked.return_value.return_value.api.setup_thumbnail.side_effect = [
            THUMBNAIL1,
            THUMBNAIL2,
        ]
        mocker.patch(
            "arrangeit.windows.app.App._window_area_desktop_screenshot"
        )
        App()._screenshot_with_thumbnails(mocker.MagicMock(), 5097)
        calls = [mocker.call(THUMBNAIL1), mocker.call(THUMBNAIL2)]
        mocked.return_value.return_value.api.unregister_thumbnail.assert_has_calls(calls, any_order=True)

    def test_WindowsApp__screenshot_with_thumbnails_returns__window_area_desktop_scsh(
        self, mocker
    ):
        mocked_controller = mocker.patch("arrangeit.base.BaseApp.setup_controller")
        mocked_controller.return_value.return_value.default_size = (587, 785)
        mocker.patch("arrangeit.windows.app.Rectangle")
        mocked_collector = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        mocked_collector.return_value.return_value.api.setup_thumbnail.side_effect = [
            "foo",
            "foo",
        ]
        mocked = mocker.patch(
            "arrangeit.windows.app.App._window_area_desktop_screenshot"
        )
        returned = App()._screenshot_with_thumbnails(mocker.MagicMock(), 5096)
        assert returned == mocked.return_value


## arrangeit.windows.collector
class TestWindowsCollector(object):
    """Testing class for :py:class:`arrangeit.windows.collector.Collector` class."""

    ## WindowsCollector.__init__
    def test_WindowsCollector__init__calls_super(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseCollector.__init__")
        Collector()
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_WindowsCollector__init__initializes_Api_and_sets_it_as_attribute(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.windows.collector.Api")
        collector = Collector()
        mocked.assert_called_once()
        mocked.assert_called_with()
        assert collector.api == mocked.return_value

    ## WindowsCollector._get_uwpapp_icon
    def test_WindowsCollector__get_uwpapp_icon_calls_get_package(self, mocker):
        SAMPLE = 220
        mocked = mocker.patch("arrangeit.windows.collector.Api")
        mocked.return_value.packages = {}
        Collector()._get_uwpapp_icon(SAMPLE)
        mocked.return_value.get_package.assert_called_once()
        mocked.return_value.get_package.assert_called_with(SAMPLE)

    def test_WindowsCollector__get_uwpapp_icon_sets_api_packages_for_hwnd(self, mocker):
        SAMPLE = 221
        mocked = mocker.patch("arrangeit.windows.collector.Api")
        mocked.return_value.packages = {}
        Collector()._get_uwpapp_icon(SAMPLE)
        assert (
            mocked.return_value.packages[SAMPLE]
            == mocked.return_value.get_package.return_value
        )

    def test_WindowsCollector__get_uwpapp_icon_returns_icon(self, mocker):
        mocker.patch("arrangeit.windows.api.Package.setup_package")
        SAMPLE = 222
        mocked = mocker.patch("arrangeit.windows.collector.Api")
        PACKAGE = Package("")
        mocked.return_value.packages = {SAMPLE: PACKAGE}
        returned = Collector()._get_uwpapp_icon(SAMPLE)
        assert returned == PACKAGE.icon

    ## WindowsCollector._get_application_icon
    def test_WindowsCollector__get_application_icon_calls_SendMessageTimeout(
        self, mocker
    ):
        mocker.patch(
            "arrangeit.windows.collector.Collector._get_image_from_icon_handle"
        )
        mocked = mocker.patch(
            "arrangeit.windows.collector.SendMessageTimeout", return_value=(0, 1)
        )
        SAMPLE = 108
        Collector()._get_application_icon(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE, WM_GETICON, 1, 0, 0, 50)

    def test_WindowsCollector__get_application_icon_calls_GetClassLong(self, mocker):
        mocker.patch(
            "arrangeit.windows.collector.Collector._get_image_from_icon_handle"
        )
        mocker.patch(
            "arrangeit.windows.collector.SendMessageTimeout", return_value=(0, 0)
        )
        mocked = mocker.patch(
            "arrangeit.windows.collector.GetClassLong", return_value=1
        )
        SAMPLE = 108
        Collector()._get_application_icon(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE, GCL_HICON)

    def test_WindowsCollector__get_application_icon_calls__get_uwpapp_icon(
        self, mocker
    ):
        mocker.patch(
            "arrangeit.windows.collector.Collector._get_image_from_icon_handle"
        )
        mocker.patch(
            "arrangeit.windows.collector.SendMessageTimeout", return_value=(0, 0)
        )
        mocker.patch("arrangeit.windows.collector.GetClassLong", return_value=0)
        mocked = mocker.patch("arrangeit.windows.collector.Collector._get_uwpapp_icon")
        SAMPLE = 452
        returned = Collector()._get_application_icon(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE)
        assert returned == mocked.return_value

    def test_WindowsCollector__get_application_icon_calls__get_image_from_icon_handle(
        self, mocker
    ):
        SAMPLE = 15002
        mocker.patch(
            "arrangeit.windows.collector.SendMessageTimeout", return_value=(0, SAMPLE)
        )
        mocked = mocker.patch(
            "arrangeit.windows.collector.Collector._get_image_from_icon_handle"
        )
        returned = Collector()._get_application_icon(100)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE)
        assert returned == mocked.return_value

    ## WindowsCollector.get_application_name
    def test_WindowsCollector_get_application_name_existing_package(self, mocker):
        mocked_api = mocker.patch("arrangeit.windows.collector.Api")
        HWND = 9715
        SAMPLE = "barfoo"
        PACKAGE = mocker.MagicMock()
        PACKAGE.app_name = SAMPLE
        mocked_api.return_value.packages = {HWND: PACKAGE}
        returned = Collector().get_application_name(HWND)
        assert returned == SAMPLE

    def test_WindowsCollector_get_application_name_calls_executable_name_for_hwnd(
        self, mocker
    ):
        mocked_api = mocker.patch("arrangeit.windows.collector.Api")
        mocked_api.return_value.packages = {}
        HWND = 9716
        Collector().get_application_name(HWND)
        mocked_api.return_value.executable_name_for_hwnd.assert_called_once()
        mocked_api.return_value.executable_name_for_hwnd.assert_called_with(HWND)

    def test_WindowsCollector_get_application_name_returns_executable_name_for_hwnd(
        self, mocker
    ):
        mocked_api = mocker.patch("arrangeit.windows.collector.Api")
        mocked_api.return_value.packages = {}
        SAMPLE = "foobar"
        mocked_api.return_value.executable_name_for_hwnd.return_value = SAMPLE
        returned = Collector().get_application_name(9717)
        assert returned == SAMPLE

    def test_WindowsCollector_get_application_name_returns_GetClassName_for_exe_None(
        self, mocker
    ):
        mocked_api = mocker.patch("arrangeit.windows.collector.Api")
        mocked_api.return_value.packages = {}
        mocked = mocker.patch("arrangeit.windows.collector.GetClassName")
        mocked_api.return_value.executable_name_for_hwnd.return_value = None
        returned = Collector().get_application_name(9718)
        assert returned == mocked.return_value

    @pytest.mark.parametrize("method", ["GetClassName"])
    def test_WindowsCollector_get_application_name_calls(self, mocker, method):
        mocked_api = mocker.patch("arrangeit.windows.collector.Api")
        mocked_api.return_value.packages = {}
        mocked_api.return_value.executable_name_for_hwnd.return_value = None
        mocked = mocker.patch("arrangeit.windows.collector.{}".format(method))
        Collector().get_application_name(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize("value", ["foo", "bar", ""])
    def test_WindowsCollector_get_application_name_functionality_no_package_no_app_name(
        self, mocker, value
    ):
        mocked_api = mocker.patch("arrangeit.windows.collector.Api")
        mocked_api.return_value.packages = {}
        mocked_api.return_value.executable_name_for_hwnd.return_value = None
        mocker.patch("arrangeit.windows.collector.GetClassName", return_value=value)
        assert Collector().get_application_name(SAMPLE_HWND) == value

    ## WindowsCollector._get_image_from_icon_handle
    def test_WindowsCollector__get_image_from_icon_handle_calls_GetDC(self, mocker):
        mocker.patch("arrangeit.windows.collector.CreateDCFromHandle")
        mocker.patch("arrangeit.windows.collector.CreateBitmap")
        mocker.patch("arrangeit.windows.collector.Image.frombuffer")
        mocked = mocker.patch("arrangeit.windows.collector.GetDC")
        Collector()._get_image_from_icon_handle(100)
        mocked.assert_called_once()
        mocked.assert_called_with(0)

    def test_WindowsCollector__get_image_from_icon_handle_calls_CreateDCFromHandle(
        self, mocker
    ):
        SAMPLE = 4545
        mocker.patch("arrangeit.windows.collector.GetDC", return_value=SAMPLE)
        mocker.patch("arrangeit.windows.collector.CreateBitmap")
        mocker.patch("arrangeit.windows.collector.Image.frombuffer")
        mocked = mocker.patch("arrangeit.windows.collector.CreateDCFromHandle")
        Collector()._get_image_from_icon_handle(100)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE)

    def test_WindowsCollector__get_image_from_icon_handle_calls_CreateBitmap(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.GetDC")
        mocker.patch("arrangeit.windows.collector.CreateDCFromHandle")
        mocker.patch("arrangeit.windows.collector.Image.frombuffer")
        mocked = mocker.patch("arrangeit.windows.collector.CreateBitmap")
        Collector()._get_image_from_icon_handle(100)
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_WindowsCollector__get_image_from_icon_handle_calls_bitmap_CreateCompatibleBitmap(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.GetDC")
        mocker.patch("arrangeit.windows.collector.CreateBitmap")
        mocker.patch("arrangeit.windows.collector.Image.frombuffer")
        mocked_create = mocker.patch("arrangeit.windows.collector.CreateDCFromHandle")
        mocked = mocker.patch("arrangeit.windows.collector.CreateBitmap")
        Collector()._get_image_from_icon_handle(100)
        mocked.return_value.CreateCompatibleBitmap.assert_called_once()
        mocked.return_value.CreateCompatibleBitmap.assert_called_with(
            mocked_create.return_value, Settings.ICON_SIZE, Settings.ICON_SIZE
        )

    def test_WindowsCollector__get_image_from_icon_handle_calls_dc_CreateCompatibleDC(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.GetDC")
        mocker.patch("arrangeit.windows.collector.CreateBitmap")
        mocker.patch("arrangeit.windows.collector.Image.frombuffer")
        mocked = mocker.patch("arrangeit.windows.collector.CreateDCFromHandle")
        Collector()._get_image_from_icon_handle(100)
        mocked.return_value.CreateCompatibleDC.assert_called_once()
        mocked.return_value.CreateCompatibleDC.assert_called_with()

    def test_WindowsCollector__get_image_from_icon_handle_calls_dc_SelectObject(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.GetDC")
        mocker.patch("arrangeit.windows.collector.Image.frombuffer")
        mocked_bitmap = mocker.patch("arrangeit.windows.collector.CreateBitmap")
        mocked = mocker.patch("arrangeit.windows.collector.CreateDCFromHandle")
        mocked_hdc = mocked.return_value.CreateCompatibleDC.return_value
        Collector()._get_image_from_icon_handle(100)
        mocked_hdc.SelectObject.assert_called_once()
        mocked_hdc.SelectObject.assert_called_with(mocked_bitmap.return_value)

    def test_WindowsCollector__get_image_from_icon_handle_calls_dc_DrawIcon(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.GetDC")
        mocker.patch("arrangeit.windows.collector.CreateBitmap")
        mocker.patch("arrangeit.windows.collector.Image.frombuffer")
        mocked = mocker.patch("arrangeit.windows.collector.CreateDCFromHandle")
        mocked_hdc = mocked.return_value.CreateCompatibleDC.return_value
        ICON_HANDLE = 54887
        Collector()._get_image_from_icon_handle(ICON_HANDLE)
        mocked_hdc.DrawIcon.assert_called_once()
        mocked_hdc.DrawIcon.assert_called_with((0, 0), ICON_HANDLE)

    def test_WindowsCollector__get_image_from_icon_handle_calls_bitmap_GetBitmapBits(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.GetDC")
        mocked = mocker.patch("arrangeit.windows.collector.CreateBitmap")
        mocker.patch("arrangeit.windows.collector.Image.frombuffer")
        mocker.patch("arrangeit.windows.collector.CreateDCFromHandle")
        Collector()._get_image_from_icon_handle(100)
        mocked.return_value.GetBitmapBits.assert_called_once()
        mocked.return_value.GetBitmapBits.assert_called_with(True)

    def test_WindowsCollector__get_image_from_icon_handle_calls_Image_frombuffer(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.GetDC")
        mocked_bitmap = mocker.patch("arrangeit.windows.collector.CreateBitmap")
        mocker.patch("arrangeit.windows.collector.CreateDCFromHandle")
        mocked = mocker.patch("arrangeit.windows.collector.Image.frombuffer")
        returned = Collector()._get_image_from_icon_handle(100)
        mocked.assert_called_once()
        mocked.assert_called_with(
            "RGBA",
            (Settings.ICON_SIZE, Settings.ICON_SIZE),
            mocked_bitmap.return_value.GetBitmapBits.return_value,
            "raw",
            "BGRA",
            0,
            1,
        )
        assert returned == mocked.return_value

    ## WindowsCollector._get_window_geometry
    def test_WindowsCollector__get_window_geometry_calls(self, mocker):
        mocked = mocker.patch(
            "arrangeit.windows.collector.GetWindowPlacement",
            return_value=(0, 0, (0, 0), (0, 0), (0, 0, 0, 0)),
        )
        Collector()._get_window_geometry(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "rect,expected",
        [
            ((0, 0, (0, 0), (0, 0), (0, 0, 200, 300)), (0, 0, 200, 300)),
            ((0, 0, (0, 0), (0, 0), (100, 200, 200, 300)), (100, 200, 100, 100)),
            ((0, 0, (0, 0), (0, 0), (500, 400, 700, 500)), (500, 400, 200, 100)),
            ((0, 0, (0, 0), (0, 0), (200, 200, 200, 300)), (200, 200, 0, 100)),
        ],
    )
    def test_WindowsCollector__get_window_geometry_functionality(
        self, mocker, rect, expected
    ):
        mocker.patch(
            "arrangeit.windows.collector.GetWindowPlacement", return_value=rect
        )
        assert Collector()._get_window_geometry(SAMPLE_HWND) == expected

    ## WindowsCollector._get_window_title
    @pytest.mark.parametrize("method", ["GetWindowText"])
    def test_WindowsCollector__get_window_title_calls(self, mocker, method):
        mocked = mocker.patch("arrangeit.windows.collector.{}".format(method))
        Collector()._get_window_title(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize("value", ["foo", "bar", ""])
    def test_WindowsCollector__get_window_title_functionality(self, mocker, value):
        mocker.patch("arrangeit.windows.collector.GetWindowText", return_value=value)
        assert Collector()._get_window_title(SAMPLE_HWND) == value

    ## WindowsCollector._is_activable
    def test_WindowsCollector__is_activable_calls_window_info_extended_style(
        self, mocker
    ):
        mocked = mocker.patch(
            "arrangeit.windows.collector.Api.window_info_extended_style"
        )
        Collector()._is_activable(SAMPLE_HWND)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE_HWND, WS_EX_NOACTIVATE)

    @pytest.mark.parametrize("value,expected", [(0, True), (1, False)])
    def test_WindowsCollector__is_activable_return(self, mocker, value, expected):
        mocker.patch(
            "arrangeit.windows.collector.Api.window_info_extended_style",
            return_value=value,
        )
        assert Collector()._is_activable(SAMPLE_HWND) == expected

    ## WindowsCollector._is_alt_tab_applicable
    def test_WindowsCollector__is_alt_tab_applicable_calls_get_ancestor_by_type(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.Api.get_last_active_popup")
        mocker.patch("arrangeit.windows.collector.IsWindowVisible")
        mocked = mocker.patch("arrangeit.windows.collector.Api.get_ancestor_by_type")
        Collector()._is_alt_tab_applicable(SAMPLE_HWND)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE_HWND, GA_ROOTOWNER)

    def test_WindowsCollector__is_alt_tab_applicable_calls_get_last_active_popup(
        self, mocker
    ):
        mocked_ancestor = mocker.patch(
            "arrangeit.windows.collector.Api.get_ancestor_by_type"
        )
        mocker.patch("arrangeit.windows.collector.IsWindowVisible")
        mocked = mocker.patch("arrangeit.windows.collector.Api.get_last_active_popup")
        Collector()._is_alt_tab_applicable(SAMPLE_HWND)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_ancestor.return_value)

    def test_WindowsCollector__is_alt_tab_applicable_calls_IsWindowVisible(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.Api.get_ancestor_by_type")
        mocked_popup = mocker.patch(
            "arrangeit.windows.collector.Api.get_last_active_popup"
        )
        mocked = mocker.patch("arrangeit.windows.collector.IsWindowVisible")
        Collector()._is_alt_tab_applicable(SAMPLE_HWND)
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_popup.return_value)

    def test_WindowsCollector__is_alt_tab_applicable_return_True(self, mocker):
        VALUE = 500
        mocker.patch(
            "arrangeit.windows.collector.Api.get_ancestor_by_type", return_value=VALUE
        )
        mocker.patch(
            "arrangeit.windows.collector.Api.get_last_active_popup", return_value=VALUE
        )
        mocker.patch("ctypes.windll.user32.GetAncestor", return_value=VALUE)
        mocker.patch("ctypes.windll.user32.GetLastActivePopup", return_value=VALUE)
        mocker.patch("arrangeit.windows.collector.IsWindowVisible", return_value=True)
        assert Collector()._is_alt_tab_applicable(VALUE)

    def test_WindowsCollector__is_alt_tab_applicable_return_False(self, mocker):
        mocker.patch(
            "arrangeit.windows.collector.Api.get_ancestor_by_type", return_value=500
        )
        mocker.patch(
            "arrangeit.windows.collector.Api.get_last_active_popup", return_value=499
        )
        mocker.patch("arrangeit.windows.collector.IsWindowVisible", return_value=True)
        assert not Collector()._is_alt_tab_applicable(SAMPLE_HWND)

    ## WindowsCollector._is_cloaked
    def test_WindowsCollector__is_cloaked_calls_dwm_window_attribute_value(
        self, mocker
    ):
        mocked = mocker.patch(
            "arrangeit.windows.collector.Api.dwm_window_attribute_value"
        )
        Collector()._is_cloaked(SAMPLE_HWND)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE_HWND, DWMWA_CLOAKED)

    @pytest.mark.parametrize("value,expected", [(0, False), (1, True), (2, True)])
    def test_WindowsCollector__is_cloaked_return(self, mocker, value, expected):
        mocker.patch(
            "arrangeit.windows.collector.Api.dwm_window_attribute_value",
            return_value=value,
        )
        assert Collector()._is_cloaked(SAMPLE_HWND) == expected

    ## WindowsCollector._is_tool_window
    @pytest.mark.parametrize("method", ["GetWindowLong"])
    def test_WindowsCollector__is_tool_window_calls(self, mocker, method):
        mocked = mocker.patch("arrangeit.windows.collector.{}".format(method))
        Collector()._is_tool_window(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "value,expected", [(1024 + WS_EX_TOOLWINDOW, True), (1023, False)]
    )
    def test_WindowsCollector__is_tool_window_return(self, mocker, value, expected):
        mocker.patch("arrangeit.windows.collector.GetWindowLong", return_value=value)
        assert Collector()._is_tool_window(SAMPLE_HWND)

    ## WindowsCollector._is_tray_window
    def test_WindowsCollector__is_tray_window_calls_title_info_state(self, mocker):
        mocked = mocker.patch("arrangeit.windows.collector.Api.title_info_state")
        Collector()._is_tray_window(SAMPLE_HWND)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE_HWND, STATE_SYSTEM_INVISIBLE)

    @pytest.mark.parametrize("value,expected", [(0, False), (1, True)])
    def test_WindowsCollector__is_tray_window_return(self, mocker, value, expected):
        mocker.patch(
            "arrangeit.windows.collector.Api.title_info_state", return_value=value
        )
        assert Collector()._is_tray_window(SAMPLE_HWND) == expected

    ## WindowsCollector.add_window
    def test_WindowsCollector_add_window_calls_WindowsCollection_add(self, mocker):
        mocked = mocker.patch("arrangeit.data.WindowsCollection.add")
        mocker.patch("arrangeit.windows.collector.Collector._get_window_geometry")
        mocker.patch("arrangeit.windows.collector.Collector._get_window_title")
        mocker.patch("arrangeit.windows.collector.Collector.get_application_name")
        mocker.patch("arrangeit.windows.collector.Collector._get_application_icon")
        Collector().add_window(SAMPLE_HWND)
        mocked.assert_called_once()

    def test_WindowsCollector_add_window_inits_WindowModel(self, mocker):
        mocker.patch("arrangeit.data.WindowsCollection.add")
        mocked_rect = mocker.patch(
            "arrangeit.windows.collector.Collector._get_window_geometry"
        )
        mocked_resizable = mocker.patch(
            "arrangeit.windows.collector.Collector.is_resizable"
        )
        mocked_restored = mocker.patch(
            "arrangeit.windows.collector.Collector.is_restored", return_value=True
        )
        mocked_title = mocker.patch(
            "arrangeit.windows.collector.Collector._get_window_title"
        )
        mocked_name = mocker.patch(
            "arrangeit.windows.collector.Collector.get_application_name"
        )
        mocked_icon = mocker.patch(
            "arrangeit.windows.collector.Collector._get_application_icon"
        )
        mocked_ws = mocker.patch(
            "arrangeit.windows.collector.Collector.get_workspace_number_for_window"
        )
        mocked = mocker.patch("arrangeit.windows.collector.WindowModel")
        Collector().add_window(SAMPLE_HWND)
        mocked.assert_called_once()
        mocked.assert_called_with(
            wid=SAMPLE_HWND,
            rect=mocked_rect.return_value,
            resizable=mocked_resizable.return_value,
            restored=mocked_restored.return_value,
            title=mocked_title.return_value,
            name=mocked_name.return_value,
            icon=mocked_icon.return_value,
            workspace=mocked_ws.return_value,
        )

    @pytest.mark.parametrize(
        "method",
        [
            "_get_window_geometry",
            "is_resizable",
            "is_restored",
            "_get_window_title",
            "get_application_name",
            "_get_application_icon",
            "get_workspace_number_for_window",
        ],
    )
    def test_WindowsCollector_add_window_calls_methods(self, mocker, method):
        mocker.patch("arrangeit.windows.collector.Collector._get_window_geometry")
        mocker.patch("arrangeit.windows.collector.Collector._get_window_title")
        mocker.patch("arrangeit.windows.collector.Collector.get_application_name")
        mocker.patch("arrangeit.windows.collector.Collector._get_application_icon")
        mocked = mocker.patch("arrangeit.windows.collector.Collector.{}".format(method))
        Collector().add_window(SAMPLE_HWND)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE_HWND)

    ## WindowsCollector.check_window
    @pytest.mark.parametrize("method", ["is_applicable", "is_valid_state"])
    def test_WindowsCollector_check_window_calls(self, mocker, method):
        mocker.patch(
            "arrangeit.windows.collector.Collector.is_applicable", return_value=True
        )
        mocked = mocker.patch("arrangeit.windows.collector.Collector.{}".format(method))
        Collector().check_window(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "is_applicable,is_valid_state,expected",
        [
            (True, True, True),
            (False, True, False),
            (True, False, False),
            (False, False, False),
        ],
    )
    def test_WindowsCollector_check_window_functionality(
        self, mocker, is_applicable, is_valid_state, expected
    ):
        mocker.patch(
            "arrangeit.windows.collector.Collector.is_applicable",
            return_value=is_applicable,
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector.is_valid_state",
            return_value=is_valid_state,
        )
        assert Collector().check_window(SAMPLE_HWND) == expected

    ## WindowsCollector.get_available_workspaces
    @pytest.mark.skip("Research how to deal with workspaces in MS Windows")
    def test_WindowsCollector_get_available_workspaces_(self, mocker):
        pass

    ## WindowsCollector.get_monitors_rects
    def test_WindowsCollector_get_monitors_rects_calls_EnumDisplayMonitors(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.windows.collector.EnumDisplayMonitors")
        Collector().get_monitors_rects()
        mocked.assert_called_once()
        mocked.assert_called_with(None, None)

    def test_WindowsCollector_get_monitors_rects_returns_list_of_rect_parts(
        self, mocker
    ):
        RECT1, RECT2 = (0, 0, 1920, 1280), (1920, 0, 1280, 1080)
        SAMPLE = [
            (mocker.MagicMock(), mocker.MagicMock(), RECT1),
            (mocker.MagicMock(), mocker.MagicMock(), RECT2),
        ]
        mocker.patch(
            "arrangeit.windows.collector.EnumDisplayMonitors", return_value=SAMPLE
        )
        returned = Collector().get_monitors_rects()
        assert returned == [RECT1, RECT2]

    # WindowsCollector.get_windows
    def test_WindowsCollector_get_windows_calls_api_enum_windows(self, mocker):
        mocked = mocker.patch("arrangeit.windows.collector.Api.enum_windows")
        returned = Collector().get_windows()
        mocked.assert_called_once()
        mocked.assert_called_with()
        assert returned == mocked.return_value

    ## WindowsCollector.get_workspace_number_for_window
    @pytest.mark.skip("Research how to deal with workspaces in MS Windows")
    def test_WindowsCollector_get_workspace_number_for_window_(self, mocker):
        pass

    ## WindowsCollector.is_applicable
    @pytest.mark.parametrize(
        "method",
        [
            "IsWindow",
            "IsWindowEnabled",
            "IsWindowVisible",
            "Collector._is_alt_tab_applicable",
            "Collector._is_tray_window",
            "Collector._is_tool_window",
        ],
    )
    def test_WindowsCollector_is_applicable_calls(self, mocker, method):
        mocker.patch("arrangeit.windows.collector.IsWindow", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowEnabled", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowVisible", return_value=True)
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_alt_tab_applicable",
            return_value=True,
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_tray_window", return_value=False
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_tool_window", return_value=False
        )
        mocked = mocker.patch("arrangeit.windows.collector.{}".format(method))
        Collector().is_applicable(SAMPLE_HWND)
        mocked.assert_called_once()

    def test_WindowsCollector_is_applicable_returns_False_for_not_IsWindow(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.IsWindow", return_value=False)
        mocker.patch("arrangeit.windows.collector.IsWindowEnabled", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowVisible", return_value=True)
        assert Collector().is_applicable(SAMPLE_HWND) is False

    def test_WindowsCollector_is_applicable_returns_False_for_not_IsWindowEnabled(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.IsWindow", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowEnabled", return_value=False)
        mocker.patch("arrangeit.windows.collector.IsWindowVisible", return_value=True)
        assert Collector().is_applicable(SAMPLE_HWND) is False

    def test_WindowsCollector_is_applicable_returns_False_for_not_IsWindowVisible(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.IsWindow", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowEnabled", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowVisible", return_value=False)
        assert Collector().is_applicable(SAMPLE_HWND) is False

    def test_WindowsCollector_is_applicable_returns_False_for_not__is_alt_tab_applicable(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.IsWindow", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowEnabled", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowVisible", return_value=True)
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_alt_tab_applicable",
            return_value=False,
        )
        assert Collector().is_applicable(SAMPLE_HWND) is False

    def test_WindowsCollector_is_applicable_returns_False_for__is_tray_window(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.IsWindow", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowEnabled", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowVisible", return_value=True)
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_alt_tab_applicable",
            return_value=True,
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_tray_window", return_value=True
        )
        assert Collector().is_applicable(SAMPLE_HWND) is False

    def test_WindowsCollector_is_applicable_returns_False_for__is_tool_window(
        self, mocker
    ):
        mocker.patch("arrangeit.windows.collector.IsWindow", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowEnabled", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowVisible", return_value=True)
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_alt_tab_applicable",
            return_value=True,
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_tray_window", return_value=False
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_tool_window", return_value=True
        )
        assert Collector().is_applicable(SAMPLE_HWND) is False

    def test_WindowsCollector_is_applicable_returns_True(self, mocker):
        mocker.patch("arrangeit.windows.collector.IsWindow", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowEnabled", return_value=True)
        mocker.patch("arrangeit.windows.collector.IsWindowVisible", return_value=True)
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_alt_tab_applicable",
            return_value=True,
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_tray_window", return_value=False
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector._is_tool_window", return_value=False
        )
        assert Collector().is_applicable(SAMPLE_HWND) is True

    ## WindowsCollector.is_resizable
    @pytest.mark.parametrize("method", ["GetWindowLong"])
    def test_WindowsCollector_is_resizable_calls(self, mocker, method):
        mocked = mocker.patch("arrangeit.windows.collector.{}".format(method))
        Collector().is_resizable(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "value,expected", [(WS_THICKFRAME, True), (WS_THICKFRAME - 1, False)]
    )
    def test_WindowsCollector_is_resizable_return(self, mocker, value, expected):
        mocker.patch("arrangeit.windows.collector.GetWindowLong", return_value=value)
        assert Collector().is_resizable(SAMPLE_HWND) == expected

    ## WindowsCollector.is_restored
    @pytest.mark.parametrize("method", ["IsIconic"])
    def test_WindowsCollector_is_restored_calls(self, mocker, method):
        mocked = mocker.patch("arrangeit.windows.collector.{}".format(method))
        Collector().is_restored(SAMPLE_HWND)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE_HWND)

    @pytest.mark.parametrize("value,expected", [(False, True), (True, False)])
    def test_WindowsCollector_is_restored_return(self, mocker, value, expected):
        mocker.patch("arrangeit.windows.collector.IsIconic", return_value=value)
        assert Collector().is_restored(SAMPLE_HWND) == expected

    ## WindowsCollector.is_valid_state
    @pytest.mark.parametrize("method", ["_is_activable"])
    def test_WindowsCollector_is_valid_state_calls(self, mocker, method):
        mocked = mocker.patch("arrangeit.windows.collector.Collector.{}".format(method))
        Collector().is_valid_state(SAMPLE_HWND)
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "method,value,expected",
        [("_is_activable", True, True), ("_is_activable", False, False)],
    )
    def test_WindowsCollector_is_valid_state_return_value(
        self, mocker, method, value, expected
    ):
        mocker.patch(
            "arrangeit.windows.collector.Collector.{}".format(method),
            return_value=value,
        )
        assert Collector().is_valid_state(SAMPLE_HWND) == expected

    ## WindowsCollector.run
    @pytest.mark.parametrize(
        "is_applicable,is_valid_state,value",
        [
            ((True, True), (True, True), 2),
            ((True, True), (True, False), 1),
            ((False, True), (True, True), 1),
            ((True, False), (False, True), 0),
            ((False, False), (False, False), 0),
        ],
    )
    def test_WindowsCollector_run_functionality(
        self, mocker, is_applicable, is_valid_state, value
    ):
        mocker.patch("arrangeit.windows.collector.Collector._get_window_geometry")
        mocker.patch("arrangeit.windows.collector.Collector._get_window_title")
        mocker.patch("arrangeit.windows.collector.Collector.get_application_name")
        mocker.patch("arrangeit.windows.collector.Collector._get_application_icon")
        mocker.patch(
            "arrangeit.windows.collector.Collector.get_windows",
            return_value=(mocker.MagicMock(), mocker.MagicMock()),
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector.is_applicable",
            side_effect=is_applicable,
        )
        mocker.patch(
            "arrangeit.windows.collector.Collector.is_valid_state",
            side_effect=is_valid_state,
        )
        collector = Collector()
        collector.run()
        assert collector.collection.size == value


## arrangeit.windows.controller
class TestWindowsController(object):
    """Testing class for :py:class:`arrangeit.windows.controller.Controller` class."""

    ## Controller
    def test_WindowsController_inits_screenshot_when_exposed_as_True(self):
        assert Controller.screenshot_when_exposed is True

    ## Controller.setup_root_window
    def test_WindowsController_setup_root_window_calls_root_overrideredirect(
        self, mocker
    ):
        root = mocker.patch("arrangeit.base.get_tkinter_root")
        mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
        mocker.patch("arrangeit.base.ViewApplication")
        Controller(mocker.MagicMock()).setup_root_window(root)
        root.overrideredirect.assert_called_once()
        calls = [mocker.call(True)]
        root.overrideredirect.assert_has_calls(calls, any_order=True)

    def test_WindowsController_setup_root_window_calls_super(self, mocker):
        root = mocker.patch("arrangeit.base.get_tkinter_root")
        mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
        mocker.patch("arrangeit.base.ViewApplication")
        mocked = mocker.patch("arrangeit.base.BaseController.setup_root_window")
        controller = Controller(mocker.MagicMock())
        mocked.reset_mock()
        controller.setup_root_window(root)
        mocked.assert_called_once()
        calls = [mocker.call(root)]
        mocked.assert_has_calls(calls, any_order=True)


## arrangeit.windows.utils
class TestWindowsUtils(object):
    """Testing class for `arrangeit.windows.utils` module."""

    ## extract_name_from_bytes_path
    def test_windows_utils_module_extract_name_from_bytes_path_calls_basename(
        self, mocker
    ):
        SAMPLE = b"foobar"
        mocker.patch("os.path.splitext")
        mocker.patch("sys.getdefaultencoding", return_value="utf-8")
        mocked = mocker.patch("os.path.basename")
        extract_name_from_bytes_path(SAMPLE)
        mocked.assert_called_once()
        mocked.assert_called_with(SAMPLE)

    def test_windows_utils_module_extract_name_from_bytes_path_calls_splitext(
        self, mocker
    ):
        NAME, EXT = b"foobar", b"exe"
        mocker.patch("sys.getdefaultencoding", return_value="utf-8")
        mocked = mocker.patch("os.path.splitext", return_value=(NAME, EXT))
        mocked_basename = mocker.patch("os.path.basename")
        returned = extract_name_from_bytes_path(b"foo")
        mocked.assert_called_once()
        mocked.assert_called_with(mocked_basename.return_value)
        assert returned == "foobar"

    def test_windows_utils_module_extract_name_from_bytes_path_getdefaultencoding(
        self, mocker
    ):
        mocker.patch("os.path.splitext")
        mocker.patch("os.path.basename")
        mocked = mocker.patch("sys.getdefaultencoding", return_value="utf-8")
        extract_name_from_bytes_path(b"foo")
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_windows_utils_module_extract_name_from_bytes_path_decode(self, mocker):
        mocked = mocker.MagicMock()
        mocker.patch("os.path.splitext", return_value=(mocked, b"exe"))
        mocked.reset_mock()
        mocker.patch("os.path.basename")
        mocked_default = mocker.patch("sys.getdefaultencoding", return_value="utf-8")
        extract_name_from_bytes_path(b"foo")
        mocked.decode.assert_called_once()
        mocked.decode.assert_called_with(mocked_default.return_value)

    @pytest.mark.parametrize(
        "path,name",
        [
            (
                b"\\Device\\HarddiskVolume2\\Program Files\\Internet Explorer\\iexplore.exe",
                "iexplore",
            ),
            (
                b"\\Device\\HarddiskVolume2\\Program Files\\Git\\usr\\bin\\mintty.exe",
                "mintty",
            ),
            (b"\\Device\\HarddiskVolume1\\temp.ext.exe", "temp.ext"),
        ],
    )
    def test_windows_utils_module_extract_name_from_bytes_path_functionality(
        self, path, name
    ):
        assert extract_name_from_bytes_path(path) == name

    ## WindowsUtils.user_data_path
    def test_windows_utils_module_user_data_path(self, mocker):
        mocker.patch(
            "os.path.expanduser",
            side_effect=lambda e: "C:\\Users\\tempuser{}".format(e).replace("~", ""),
        )
        assert user_data_path() == "C:\\Users\\tempuser\\arrangeit"
