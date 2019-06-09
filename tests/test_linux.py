import os

import gi

gi.require_version("Wnck", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Wnck, GdkPixbuf
from PIL import Image, ImageTk
from Xlib import X
import pytest

import arrangeit
from arrangeit.data import WindowModel
from arrangeit.linux.app import App
from arrangeit.linux.collector import Collector, MOVE_RESIZE_MASKS
from arrangeit.linux.controller import Controller
from arrangeit.linux.utils import user_data_path


class TestLinuxUtils(object):
    """Testing class for `arrangeit.linux.utils` module."""

    ## LinuxUtils.user_data_path
    def test_linux_utils_module_user_data_path_checks_local_share_first(self, mocker):
        mocked_expand = mocker.patch(
            "os.path.expanduser",
            side_effect=lambda e: "/home/tempuser/{}".format(e).replace("~/", ""),
        )
        mocked_exists = mocker.patch("arrangeit.base.os.path.exists")
        user_data_path()
        calls = [mocker.call("/home/tempuser/.local/share")]
        mocked_exists.assert_has_calls(calls, any_order=True)
        calls = [mocker.call("~/.local/share/arrangeit")]
        mocked_expand.assert_has_calls(calls, any_order=True)

    def test_linux_utils_module__user_data_path_for_local_share_not_exists(
        self, mocker
    ):
        mocker.patch(
            "os.path.expanduser",
            side_effect=lambda e: "/home/tempuser/{}".format(e).replace("~/", ""),
        )
        mocker.patch("arrangeit.base.os.path.exists", return_value=False)
        assert user_data_path() == "/home/tempuser/.arrangeit"


class TestLinuxApp(object):
    """Testing class for :class:`arrangeit.linux.app.App` class."""

    ## LinuxApp.grab_window_screen
    def test_LinuxApp_grab_window_screen_calls_get_window_stack(self, mocker):
        mocked = mocker.patch("arrangeit.linux.app.Gdk.Screen.get_default")
        App().grab_window_screen(mocker.MagicMock())
        mocked.return_value.get_window_stack.assert_called_once()

    def test_LinuxApp_grab_window_screen_for_no_window_returns_empty_icon(self, mocker):
        mocked = mocker.patch("arrangeit.linux.app.Gdk.Screen.get_default")
        mocked.return_value.get_window_stack.return_value = [mocker.MagicMock()]
        returned = App().grab_window_screen(mocker.MagicMock())
        assert isinstance(returned[0], ImageTk.PhotoImage)
        assert returned[1] == (0, 0)

    def test_LinuxApp_grab_window_screen_calls_pixbuf_get_from_window(self, mocker):
        mocker.patch("arrangeit.linux.collector.Collector.get_image_from_pixbuf")
        mocker.patch("arrangeit.linux.app.ImageTk.PhotoImage")
        mocked_default = mocker.patch("arrangeit.linux.app.Gdk.Screen.get_default")
        mocked_model = mocker.MagicMock()
        type(mocked_model).wid = mocker.PropertyMock(return_value=100)
        mocked_window = mocker.MagicMock()
        mocked_window.get_xid.return_value = 100
        mocked_default.return_value.get_window_stack.return_value = [mocked_window]
        mocked = mocker.patch("arrangeit.linux.app.Gdk.pixbuf_get_from_window")
        App().grab_window_screen(mocked_model)
        mocked.assert_called_once()

    def test_LinuxApp_grab_window_screen_returns_get_prepared_screenshot_image(self, mocker):
        mocker.patch("arrangeit.linux.collector.Collector.get_image_from_pixbuf")
        mocked_photo = mocker.patch("arrangeit.linux.app.get_prepared_screenshot")
        mocked_default = mocker.patch("arrangeit.linux.app.Gdk.Screen.get_default")
        mocked_model = mocker.MagicMock()
        mocked_model.changed_w = 500
        mocked_model.changed_h = 400
        type(mocked_model).wid = mocker.PropertyMock(return_value=100)
        mocked_window = mocker.MagicMock()
        mocked_window.get_xid.return_value = 100
        mocked_window.get_width.return_value = 450
        mocked_window.get_height.return_value = 340
        mocked_default.return_value.get_window_stack.return_value = [mocked_window]
        mocker.patch("arrangeit.linux.app.Gdk.pixbuf_get_from_window")
        returned = App().grab_window_screen(mocked_model)
        assert returned[0] == mocked_photo.return_value
        assert returned[1] == (50, 60)

    ## LinuxApp.move_and_resize
    def test_LinuxApp_move_and_resize_calls_get_model_by_wid(self, mocker):
        mocked = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        app = App()
        with pytest.raises(AttributeError):
            app.move_and_resize(100)
        mocked.assert_called()

    def test_LinuxApp_move_and_resize_calls__move_window_to_workspace(self, mocker):
        mocked = mocker.patch("arrangeit.linux.app.App._move_window_to_workspace")
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        type(mocked_model.return_value).is_ws_changed = mocker.PropertyMock(
            return_value=True
        )
        type(mocked_model.return_value).changed_ws = mocker.PropertyMock(
            return_value=1005
        )
        app = App()
        with pytest.raises(AttributeError):
            app.move_and_resize(100)
        mocked.assert_called_with(100, 1005)

    def test_LinuxApp_move_and_resize_not_calling__move_window_to_workspace(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.linux.app.App._move_window_to_workspace")
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        type(mocked_model.return_value).is_ws_changed = mocker.PropertyMock(
            return_value=False
        )
        app = App()
        with pytest.raises(AttributeError):
            app.move_and_resize(100)
        mocked.assert_not_called()

    def test_LinuxApp_move_and_resize_calls_get_window_move_resize_mask(self, mocker):
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector.get_window_move_resize_mask"
        )
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        type(mocked_model.return_value).is_ws_changed = mocker.PropertyMock(
            return_value=False
        )
        app = App()
        with pytest.raises(AttributeError):
            app.move_and_resize(100)
        mocked.assert_called()

    def test_LinuxApp_move_and_resize_calls_get_window_by_wid(self, mocker):
        mocked = mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocker.patch("arrangeit.linux.collector.Collector.get_window_move_resize_mask")
        mocked_model = mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        type(mocked_model.return_value).is_ws_changed = mocker.PropertyMock(
            return_value=False
        )
        app = App()
        app.move_and_resize(100)
        mocked.assert_called()

    def test_LinuxApp_move_and_resize_not_calling_get_window_by_wid(self, mocker):
        mocked = mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocker.patch(
            "arrangeit.linux.collector.Collector.get_window_move_resize_mask",
            return_value=False,
        )
        mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        app = App()
        app.move_and_resize(100)
        assert mocked.return_value.set_geometry.call_count == 0

    def test_LinuxApp_move_and_resize_calls_WnckWindow_set_geometry(self, mocker):
        mocked = mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocker.patch("arrangeit.linux.collector.Collector.get_window_move_resize_mask")
        mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        app = App()
        app.move_and_resize(100)
        assert mocked.return_value.set_geometry.call_count == 1

    def test_LinuxApp_move_and_resize_checks_maximized(self, mocker):
        mocked = mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocker.patch("arrangeit.linux.collector.Collector.get_window_move_resize_mask")
        mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        app = App()
        app.move_and_resize(100)
        assert mocked.return_value.is_maximized.call_count == 1

    def test_LinuxApp_move_and_resize_calls_unmaximize(self, mocker):
        mocked = mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocker.patch("arrangeit.linux.collector.Collector.get_window_move_resize_mask")
        mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        mocked.return_value.is_maximized.return_value = True
        app = App()
        app.move_and_resize(100)
        mocked.return_value.unmaximize.assert_called_once()

    def test_LinuxApp_move_and_resize_not_calling_unmaximize(self, mocker):
        mocked = mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocker.patch("arrangeit.linux.collector.Collector.get_window_move_resize_mask")
        mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        mocked.return_value.is_maximized.return_value = False
        app = App()
        app.move_and_resize(100)
        mocked.return_value.unmaximize.assert_not_called()

    def test_LinuxApp_move_and_resize_not_calling_WnckWindow_set_geometry(self, mocker):
        mocked = mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocker.patch(
            "arrangeit.linux.collector.Collector.get_window_move_resize_mask",
            return_value=False,
        )
        mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        app = App()
        app.move_and_resize(100)
        assert mocked.return_value.set_geometry.call_count == 0

    def test_LinuxApp_move_and_resize_returns_False(self, mocker):
        mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocker.patch("arrangeit.linux.collector.Collector.get_window_move_resize_mask")
        mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        app = App()
        assert app.move_and_resize(100) is False

    def test_LinuxApp_move_and_resize_returns_True(self, mocker):
        mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocker.patch(
            "arrangeit.linux.collector.Collector.get_window_move_resize_mask",
            return_value=False,
        )
        mocker.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
        app = App()
        assert app.move_and_resize(100) is True

    ## LinuxApp.move
    def test_LinuxApp_move_calls_move_and_resize(self, mocker):
        mocked = mocker.patch("arrangeit.linux.app.App.move_and_resize")
        app = App()
        app.move(100)
        mocked.assert_called()
        mocked.assert_called_with(100)

    ## LinuxApp._activate_workspace
    def test_LinuxApp__activate_workspace_calls__get_wnck_workspace_for_custom(
        self, mocker
    ):
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector.get_wnck_workspace_for_custom_number"
        )
        app = App()
        app._activate_workspace(1000)
        mocked.assert_called()
        mocked.assert_called_with(1000)

    def test_LinuxApp__activate_workspace_calls_Wnck_Workspace_activate(self, mocker):
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector.get_wnck_workspace_for_custom_number"
        )
        app = App()
        app._activate_workspace(1000)
        assert mocked.return_value.activate.call_count == 1

    def test_LinuxApp__activate_workspace_returns_True(self, mocker):
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector.get_wnck_workspace_for_custom_number"
        )
        mocked.return_value = False
        app = App()
        returned = app._activate_workspace(1000)
        assert returned is True

    def test_LinuxApp__activate_workspace_returns_workspace(self, mocker):
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector.get_wnck_workspace_for_custom_number"
        )
        app = App()
        returned = app._activate_workspace(1000)
        assert returned == mocked.return_value

    ## LinuxApp._move_window_to_workspace
    def test_LinuxApp__move_window_to_workspace_calls_Wnck_shutdown(self, mocker):
        mocked_ws = mocker.patch("arrangeit.linux.app.App._activate_workspace")
        mocked_ws.return_value = False
        mocked = mocker.patch("arrangeit.linux.app.Wnck.shutdown")
        app = App()
        app._move_window_to_workspace(500, 1000)
        mocked.assert_called()

    def test_LinuxApp__move_window_to_workspace_calls_Wnck_Workspace_activate(
        self, mocker
    ):
        mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocked = mocker.patch("arrangeit.linux.app.App._activate_workspace")
        app = App()
        app._move_window_to_workspace(500, 1000)
        assert mocked.call_count == 1
        mocked.assert_called_with(1000)

    def test_LinuxApp__move_window_to_workspace_calls_get_window_by_wid(self, mocker):
        mocked = mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocker.patch("arrangeit.linux.app.App._activate_workspace")
        app = App()
        app._move_window_to_workspace(500, 1000)
        assert mocked.call_count == 1
        mocked.assert_called_with(500)

    def test_LinuxApp__move_window_to_workspace_calls_win_move_to_workspace(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocked_ws = mocker.patch("arrangeit.linux.app.App._activate_workspace")
        app = App()
        app._move_window_to_workspace(500, 1000)
        assert mocked.return_value.move_to_workspace.call_count == 1
        mocked.return_value.move_to_workspace.assert_called_with(mocked_ws.return_value)

    def test_LinuxApp__move_window_to_workspace_calls_win_activate(self, mocker):
        mocked = mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocker.patch("arrangeit.linux.app.App._activate_workspace")
        app = App()
        app._move_window_to_workspace(500, 1000)
        assert mocked.return_value.activate.call_count == 1
        mocked.return_value.activate.assert_called_with(X.CurrentTime)

    def test_LinuxApp__move_window_to_workspace_returns_False(self, mocker):
        mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocker.patch("arrangeit.linux.app.App._activate_workspace")
        app = App()
        returned = app._move_window_to_workspace(500, 1000)
        assert returned is False

    def test_LinuxApp__move_window_to_workspace_returns_True(self, mocker):
        mocker.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
        mocked = mocker.patch("arrangeit.linux.app.App._activate_workspace")
        mocked.return_value = False
        app = App()
        returned = app._move_window_to_workspace(500, 1000)
        assert returned is True

    ## LinuxApp.move_to_workspace
    def test_LinuxApp_activate_root_calls_get_window_stack(self, mocker):
        mocked = mocker.patch("arrangeit.linux.app.Gdk.Screen.get_default")
        App().activate_root(100)
        mocked.return_value.get_window_stack.assert_called_once()

    def test_LinuxApp_activate_root_calls_window_focus(self, mocker):
        mocked_screen = mocker.patch("arrangeit.linux.app.Gdk.Screen.get_default")
        SAMPLE = 100
        window = mocker.MagicMock()
        window.get_xid.return_value = SAMPLE + 1
        mocked_screen.return_value.get_window_stack.return_value = [window, ]
        App().activate_root(SAMPLE)
        window.focus.assert_called_once()
        window.focus.assert_called_with(X.CurrentTime)

    def test_LinuxApp_activate_root_not_calling_window_focus(self, mocker):
        mocked_screen = mocker.patch("arrangeit.linux.app.Gdk.Screen.get_default")
        SAMPLE = 100
        window = mocker.MagicMock()
        window.get_xid.return_value = 8000
        mocked_screen.return_value.get_window_stack.return_value = [window, ]
        App().activate_root(SAMPLE)
        window.focus.assert_not_called()


    ## LinuxApp.activate_root
    def test_LinuxApp_activate_root_calls__move_window_to_workspace(self, mocker):
        mocked = mocker.patch("arrangeit.linux.app.App._move_window_to_workspace")
        app = App()
        app.move_to_workspace(100, 1001)
        mocked.assert_called()
        mocked.assert_called_with(101, 1001)


class TestLinuxController(object):
    """Testing class for :py:class:`arrangeit.linux.controller.Controller` class."""

    ## Controller.setup_root_window
    def test_LinuxController_setup_root_window_calls_type_splash(self, mocker):
        root = mocker.patch("arrangeit.base.get_tkinter_root")
        mocker.patch("arrangeit.base.quarter_by_smaller", return_value=(100, 100))
        mocker.patch("arrangeit.base.ViewApplication")
        Controller(mocker.MagicMock()).setup_root_window(root)
        root.wm_attributes.assert_called()
        calls = [mocker.call("-type", "splash")]
        root.wm_attributes.assert_has_calls(calls, any_order=True)


class TestLinuxCollector(object):
    """Testing class for :py:class:`arrangeit.linux.collector.Collector` class."""

    ## Collector.is_applicable
    @pytest.mark.parametrize(
        "window_type,value",
        [
            (Wnck.WindowType.NORMAL, True),
            (Wnck.WindowType.DIALOG, True),
            (Wnck.WindowType.UTILITY, True),
            (Wnck.WindowType.DESKTOP, False),
            (Wnck.WindowType.DOCK, False),
            (Wnck.WindowType.TOOLBAR, False),
            (Wnck.WindowType.MENU, False),
            (Wnck.WindowType.SPLASHSCREEN, False),
        ],
    )
    def test_LinuxCollector_is_applicable(self, window_type, value):
        assert Collector().is_applicable(window_type) == value

    ## Collector.is_valid_state
    @pytest.mark.parametrize(
        "window_type,window_state,value",
        [
            (Wnck.WindowType.NORMAL, Wnck.WindowState.SKIP_TASKLIST, True),
            (Wnck.WindowType.DIALOG, Wnck.WindowState.SKIP_TASKLIST, False),
            (Wnck.WindowType.UTILITY, Wnck.WindowState.SKIP_TASKLIST, True),
            (Wnck.WindowType.NORMAL, Wnck.WindowState.SHADED, True),
            (Wnck.WindowType.NORMAL, Wnck.WindowState.FULLSCREEN, False),
            (
                Wnck.WindowType.NORMAL,
                Wnck.WindowState.HIDDEN | Wnck.WindowState.MINIMIZED,
                True,
            ),
            (Wnck.WindowType.NORMAL, Wnck.WindowState.HIDDEN, False),
            (Wnck.WindowType.NORMAL, Wnck.WindowState.DEMANDS_ATTENTION, True),
            (Wnck.WindowType.NORMAL, Wnck.WindowState.MAXIMIZED_HORIZONTALLY, True),
            (Wnck.WindowType.NORMAL, Wnck.WindowState.ABOVE, True),
            (Wnck.WindowType.NORMAL, Wnck.WindowState.BELOW, True),
        ],
    )
    def test_LinuxCollector_is_valid_state(self, window_type, window_state, value):
        assert Collector().is_valid_state(window_type, window_state) == value

    ## Collector.is_resizable
    @pytest.mark.parametrize(
        "window_type,value",
        [
            (Wnck.WindowType.NORMAL, True),
            (Wnck.WindowType.DIALOG, False),
            (Wnck.WindowType.UTILITY, False),
        ],
    )
    def test_LinuxCollector_is_resizable(self, window_type, value):
        assert Collector().is_resizable(window_type) == value

    ## LinuxCollector.get_windows
    @pytest.mark.parametrize("method", ["get_default", "force_update", "get_windows"])
    def test_LinuxCollector_get_windows_calls_Screen_methods(self, mocker, method):
        mocked = mocker.patch("arrangeit.linux.collector.Wnck.Screen.{}".format(method))
        Collector().get_windows()
        mocked.assert_called_once()

    ## LinuxCollector.check_window
    def test_LinuxCollector_check_window_calls_W_get_window_type(self, mocker):
        mocked = mocker.patch("arrangeit.linux.collector.Wnck.Window.get_window_type")
        Collector().check_window(Wnck.Window)
        mocked.assert_called_once()

    def test_LinuxCollector_check_window_calls_is_applicable(self, mocker):
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_window_type")
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_state")
        mocked = mocker.patch("arrangeit.linux.collector.Collector.is_applicable")
        Collector().check_window(Wnck.Window)
        mocked.assert_called_once()

    def test_LinuxCollector_check_window_calls_W_get_state(self, mocker):
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_window_type")
        mocker.patch(
            "arrangeit.linux.collector.Collector.is_applicable", return_Value=True
        )
        mocked = mocker.patch("arrangeit.linux.collector.Wnck.Window.get_state")
        Collector().check_window(Wnck.Window)
        mocked.assert_called_once()

    def test_LinuxCollector_check_window_calls_is_valid_state(self, mocker):
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_window_type")
        mocker.patch(
            "arrangeit.linux.collector.Collector.is_applicable", return_Value=True
        )
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_state")
        mocked = mocker.patch("arrangeit.linux.collector.Collector.is_valid_state")
        Collector().check_window(Wnck.Window)
        mocked.assert_called_once()

    def test_LinuxCollector_check_window_returns_False_for_not_is_app(self, mocker):
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_window_type")
        mocker.patch(
            "arrangeit.linux.collector.Collector.is_applicable", return_value=False
        )
        assert not Collector().check_window(Wnck.Window)

    def test_LinuxCollector_check_window_returns_False_for_invalid_state(self, mocker):
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_window_type")
        mocker.patch(
            "arrangeit.linux.collector.Collector.is_applicable", return_value=True
        )
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_state")
        mocker.patch(
            "arrangeit.linux.collector.Collector.is_valid_state", return_value=False
        )
        assert not Collector().check_window(Wnck.Window)

    def test_LinuxCollector_check_window_returns_True_for_both_True(self, mocker):
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_window_type")
        mocker.patch(
            "arrangeit.linux.collector.Collector.is_applicable", return_value=True
        )
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_state")
        mocker.patch(
            "arrangeit.linux.collector.Collector.is_valid_state", return_value=True
        )
        assert Collector().check_window(Wnck.Window)

    ## LinuxCollector.add_window
    def test_LinuxCollector_add_window_calls_WindowsCollection_add(self, mocker):
        mocker.patch("arrangeit.linux.collector.Collector.get_image_from_pixbuf")
        mocked = mocker.patch("arrangeit.data.WindowsCollection.add")
        Collector().add_window(mocker.MagicMock())
        mocked.assert_called_once()

    def test_LinuxCollector_add_window_inits_WindowModel(self, mocker):
        mocker.patch("arrangeit.linux.collector.Collector.get_image_from_pixbuf")
        mocker.patch("arrangeit.data.WindowsCollection.add")
        mocked = mocker.patch("arrangeit.linux.collector.WindowModel")
        Collector().add_window(mocker.MagicMock())
        mocked.assert_called_once()

    @pytest.mark.parametrize(
        "method",
        [
            "get_xid",
            "get_geometry",
            "get_window_type",
            "get_name",
            "get_class_group_name",
            "get_icon",
        ],
    )
    def test_LinuxCollector_add_window_calls_Wnck_Window_methods(self, mocker, method):
        mocker.patch("arrangeit.linux.collector.Collector.get_image_from_pixbuf")
        mocked_ww = mocker.patch("arrangeit.linux.collector.Wnck.Window")
        mocked = mocker.patch("arrangeit.linux.collector.Wnck.Window.{}".format(method))
        Collector().add_window(mocked_ww)
        mocked.assert_called_once()

    def test_LinuxCollector_rect_is_converted_to_tuple(self, mocker):
        mocker.patch("arrangeit.linux.collector.Collector.get_image_from_pixbuf")
        mocked_ww = mocker.patch("arrangeit.linux.collector.Wnck.Window")
        collector = Collector()
        collector.add_window(mocked_ww)
        assert isinstance(collector.collection._members[0].rect, tuple)

    def test_LinuxCollector_add_window_calls_is_resizable(self, mocker):
        mocker.patch("arrangeit.linux.collector.Collector.get_image_from_pixbuf")
        mocked = mocker.patch("arrangeit.linux.collector.Collector.is_resizable")
        Collector().add_window(mocker.MagicMock())
        mocked.assert_called_once()

    def test_LinuxCollector_add_window_calls_get_image_from_pixbuf(self, mocker):
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector.get_image_from_pixbuf"
        )
        Collector().add_window(mocker.MagicMock())
        mocked.assert_called_once()

    def test_LinuxCollector_add_window_calls_get_workspace_number_for_window(
        self, mocker
    ):
        mocker.patch("arrangeit.linux.collector.Collector.get_image_from_pixbuf")
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector.get_workspace_number_for_window"
        )
        Collector().add_window(mocker.MagicMock())
        mocked.assert_called_once()

    ## LinuxCollector.run
    def test_LinuxCollector_run_super(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseCollector.run")
        Collector().run()
        mocked.assert_called()

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
    def test_LinuxCollector_run_functionality(
        self, mocker, is_applicable, is_valid_state, value
    ):
        mocker.patch("arrangeit.linux.collector.Collector.get_image_from_pixbuf")
        mocker.patch(
            "arrangeit.linux.collector.Collector.get_windows",
            return_value=(mocker.MagicMock(), mocker.MagicMock()),
        )
        mocker.patch(
            "arrangeit.linux.collector.Collector.is_applicable",
            side_effect=is_applicable,
        )
        mocker.patch(
            "arrangeit.linux.collector.Collector.is_valid_state",
            side_effect=is_valid_state,
        )
        mocker.patch("arrangeit.data.WindowsCollection.sort")
        collector = Collector()
        collector.run()
        assert collector.collection.size == value

    ## LinuxCollector.get_image_from_pixbuf
    def test_LinuxCollector_get_image_from_pixbuf_returns_valid_type(self):
        collector = Collector()
        image = GdkPixbuf.Pixbuf.new_from_file(
            os.path.join(os.path.dirname(arrangeit.__file__), "resources", "blank.png")
        )
        assert isinstance(collector.get_image_from_pixbuf(image), Image.Image)

    ## LinuxCollector.get_workspace_number_for_window
    def test_LinuxCollector_get_workspace_number_for_window_calls_W_get_workspace(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.linux.collector.Wnck.Window.get_workspace")
        Collector().get_workspace_number_for_window(Wnck.Window)
        mocked.assert_called_once()

    def test_LinuxCollector_get_workspace_number_for_window_calls_wn_for_window(
        self, mocker
    ):
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_workspace")
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector.get_workspace_number"
        )
        Collector().get_workspace_number_for_window(Wnck.Window)
        mocked.assert_called_once()

    ## LinuxCollector.get_workspace_number
    def test_LinuxCollector_get_workspace_number_returns_0(self, mocker):
        assert Collector().get_workspace_number(None) == 0

    @pytest.mark.parametrize(
        "screen,workspace,expected",
        [(0, 0, 0), (0, 1, 1), (0, 9, 9), (1, 0, 1000), (1, 12, 1012), (5, 4, 5004)],
    )
    def test_LinuxCollector_get_workspace_number_returns_correct_number(
        self, mocker, screen, workspace, expected
    ):
        ws = mocker.MagicMock()
        ws.get_screen.return_value.get_number.return_value = screen
        ws.get_number.return_value = workspace

        returned = Collector().get_workspace_number(ws)
        ws.get_screen.assert_called_once()
        ws.get_screen.return_value.get_number.assert_called_once()
        ws.get_number.assert_called_once()

        assert returned == expected

    ## LinuxCollector._get_available_wnck_workspaces
    @pytest.mark.parametrize(
        "method", ["get_default", "force_update", "get_workspaces"]
    )
    def test_LinuxCollector__get_available_wnck_workspaces_calls_Screen_methods(
        self, mocker, method
    ):
        mocked = mocker.patch("arrangeit.linux.collector.Wnck.Screen.{}".format(method))
        Collector()._get_available_wnck_workspaces()
        mocked.assert_called_once()

    def test_LinuxCollector__get_available_wnck_workspaces_returns_list(self, mocker):
        workspaces = Collector()._get_available_wnck_workspaces()
        assert isinstance(workspaces, list)
        if len(workspaces):
            assert isinstance(workspaces[0], Wnck.Workspace)

    ## LinuxCollector.get_available_workspaces
    def test_LinuxCollector_get_available_workspaces_calls__get_available_wnck(
        self, mocker
    ):
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector._get_available_wnck_workspaces"
        )
        Collector().get_available_workspaces()
        mocked.assert_called_once()

    def test_LinuxCollector_get_available_workspaces_returns_list(self, mocker):
        mocker.patch(
            "arrangeit.linux.collector.Wnck.Screen.get_workspaces", return_value=[]
        )
        assert isinstance(Collector().get_available_workspaces(), list)

    def test_LinuxCollector_get_available_workspaces_returns_one_element(self, mocker):
        mocker.patch(
            "arrangeit.linux.collector.Wnck.Screen.get_workspaces", return_value=[]
        )
        returned = Collector().get_available_workspaces()
        assert len(returned) == 1
        assert returned == [(0, "")]

    def test_LinuxCollector_get_available_workspaces_calls_get_workspace_number(
        self, mocker
    ):
        ws1, ws2 = mocker.MagicMock(), mocker.MagicMock()
        mocker.patch(
            "arrangeit.linux.collector.Wnck.Screen.get_workspaces",
            return_value=(ws1, ws2),
        )
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector.get_workspace_number"
        )
        Collector().get_available_workspaces()
        calls = [mocker.call(ws1), mocker.call(ws2)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_LinuxCollector_get_available_workspaces_calls_W_workspace_get_name(
        self, mocker
    ):
        ws1, ws2 = mocker.MagicMock(), mocker.MagicMock()
        mocker.patch(
            "arrangeit.linux.collector.Wnck.Screen.get_workspaces",
            return_value=(ws1, ws2),
        )
        Collector().get_available_workspaces()
        assert ws1.get_name.call_count == 1
        assert ws2.get_name.call_count == 1

    def test_LinuxCollector_get_available_workspaces_functionality(self, mocker):
        ws1, ws2 = mocker.MagicMock(), mocker.MagicMock()
        mocker.patch(
            "arrangeit.linux.collector.Wnck.Screen.get_workspaces",
            return_value=(ws1, ws2),
        )
        mocker.patch(
            "arrangeit.linux.collector.Collector.get_workspace_number",
            return_value=1002,
        )
        ws1.get_name.return_value = "foo"
        ws2.get_name.return_value = "bar"
        returned = Collector().get_available_workspaces()
        assert returned == [(1002, "foo"), (1002, "bar")]

    ## LinuxCollector.get_wnck_workspace_for_custom_number
    def test_LinuxCollector_get_wnck_workspace_for_custom_number_calls__get_available(
        self, mocker
    ):
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector._get_available_wnck_workspaces"
        )
        Collector().get_wnck_workspace_for_custom_number(0)
        mocked.assert_called_once()

    def test_LinuxCollector_get_wnck_workspace_for_custom_number_calls_get_w_number(
        self, mocker
    ):
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector.get_workspace_number"
        )
        Collector().get_wnck_workspace_for_custom_number(0)
        mocked.assert_called()

    ## LinuxCollector.get_window_by_wid
    def test_LinuxCollector_get_window_by_wid_calls_Wnck_Window_get(self, mocker):
        mocked = mocker.patch("arrangeit.linux.collector.Wnck.Window")
        collector = Collector()
        collector.get_window_by_wid(100)
        assert mocked.get.call_count == 1

    ## LinuxCollector._check_mask_part
    @pytest.mark.parametrize(
        "rect,changed,expected",
        [
            ((100, 200, 300, 400), (100, 200, 300, 400), False),
            ((100, 200, 300, 400), (101, 200, 300, 400), MOVE_RESIZE_MASKS["x"]),
            ((100, 200, 300, 400), (100, 201, 300, 400), MOVE_RESIZE_MASKS["y"]),
            ((100, 200, 300, 400), (100, 200, 301, 400), MOVE_RESIZE_MASKS["w"]),
            ((100, 200, 300, 400), (100, 200, 300, 401), MOVE_RESIZE_MASKS["h"]),
            (
                (100, 200, 300, 400),
                (101, 201, 300, 400),
                MOVE_RESIZE_MASKS["x"] | MOVE_RESIZE_MASKS["y"],
            ),
            (
                (100, 200, 300, 400),
                (101, 201, 301, 400),
                MOVE_RESIZE_MASKS["x"]
                | MOVE_RESIZE_MASKS["y"]
                | MOVE_RESIZE_MASKS["w"],
            ),
            (
                (100, 200, 300, 400),
                (101, 201, 301, 401),
                MOVE_RESIZE_MASKS["x"]
                | MOVE_RESIZE_MASKS["y"]
                | MOVE_RESIZE_MASKS["w"]
                | MOVE_RESIZE_MASKS["h"],
            ),
        ],
    )
    def test_LinuxCollector__check_mask_part_functionality(
        self, mocker, rect, changed, expected
    ):
        collector = Collector()
        model = WindowModel(rect=rect)
        model.set_changed(rect=changed)
        returned = collector._check_mask_part(model, list(MOVE_RESIZE_MASKS.keys()))
        assert returned == expected

    ## LinuxCollector.get_window_move_resize_mask
    def test_LinuxCollector_get_window_move_resize_mask_calls__check_mask_part(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.linux.collector.Collector._check_mask_part")
        collector = Collector()
        model = mocker.MagicMock()
        collector.get_window_move_resize_mask(model)
        assert mocked.call_count == 1
        mocked.assert_called_with(model, list(MOVE_RESIZE_MASKS.keys()))

    ## LinuxCollector.get_monitors_rects
    def test_LinuxCollector_get_monitors_rects_calls_GDK_display_get_default(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.linux.collector.Gdk.Display.get_default")
        collector = Collector()
        collector.get_monitors_rects()
        mocked.assert_called_once()

    def test_LinuxCollector_get_monitors_rects_calls_GDK_display_get_n_monitors(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.linux.collector.Gdk.Display.get_n_monitors")
        collector = Collector()
        collector.get_monitors_rects()
        mocked.assert_called_once()

    def test_LinuxCollector_get_monitors_rects_calls_GDK_display_get_monitor(
        self, mocker
    ):
        mocker.patch(
            "arrangeit.linux.collector.Gdk.Display.get_n_monitors", return_value=1
        )
        mocked = mocker.patch("arrangeit.linux.collector.Gdk.Display.get_monitor")
        collector = Collector()
        collector.get_monitors_rects()
        mocked.assert_called_once()
        mocked.assert_called_with(0)

    def test_LinuxCollector_get_monitors_rects_calls_GDK_monitor_get_workarea(
        self, mocker
    ):
        mocker.patch(
            "arrangeit.linux.collector.Gdk.Display.get_n_monitors", return_value=1
        )
        mocked = mocker.patch("arrangeit.linux.collector.Gdk.Display.get_monitor")
        collector = Collector()
        collector.get_monitors_rects()
        mocked.return_value.get_workarea.assert_called_once()

    def test_LinuxCollector_get_monitors_rects_returns_list_of_rects(self, mocker):
        mocker.patch(
            "arrangeit.linux.collector.Gdk.Display.get_n_monitors", return_value=1
        )
        mocked = mocker.patch("arrangeit.linux.collector.Gdk.Display.get_monitor")
        type(mocked.return_value.get_workarea.return_value).x = mocker.PropertyMock(return_value=10)
        type(mocked.return_value.get_workarea.return_value).y = mocker.PropertyMock(return_value=20)
        type(mocked.return_value.get_workarea.return_value).width = mocker.PropertyMock(return_value=100)
        type(mocked.return_value.get_workarea.return_value).height = mocker.PropertyMock(return_value=200)
        collector = Collector()
        rects = collector.get_monitors_rects()
        assert isinstance(rects, list)
        assert rects == [(10, 20, 100, 200)]





    ## LinuxCollector.get_smallest_monitor_size
    def test_LinuxCollector_get_smallest_monitor_size_calls_GDK_display_get_default(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.linux.collector.Gdk.Display.get_default")
        collector = Collector()
        collector.get_smallest_monitor_size()
        mocked.assert_called_once()

    def test_LinuxCollector_get_smallest_monitor_size_calls_GDK_display_get_n_monitors(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.linux.collector.Gdk.Display.get_n_monitors")
        collector = Collector()
        collector.get_smallest_monitor_size()
        mocked.assert_called_once()

    def test_LinuxCollector_get_smallest_monitor_size_calls_GDK_display_get_monitor(
        self, mocker
    ):
        mocker.patch(
            "arrangeit.linux.collector.Gdk.Display.get_n_monitors", return_value=1
        )
        mocked = mocker.patch("arrangeit.linux.collector.Gdk.Display.get_monitor")
        collector = Collector()
        collector.get_smallest_monitor_size()
        mocked.assert_called_once()
        mocked.assert_called_with(0)

    def test_LinuxCollector_get_smallest_monitor_size_calls_GDK_monitor_get_workarea(
        self, mocker
    ):
        mocker.patch(
            "arrangeit.linux.collector.Gdk.Display.get_n_monitors", return_value=1
        )
        mocked = mocker.patch("arrangeit.linux.collector.Gdk.Display.get_monitor")
        collector = Collector()
        collector.get_smallest_monitor_size()
        mocked.return_value.get_workarea.assert_called_once()

    def test_LinuxCollector_get_smallest_monitor_size_returns_tuple(
        self, mocker
    ):
        mocker.patch(
            "arrangeit.linux.collector.Gdk.Display.get_n_monitors", return_value=1
        )
        mocked = mocker.patch("arrangeit.linux.collector.Gdk.Display.get_monitor")
        WIDTH, HEIGHT = 800, 600
        rect = mocker.MagicMock()
        rect.width = WIDTH
        rect.height = HEIGHT
        mocked.return_value.get_workarea.return_value = rect
        collector = Collector()
        returned = collector.get_smallest_monitor_size()
        assert returned == (WIDTH, HEIGHT)