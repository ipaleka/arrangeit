import pytest

from arrangeit import base, data, utils


def mock_main_loop(mocker):
    mocker.patch("arrangeit.base.get_initialized_tk_root")
    mocker.patch("arrangeit.base.GuiApplication")
    mocker.patch("arrangeit.base.BasePlayer.mainloop")


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
    def test_BaseApp_run_calls_collector_run(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch(
            "arrangeit.{}.collector.Collector".format(utils.platform_path())
        )
        base.BaseApp().run()
        assert mocked.return_value.run.call_count == 1

    def test_BaseApp_run_calls_WindowsCollection_generator(self, mocker):
        mock_main_loop(mocker)
        mocked = mocker.patch("arrangeit.base.WindowsCollection")
        base.BaseApp().run()
        assert mocked.return_value.generator.call_count == 1

    def test_BaseApp_run_calls_player_run(self, mocker):
        mocked = mocker.patch(
            "arrangeit.{}.player.Player".format(utils.platform_path())
        )
        base.BaseApp().run()
        assert mocked.return_value.run.call_count == 1

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

    ## BaseCollector.run
    def test_BaseCollector_run_calls_get_windows(self, mocker):
        mocked = mocker.patch("arrangeit.base.BaseCollector.get_windows")
        base.BaseCollector().run()
        mocked.assert_called_once()

    def test_BaseCollector_run_calls_check_window(self, mocker):
        mocker.patch("arrangeit.base.BaseCollector.get_windows", return_value=(0,))
        mocked = mocker.patch("arrangeit.base.BaseCollector.check_window")
        mocker.patch("arrangeit.base.BaseCollector.add_window")
        base.BaseCollector().run()
        mocked.assert_called_once()

    @pytest.mark.parametrize("elems", [(), (5, 10, 15), (4,)])
    def test_BaseCollector__call___calls_add_window(self, mocker, elems):
        mocker.patch("arrangeit.base.BaseCollector.get_windows", return_value=elems)
        mocker.patch("arrangeit.base.BaseCollector.check_window")
        mocked = mocker.patch("arrangeit.base.BaseCollector.add_window")
        base.BaseCollector().run()
        if len(elems) > 0:
            mocked.assert_called()
        mocked.call_count == len(elems)


class TestBasePlayer(object):
    """Testing class for base Player class."""

    ## BasePlayer
    @pytest.mark.parametrize("attr", ["model", "generator", "gui"])
    def test_BasePlayer_inits_attr_as_None(self, attr):
        assert getattr(base.BasePlayer, attr) is None

    ## BasePlayer.__init__
    def test_BasePlayer_initialization_instantiate_WindowModel(self, mocker):
        player = base.BasePlayer()
        assert getattr(player, "model", None) is not None
        assert isinstance(getattr(player, "model"), data.WindowModel)

    def test_BasePlayer_initialization_calls_setup(self, mocker):
        mocked = mocker.patch("arrangeit.base.BasePlayer.setup")
        base.BasePlayer()
        mocked.assert_called_once()

    ## BasePlayer.setup
    def test_BasePlayer_setup_calls_get_initialized_tk_root(self, mocker):
        mocked = mocker.patch("arrangeit.base.get_initialized_tk_root")
        base.BasePlayer().setup()
        assert mocked.call_count == 2

    def test_BasePlayer_setup_initializes_GuiApplication(self, mocker):
        mocked = mocker.patch("arrangeit.base.GuiApplication")
        base.BasePlayer().setup()
        assert mocked.call_count == 2

    @pytest.mark.skip(reason="can't get it work... for now...")
    def test_BasePlayer_setup_initializes_GuiApplication_with_right_args(self, mocker):
        mocked_root = mocker.patch("arrangeit.base.get_initialized_tk_root")
        mocked = mocker.patch("arrangeit.base.GuiApplication")
        player = base.BasePlayer()
        player.setup()
        mocked.return_value.assert_called_with(mocked_root.return_value, player)

    def test_BasePlayer_setup_withdraws_root_tk_window(self, mocker):
        mocked = mocker.patch("arrangeit.gui.tk.Tk")
        base.BasePlayer().setup()
        assert mocked.return_value.withdraw.call_count == 2

    ## BasePlayer.run
    def test_BasePlayer_run_sets_generator_attribute_from_provided_attr(self, mocker):
        mocker.patch("arrangeit.base.get_initialized_tk_root")
        mocker.patch("arrangeit.base.GuiApplication")
        generator = mocker.MagicMock()
        player = base.BasePlayer()
        player.run(generator)
        assert player.generator == generator

    def test_BasePlayer_run_calls_next(self, mocker):
        mocker.patch("arrangeit.base.get_initialized_tk_root")
        mocker.patch("arrangeit.base.GuiApplication")
        mocked = mocker.patch("arrangeit.base.BasePlayer.next")
        base.BasePlayer().run(mocker.MagicMock())
        mocked.assert_called_once()

    @pytest.mark.parametrize("method", ["update", "deiconify"])
    def test_BasePlayer_run_calls_master_showing_up_method(self, mocker, method):
        mocker.patch("arrangeit.base.get_initialized_tk_root")
        mocked = mocker.patch("arrangeit.base.GuiApplication")
        mocker.patch("arrangeit.base.BasePlayer.next")
        base.BasePlayer().run(mocker.MagicMock())
        instance = mocked.return_value.master
        assert getattr(instance, method).call_count == 1

    def test_BasePlayer_run_calls_mainloop(self, mocker):
        mocker.patch("arrangeit.base.get_initialized_tk_root")
        mocker.patch("arrangeit.base.GuiApplication")
        mocked = mocker.patch("arrangeit.base.BasePlayer.mainloop")
        base.BasePlayer().run(mocker.MagicMock())
        mocked.assert_called_once()

    ## BasePlayer.next
    @pytest.mark.skip(reason="can't get it work... for now...")
    def test_BasePlayer_next_runs_generator(self, mocker):
        mocker.patch("arrangeit.base.get_initialized_tk_root")
        mocker.patch("arrangeit.base.GuiApplication")
        model = data.WindowModel()
        generator = mocker.MagicMock()
        player = base.BasePlayer()
        player.run(generator)
        player.next()
        assert generator.call_count == 1

    @pytest.mark.skip(reason="can't get it work... for now...")
    def test_BasePlayer_next_sets_model_attribute_from_generator(self, mocker):
        mocker.patch("arrangeit.base.get_initialized_tk_root")
        mocker.patch("arrangeit.base.GuiApplication")
        model = data.WindowModel()
        generator = mocker.MagicMock(return_value=model)
        player = base.BasePlayer()
        player.run(generator)
        player.next()
        assert player.model == model

    ## BasePlayer.mainloop
    def test_BasePlayer_main_loop_calls_Tkinter_mainloop(self, mocker):
        mocker.patch("arrangeit.base.get_initialized_tk_root")
        mocked = mocker.patch("arrangeit.base.GuiApplication")
        base.BasePlayer().mainloop()
        assert mocked.return_value.mainloop.call_count == 1
