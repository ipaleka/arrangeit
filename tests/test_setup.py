import pytest

from arrangeit import main, base
from arrangeit import utils
from arrangeit.utils import get_app, get_collector, get_player


class TestStructure(object):
    """Testing class for platform specific subpackages structure."""

    ## BaseApp
    def test_host_platform_App_issubclass_of_BaseApp(self):
        assert issubclass(get_app(), base.BaseApp)

    ## BaseCollector
    def test_host_platform_Collector_issubclass_of_BaseCollector(self):
        assert issubclass(get_collector(), base.BaseCollector)

    ## BasePlayer
    def test_host_platform_Player_issubclass_of_BasePlayer(self):
        assert issubclass(get_player(), base.BasePlayer)


class TestSetup(object):
    """Testing class for main app initialization and configuration."""

    ## main
    def test_main_calls_get_app(self, mocker):
        mocked = mocker.patch("arrangeit.main.get_app")
        main.main()
        mocked.assert_called_once()

    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_main_initializes_platform_specific_App(self, mocker, platform):
        mocker.patch("arrangeit.utils.platform_path", return_value=platform)
        mocked = mocker.patch("arrangeit.{}.app.App".format(platform))
        main.main()
        mocked.assert_called()

    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_main_calls_App_run(self, mocker, platform):
        mocker.patch("arrangeit.utils.platform_path", return_value=platform)
        mocker.patch("arrangeit.utils.get_app", return_value=utils.get_app(platform))
        mocked = mocker.patch("arrangeit.{}.app.App.run".format(platform))
        main.main()
        mocked.assert_called()
