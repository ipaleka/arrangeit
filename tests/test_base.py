import pytest

from arrangeit import base, data


class TestBaseApp(object):
    """Testing class for BaseApp class."""

    ## BaseApp
    def test_BaseApp_inits_collector_as_None(self):
        assert base.BaseApp.player is None

    def test_BaseApp_inits_player_as_None(self):
        assert base.BaseApp.collector is None

    ## BaseApp.__init__.collector
    def test_BaseApp_initialization_calls_setup_collector(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseApp.setup_collector")
        base.BaseApp()
        mocked.assert_called_once()

    def test_BaseApp_initialization_instantiate_collector(self, mocker):
        mainapp = base.BaseApp()
        assert getattr(mainapp, "collector", None) is not None
        assert isinstance(getattr(mainapp, "collector"), base.BaseCollector)

    ## BaseApp.__init__.player
    def test_BaseApp_initialization_calls_setup_player(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseApp.setup_player")
        base.BaseApp()
        mocked.assert_called_once()

    def test_BaseApp_initialization_instantiate_player(self, mocker):
        mainapp = base.BaseApp()
        assert getattr(mainapp, "player", None) is not None
        assert isinstance(getattr(mainapp, "player"), base.BasePlayer)

    ## BaseApp.setup_collector
    def test_BaseApp_setup_collector_calls_get_collector(self, mocker):
        mocked = mocker.patch("arrangeit.utils.get_collector")
        base.BaseApp().setup_collector()
        mocked.assert_called()

    ## BaseApp.setup_player
    def test_BaseApp_setup_player_calls_get_player(self, mocker):
        mocked = mocker.patch("arrangeit.utils.get_player")
        base.BaseApp().setup_player()
        mocked.assert_called()

    ## BaseApp.run
    def test_BaseApp_run_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseApp().run()


class TestBaseCollector(object):
    """Testing class for base Collector class."""

    ## BaseCollector
    def test_BaseCollector_inits_collection_as_None(self):
        assert base.BaseCollector.collection is None

    ## BaseCollector.__init__
    def test_BaseCollector_initialization_instantiate_WindowsCollection(self, mocker):
        collector = base.BaseCollector()
        assert getattr(collector, "collection", None) is not None
        assert isinstance(getattr(collector, "collection"), data.WindowsCollection)

    ## BaseCollector.is_applicable
    def test_BaseCollector_is_applicable_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().is_applicable(0)

    ## BaseCollector.is_valid_state
    def test_BaseCollector_is_valid_state_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().is_valid_state(0, 0)

    ## BaseCollector.is_resizable
    def test_BaseCollector_is_resizable_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().is_resizable(0)

    ## BaseCollector.get_windows
    def test_BaseCollector_get_windows_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().get_windows()

    ## BaseCollector.check_window
    def test_BaseCollector_check_window_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().check_window(None)

    ## BaseCollector.add_window
    def test_BaseCollector_add_window_raises_NotImplementedError(self):
        with pytest.raises(NotImplementedError):
            base.BaseCollector().add_window(None)

    ## BaseCollector.__call__
    def test_BaseCollector__call___calls_get_windows(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseCollector.get_windows")
        base.BaseCollector()()
        mocked.assert_called_once()

    def test_BaseCollector__call___calls_check_window(self, mocker):
        mocker.patch("arrangeit.base.BaseCollector.get_windows", return_value=(0,))
        mocked = mocker.patch("arrangeit.base.BaseCollector.check_window")
        mocker.patch("arrangeit.base.BaseCollector.add_window")
        base.BaseCollector()()
        mocked.assert_called_once()

    @pytest.mark.parametrize("elems", [(), (5, 10, 15), (4,)])
    def test_BaseCollector__call___calls_add_window(self, mocker, elems):
        mocker.patch("arrangeit.base.BaseCollector.get_windows", return_value=elems)
        mocker.patch("arrangeit.base.BaseCollector.check_window")
        mocked = mocker.patch("arrangeit.base.BaseCollector.add_window")
        base.BaseCollector()()
        if len(elems) > 0:
            mocked.assert_called()
        mocked.call_count == len(elems)


class TestBasePlayer(object):
    """Testing class for base Player class."""

    def test_BasePlayer_inits_model_as_None(self):
        assert base.BasePlayer.model is None

    def test_BasePlayer_initialization_instantiate_WindowModel(self, mocker):
        player = base.BasePlayer()
        assert getattr(player, "model", None) is not None
        assert isinstance(getattr(player, "model"), data.WindowModel)
