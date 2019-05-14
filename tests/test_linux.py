import platform

import pytest
import gi

gi.require_version("Wnck", "3.0")
from gi.repository import Wnck

from arrangeit.linux.collector import Collector


@pytest.mark.skipif(platform.system() != "Linux", reason="GNU/Linux only tests")
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
        mocker.patch("arrangeit.linux.collector.Wnck.Screen.{}".format(method))
        Collector().get_windows()
        getattr(Wnck.Screen, method).assert_called_once()

    ## LinuxCollector.check_window
    def test_LinuxCollector_check_window_calls_W_get_window_type(self, mocker):
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_window_type")
        Collector().check_window(Wnck.Window)
        Wnck.Window.get_window_type.assert_called_once()

    def test_LinuxCollector_check_window_calls_is_applicable(self, mocker):
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_window_type")
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_state")
        mocker.patch("arrangeit.linux.collector.Collector.is_applicable")
        Collector().check_window(Wnck.Window)
        Collector.is_applicable.assert_called_once()

    def test_LinuxCollector_check_window_calls_W_get_state(self, mocker):
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_window_type")
        mocker.patch(
            "arrangeit.linux.collector.Collector.is_applicable", return_Value=True
        )
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_state")
        Collector().check_window(Wnck.Window)
        Wnck.Window.get_state.assert_called_once()

    def test_LinuxCollector_check_window_calls_is_valid_state(self, mocker):
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_window_type")
        mocker.patch(
            "arrangeit.linux.collector.Collector.is_applicable", return_Value=True
        )
        mocker.patch("arrangeit.linux.collector.Wnck.Window.get_state")
        mocker.patch("arrangeit.linux.collector.Collector.is_valid_state")
        Collector().check_window(Wnck.Window)
        Collector.is_valid_state.assert_called_once()

    def test_LinuxCollector_check_window_returns_False_for_not_is_applic(self, mocker):
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

    ## LinuxCollector.__call__
    def test_LinuxCollector__call___calls_is_resizable(self, mocker):
        mocker.patch(
            "arrangeit.linux.collector.Collector.get_windows",
            return_value=(mocker.MagicMock(),),
        )
        mocker.patch(
            "arrangeit.linux.collector.Collector.is_applicable", side_effect=(True,)
        )
        mocker.patch(
            "arrangeit.linux.collector.Collector.is_valid_state", side_effect=(True,)
        )
        mocker.patch("arrangeit.linux.collector.Collector.is_resizable")
        Collector()()
        Collector.is_resizable.assert_called_once()

    # TODo: check calls for Wnck.Window methods, collection.add and WindowModel.__init__

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
    def test_LinuxCollector___call__(
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
        collector()
        assert collector.collection.size == value

