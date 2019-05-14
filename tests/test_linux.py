import platform

import pytest
import gi

gi.require_version("Wnck", "3.0")
from gi.repository import Wnck

from arrangeit.linux.collector import Collector


@pytest.mark.skipif(platform.system() != "Linux", reason="GNU/Linux only tests")
class TestLinuxCollector(object):
    """Testing class for :py:class:`arrangeit.linux.collector.Collector` class."""

    ## Collector.applicable
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
    def test_LinuxCollector_applicable(self, window_type, value):
        assert Collector().applicable(window_type) == value

    ## Collector.valid_state
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
    def test_LinuxCollector_valid_state(self, window_type, window_state, value):
        assert Collector().valid_state(window_type, window_state) == value

    ## Collector.resizable
    @pytest.mark.parametrize(
        "window_type,value",
        [
            (Wnck.WindowType.NORMAL, True),
            (Wnck.WindowType.DIALOG, False),
            (Wnck.WindowType.UTILITY, False),
        ],
    )
    def test_LinuxCollector_resizable(self, window_type, value):
        assert Collector().resizable(window_type) == value

    ## LinuxCollector.get_windows
    @pytest.mark.parametrize(
        "method", ["get_default", "force_update", "get_windows"],
    )
    def test_LinuxCollector_get_windows_calls_Screen_methods(self, mocker, method):
        mocker.patch("arrangeit.linux.collector.Wnck.Screen.{}".format(method))
        Collector().get_windows()
        getattr(Wnck.Screen, method).assert_called_once()

    @pytest.mark.parametrize(
        "applicable,valid_state,value",
        [
            ((True, True), (True, True), 2),
            ((True, True), (True, False), 1),
            ((False, True), (True, True), 1),
            ((True, False), (False, True), 0),
            ((False, False), (False, False), 0),
        ],
    )
    def test_LinuxCollector___call__(self, mocker, applicable, valid_state, value):
        mocker.patch(
            "arrangeit.linux.collector.Collector.get_windows",
            return_value=(mocker.MagicMock(), mocker.MagicMock()),
        )
        mocker.patch(
            "arrangeit.linux.collector.Collector.applicable", side_effect=applicable
        )
        mocker.patch(
            "arrangeit.linux.collector.Collector.valid_state", side_effect=valid_state
        )
        collector = Collector()
        collector()
        assert collector.collection.size == value

