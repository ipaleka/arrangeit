import pytest

import arrangeit
from arrangeit import main, base
from arrangeit import utils
from arrangeit.utils import get_app, get_collector, get_player


class TestStructure(object):
    """Testing class for platform specific subpackages structure."""

    ## BaseApp
    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_platform_App_issubclass_of_BaseApp(self, platform):
        assert issubclass(get_app(platform), base.BaseApp)

    ## BaseCollector
    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_platform_Collector_issubclass_of_BaseCollector(self, platform):
        assert issubclass(get_collector(platform), base.BaseCollector)

    ## BasePlayer
    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_platform_Player_issubclass_of_BasePlayer(self, platform):
        assert issubclass(get_player(platform), base.BasePlayer)


class TestSetup(object):
    """Testing class for main app initialization and configuration."""

    ## main
    def test_main_calls_get_app(self, mocker):
        mocker.patch("arrangeit.main.get_app")
        main.main()
        main.get_app.assert_called_once()

    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_main_initializes_platform_specific_App(self, mocker, platform):
        mocker.patch("arrangeit.utils.platform_path", return_value=platform)
        # mocker.patch("arrangeit.main.get_app", return_value=utils.get_app(platform))
        mocker.patch("arrangeit.{}.app.App".format(platform))
        main.main()
        getattr(arrangeit, platform).app.App.assert_called()

    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_main_calls_App_run(self, mocker, platform):
        mocker.patch("arrangeit.utils.platform_path", return_value=platform)
        mocker.patch("arrangeit.utils.get_app", return_value=utils.get_app(platform))
        mocker.patch("arrangeit.{}.app.App.run".format(platform))
        main.main()
        getattr(arrangeit, platform).app.App.run.assert_called()
