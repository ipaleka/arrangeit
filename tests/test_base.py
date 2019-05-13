import pytest

from arrangeit import base, data, utils


class TestBaseApp(object):
    """Testing class for BaseApp class."""

    ## BaseApp
    def test_BaseApp_inits_collector_as_None(self):
        assert base.BaseApp.player is None

    def test_BaseApp_inits_player_as_None(self):
        assert base.BaseApp.collector is None

    ## BaseApp.__init__.collector
    def test_BaseApp_initialization_calls_setup_collector(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_collector")
        base.BaseApp()
        base.BaseApp.setup_collector.assert_called_once()

    def test_BaseApp_initialization_instantiate_collector(self, mocker):
        mainapp = base.BaseApp()
        assert getattr(mainapp, "collector", None) is not None
        assert isinstance(getattr(mainapp, "collector"), base.BaseCollector)

    ## BaseApp.__init__.player
    def test_BaseApp_initialization_calls_setup_player(self, mocker):
        mocker.patch("arrangeit.base.BaseApp.setup_player")
        base.BaseApp()
        base.BaseApp.setup_player.assert_called_once()

    def test_BaseApp_initialization_instantiate_player(self, mocker):
        mainapp = base.BaseApp()
        assert getattr(mainapp, "player", None) is not None
        assert isinstance(getattr(mainapp, "player"), base.BasePlayer)

    ## BaseApp.setup_collector
    def test_BaseApp_setup_collector_calls_get_collector(self, mocker):
        mocker.patch("arrangeit.utils.get_collector")
        base.BaseApp().setup_collector()
        utils.get_collector.assert_called()

    ## BaseApp.setup_player
    def test_BaseApp_setup_player_calls_get_player(self, mocker):
        mocker.patch("arrangeit.utils.get_player")
        base.BaseApp().setup_player()
        utils.get_player.assert_called()

    ## BaseApp.run
    def test_BaseApp_run_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseApp().run()


class TestBaseCollector(object):
    """Testing class for base Collector class."""

    ## BaseCollector
    def test_BaseCollector_inits_model_as_None(self):
        assert base.BaseCollector.model is None

    def test_BaseCollector_initialization_instantiate_WindowModel(self, mocker):
        collector = base.BaseCollector()
        assert getattr(collector, "model", None) is not None
        assert isinstance(getattr(collector, "model"), data.WindowModel)

    @pytest.mark.skip(reason="not implemented yet")
    def test_BaseCollector_next_calls_model_setup(self, mocker):
        pass

    @pytest.mark.skip(reason="not implemented yet")
    def test_BaseCollector_next_yields_model_instance(self, mocker):
        pass


class TestBasePlayer(object):
    """Testing class for base Player class."""

    @pytest.mark.skip(reason="not implemented yet")
    def test_BasePlayer_next_calls_BaseCollector_next(self, mocker):
        pass

