import pytest

from arrangeit import __main__, base
from arrangeit import utils
from arrangeit.utils import get_component_class


class TestStructure(object):
    """Testing class for platform specific subpackages structure."""

    ## BaseApp
    def test_host_platform_App_issubclass_of_BaseApp(self):
        assert issubclass(get_component_class("App"), base.BaseApp)

    ## BaseController
    def test_host_platform_Controller_issubclass_of_BaseController(self):
        assert issubclass(get_component_class("Controller"), base.BaseController)

    ## BaseCollector
    def test_host_platform_Collector_issubclass_of_BaseCollector(self):
        assert issubclass(get_component_class("Collector"), base.BaseCollector)


class TestSetup(object):
    """Testing class for main app initialization and configuration."""

    ## main
    def test_main_calls_get_component_class_App(self, mocker):
        mocked = mocker.patch("arrangeit.__main__.get_component_class")
        __main__.main()
        mocked.assert_called_once()
        mocked.assert_called_with("App")

    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_main_initializes_platform_specific_App(self, mocker, platform):
        mocker.patch("arrangeit.utils.platform_path", return_value=platform)
        mocked = mocker.patch("arrangeit.{}.app.App".format(platform))
        __main__.main()
        mocked.assert_called()

    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_main_calls_App_run(self, mocker, platform):
        mocker.patch("arrangeit.utils.platform_path", return_value=platform)
        mocked = mocker.patch("arrangeit.{}.app.App".format(platform))
        __main__.main()
        assert mocked.return_value.run.call_count == 1
