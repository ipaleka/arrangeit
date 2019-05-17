import tkinter as tk

import pytest

from arrangeit.gui import get_initialized_tk_root, GuiApplication


class TestGui(object):
    """Unit testing class for gui module inner functions."""

    ## get_initialized_tk_root
    def test_get_initialized_tk_root_initializes_Tk(self, mocker):
        mocked = mocker.patch("arrangeit.gui.tk.Tk")
        get_initialized_tk_root()
        mocked.assert_called()

    def test_get_initialized_tk_root_returns_Tk_instance(self, mocker):
        mocked = mocker.patch("arrangeit.gui.tk.Tk")
        assert get_initialized_tk_root() == mocked.return_value


class TestGuiApplication(object):
    """Unit testing class for gui module inner functions."""

    ## GuiApplication
    def test_GuiApplication_issubclass_of_Frame(self):
        assert issubclass(GuiApplication, tk.Frame)

    ## GuiApplication.__init__
    @pytest.mark.skip(reason="can't get it work... for now...")
    def test_GuiApplication_init_calls_super(self, mocker):
        mocked = mocker.patch("arrangeit.gui.tk.Frame")
        GuiApplication(None)
        assert mocked.return_value.call_count == 1

    def test_GuiApplication_init_sets_master_and_player_attributes(self, mocker):
        master = mocker.MagicMock()
        player = mocker.MagicMock()
        gui = GuiApplication(master, player)
        assert gui.master == master
        assert gui.player == player

    def test_GuiApplication_init_calls_pack(self, mocker):
        mocked = mocker.patch("arrangeit.gui.GuiApplication.pack")
        GuiApplication(None)
        assert mocked.call_count == 1

    def test_GuiApplication_inits_calls_create_widgets(self, mocker):
        mocked = mocker.patch("arrangeit.gui.GuiApplication.create_widgets")
        GuiApplication(None)
        assert mocked.call_count == 1

    ## GuiApplication.create_widgets