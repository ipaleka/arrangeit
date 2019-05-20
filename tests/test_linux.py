import pytest
import gi

gi.require_version("Wnck", "3.0")
from gi.repository import Wnck

from arrangeit.linux.controller import Controller
from arrangeit.linux.collector import Collector


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
        mocked = mocker.patch("arrangeit.data.WindowsCollection.add")
        Collector().add_window(mocker.MagicMock())
        mocked.assert_called_once()

    def test_LinuxCollector_add_window_inits_WindowModel(self, mocker):
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
        ],
    )
    def test_LinuxCollector_add_window_calls_Wnck_Window_methods(self, mocker, method):
        mocked_ww = mocker.patch("arrangeit.linux.collector.Wnck.Window")
        mocked = mocker.patch("arrangeit.linux.collector.Wnck.Window.{}".format(method))
        Collector().add_window(mocked_ww)
        mocked.assert_called_once()

    def test_LinuxCollector_add_window_calls_is_resizable(self, mocker):
        mocked = mocker.patch("arrangeit.linux.collector.Collector.is_resizable")
        Collector().add_window(mocker.MagicMock())
        mocked.assert_called_once()

    ## LinuxCollector.run
    def test_LinuxCollector_run_super(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseCollector.run")
        Collector().run()
        mocked.assert_called()

    def test_LinuxCollector_run_shutdowns_Wnck(self, mocker):
        mocker.patch(
            "arrangeit.linux.collector.Collector.get_windows",
            return_value=(mocker.MagicMock(),),
        )
        mocked = mocker.patch("arrangeit.linux.collector.Wnck.shutdown")
        Collector().run()
        mocked.assert_called_once()

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
