import pytest
from importlib import import_module

from arrangeit import app


class TestSetup(object):
    """App initialization and configuration pytest class"""

    def get_collector(self, platform):
        """Helper method for retrieving platform specific Collector class"""
        collector = import_module("arrangeit.{}.collector".format(platform))
        return collector.Collector

    def test_main_initializes_App(self, mocker):
        mocker.patch("arrangeit.app.App")
        app.main()
        app.App.assert_called_once()

    def test_main_calls_App_setup(self, mocker):
        mocker.patch("arrangeit.app.App.setup")
        app.main()
        app.App.setup.assert_called_once()

    def test_App_inits_collector_as_None(self):
        assert app.App.collector is None

    def test_app_initialization_calls_setup_collector(self, mocker):
        mocker.patch("arrangeit.app.App.setup_collector")
        app.App()
        app.App.setup_collector.assert_called_once()

    def test_app_setup_collector_calls_platform_path(self, mocker):
        with mocker.patch.object(
            app.App, "platform_path", return_value="windows"
        ) as mock_method:
            app.App().setup_collector()
            app.App.platform_path.assert_called()

    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_setup_calls_app_collector(self, mocker, platform):
        mocker.patch.object(app.App, "platform_path", return_value=platform)
        mocker.patch.object(
            app.App, "collector", return_value=self.get_collector(platform)
        )
        mocker.patch("arrangeit.{}.collector.Collector.__call__".format(platform))
        app.App().setup()
        self.get_collector(platform).__call__.assert_called()
