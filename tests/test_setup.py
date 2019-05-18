import pytest

from arrangeit import main, base
from arrangeit import utils
from arrangeit.utils import get_component_class


class TestStructure(object):
    """Testing class for platform specific subpackages structure."""

    ## BaseApp
    def test_host_platform_App_issubclass_of_BaseApp(self):
        assert issubclass(get_component_class("App"), base.BaseApp)

    ## BaseGui
    def test_host_platform_Gui_issubclass_of_BaseGui(self):
        assert issubclass(get_component_class("Gui"), base.BaseGui)

    ## BaseCollector
    def test_host_platform_Collector_issubclass_of_BaseCollector(self):
        assert issubclass(get_component_class("Collector"), base.BaseCollector)

    ## BasePlayer
    def test_host_platform_Player_issubclass_of_BasePlayer(self):
        assert issubclass(get_component_class("Player"), base.BasePlayer)


class TestSetup(object):
    """Testing class for main app initialization and configuration."""

    ## main
    def test_main_calls_get_component_class_App(self, mocker):
        mocked = mocker.patch("arrangeit.main.get_component_class")
        main.main()
        mocked.assert_called_once()
        mocked.assert_called_with("App")

    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_main_initializes_platform_specific_App(self, mocker, platform):
        mocker.patch("arrangeit.utils.platform_path", return_value=platform)
        mocked = mocker.patch("arrangeit.{}.app.App".format(platform))
        main.main()
        mocked.assert_called()

    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_main_calls_App_run(self, mocker, platform):
        mocker.patch("arrangeit.utils.platform_path", return_value=platform)
        mocked = mocker.patch("arrangeit.{}.app.App".format(platform))
        main.main()
        assert mocked.return_value.run.call_count == 1
