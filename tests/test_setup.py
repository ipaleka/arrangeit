import pytest

from arrangeit import app, base
from arrangeit import utils
from arrangeit.utils import get_collector, get_player


class TestStructure(object):
    """Classes structure testing class"""

    ## BaseCollector
    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_platform_Collector_issubclass_of_BaseCollector(self, platform):
        assert issubclass(get_collector(platform), base.BaseCollector)

    ## BasePlayer
    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_platform_Player_issubclass_of_BasePlayer(self, platform):
        assert issubclass(get_player(platform), base.BasePlayer)


class TestSetup(object):
    """App initialization and configuration testing class"""

    ## main
    def test_main_initializes_App(self, mocker):
        mocker.patch("arrangeit.app.App")
        app.main()
        app.App.assert_called_once()

    def test_main_calls_App_setup(self, mocker):
        mocker.patch("arrangeit.app.App.setup")
        app.main()
        app.App.setup.assert_called_once()

    ## App
    def test_App_inits_collector_as_None(self):
        assert app.App.player is None

    def test_App_inits_player_as_None(self):
        assert app.App.collector is None

    ## App.__init__.collector

    def test_app_initialization_calls_setup_collector(self, mocker):
        mocker.patch("arrangeit.app.App.setup_collector")
        app.App()
        app.App.setup_collector.assert_called_once()

    def test_app_initialization_instantiate_collector(self, mocker):
        collector = app.App().collector
        assert isinstance(collector, base.BaseCollector)

    ## App.__init__.player
    def test_app_initialization_calls_setup_player(self, mocker):
        mocker.patch("arrangeit.app.App.setup_player")
        app.App()
        app.App.setup_player.assert_called_once()

    def test_app_initialization_instantiate_player(self, mocker):
        player = app.App().player
        assert isinstance(player, base.BasePlayer)

    ## App.setup_collector
    def test_app_setup_collector_calls_get_collector(self, mocker):
        mocker.patch("arrangeit.utils.get_collector")
        app.App().setup_collector()
        utils.get_collector.assert_called()

    ## App.setup_player
    def test_app_setup_player_calls_get_player(self, mocker):
        mocker.patch("arrangeit.utils.get_player")
        app.App().setup_player()
        utils.get_player.assert_called()

    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_setup_calls_app_collector(self, mocker, platform):
        mocker.patch("arrangeit.utils.platform_path", return_value=platform)
        mocker.patch("arrangeit.utils.get_collector", return_value=get_collector(platform))
        mocker.patch("arrangeit.{}.collector.Collector.__call__".format(platform))
        app.App().setup()
        import arrangeit
        getattr(arrangeit, platform).collector.Collector.__call__.assert_called()
