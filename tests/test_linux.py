import os

import asynctest
import gi

gi.require_version("Wnck", "3.0")
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Wnck, GdkPixbuf
from PIL import Image
from Xlib import X
import pytest

import arrangeit
from arrangeit.data import WindowModel
from arrangeit.linux.app import App
from arrangeit.linux.collector import Collector
from arrangeit.linux.controller import Controller


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
        mocker.patch("arrangeit.linux.collector.Collector._get_tk_image_from_pixbuf")
        mocked = mocker.patch("arrangeit.data.WindowsCollection.add")
        Collector().add_window(mocker.MagicMock())
        mocked.assert_called_once()

    def test_LinuxCollector_add_window_inits_WindowModel(self, mocker):
        mocker.patch("arrangeit.linux.collector.Collector._get_tk_image_from_pixbuf")
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
        mocker.patch("arrangeit.linux.collector.Collector._get_tk_image_from_pixbuf")
        mocked_ww = mocker.patch("arrangeit.linux.collector.Wnck.Window")
        mocked = mocker.patch("arrangeit.linux.collector.Wnck.Window.{}".format(method))
        Collector().add_window(mocked_ww)
        mocked.assert_called_once()

    def test_LinuxCollector_add_window_calls_is_resizable(self, mocker):
        mocker.patch("arrangeit.linux.collector.Collector._get_tk_image_from_pixbuf")
        mocked = mocker.patch("arrangeit.linux.collector.Collector.is_resizable")
        Collector().add_window(mocker.MagicMock())
        mocked.assert_called_once()

    def test_LinuxCollector_add_window_calls__get_tk_image_from_pixbuf(self, mocker):
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector._get_tk_image_from_pixbuf"
        )
        Collector().add_window(mocker.MagicMock())
        mocked.assert_called_once()

    def test_LinuxCollector_add_window_calls_get_workspace_number_for_window(
        self, mocker
    ):
        mocker.patch("arrangeit.linux.collector.Collector._get_tk_image_from_pixbuf")
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
        mocker.patch("arrangeit.linux.collector.Collector._get_tk_image_from_pixbuf")
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
        collector = Collector()
        collector.run()
        assert collector.collection.size == value

    ## LinuxCollector._get_tk_image_from_pixbuf
    def test_LinuxCollector__get_tk_image_from_pixbuf_returns_valid_type(self):
        collector = Collector()
        image = GdkPixbuf.Pixbuf.new_from_file(
            os.path.join(os.path.dirname(arrangeit.__file__), "resources", "blank.png")
        )
        assert isinstance(collector._get_tk_image_from_pixbuf(image), Image.Image)

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

    def test_LinuxCollector__get_available_wnck_workspaces_returns_list(
        self, mocker 
    ):
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

    ## LinuxCollector._get_wnck_workspace_for_custom_number
    def test_LinuxCollector__get_wnck_workspace_for_custom_number_calls__get_available(self, mocker):
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector._get_available_wnck_workspaces"
        )
        Collector().activate_workspace(0)
        mocked.assert_called_once()

    ## LinuxCollector.activate_workspace
    def test_LinuxCollector_activate_workspace_calls__get_wnck_workspace_for_custom(self, mocker):
        mocked = mocker.patch(
            "arrangeit.linux.collector.Collector._get_wnck_workspace_for_custom_number"
        )
        Collector().activate_workspace(0)
        mocked.assert_called_once()

    def test_LinuxCollector_activate_workspace_calls_Wnck_Workspace_activate(
        self, mocker
    ):
        mocked = mocker.MagicMock()
        mocker.patch(
            "arrangeit.linux.collector.Collector.get_workspace_number", return_value=0
        )
        mocker.patch(
            "arrangeit.linux.collector.Collector._get_available_wnck_workspaces",
            return_value=[mocked],
        )
        Collector().activate_workspace(0)
        assert mocked.activate.call_count == 1
        calls = [mocker.call(X.CurrentTime)]
        mocked.activate.assert_has_calls(calls, any_order=True)


@pytest.mark.asyncio
class TestAsyncLinuxCollector(object):
    """Testing class for :py:class:`arrangeit.linux.Collector` async methods."""

    ## LinuxCollector.get_window_by_wid
    async def test_LinuxCollector_get_window_by_wid_calls_Wnck_Window_get(self, mocker):
        mocked = mocker.patch("arrangeit.linux.collector.Wnck.Window")
        collector = Collector()
        await collector.get_window_by_wid(100)
        assert mocked.get.call_count == 1

    ## LinuxCollector.get_window_move_resize_mask
    async def test_LinuxCollector_get_window_move_resize_mask_all(self):
        collector = Collector()
        returned = await collector.get_window_move_resize_mask(WindowModel())
        assert returned == (
            Wnck.WindowMoveResizeMask.X
            | Wnck.WindowMoveResizeMask.Y
            | Wnck.WindowMoveResizeMask.WIDTH
            | Wnck.WindowMoveResizeMask.HEIGHT
        )


class TestAsyncLinuxApp(asynctest.TestCase):

    ## LinuxApp.move_and_resize
    @asynctest.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
    async def test_LinuxApp_move_and_resize_calls_get_model_by_wid(self, mocked):
        app = App()
        with self.assertRaises(AttributeError):
            await app.move_and_resize(100)
        mocked.assert_called()

    @asynctest.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
    async def test_LinuxApp_move_and_resize_calls_get_window_by_wid(self, mocked):
        app = App()
        with self.assertRaises(AttributeError):
            await app.move_and_resize(100)
        mocked.assert_called()

    @asynctest.patch("arrangeit.linux.collector.Collector.get_window_move_resize_mask")
    async def test_LinuxApp_move_and_resize_c_get_window_move_resize_mask(self, mocked):
        app = App()
        with self.assertRaises(AttributeError):
            await app.move_and_resize(100)
        mocked.assert_called()

    @asynctest.patch("arrangeit.base.WindowsCollection.get_model_by_wid")
    @asynctest.patch("arrangeit.linux.collector.Collector.get_window_by_wid")
    async def test_LinuxApp_move_and_resize_calls_WnckWindow_set_geometry(
        self, mocked_win, mocked_model
    ):
        app = App()
        mocked_win.return_value.set_geometry.return_value = 200
        returned = await app.move_and_resize(100)
        self.assertEqual(returned, 200)

    ## LinuxApp.move
    @asynctest.patch("arrangeit.linux.app.App.move_and_resize")
    async def test_LinuxApp_move_calls_move_and_resize(self, mocked):
        app = App()
        await app.move(100)
        mocked.assert_called()
        mocked.assert_called_with(100)
