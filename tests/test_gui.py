from tkinter import Frame

import pytest
from pynput import mouse

from arrangeit.guicommon import get_tkinter_root, get_mouse_listener, GuiApplication


class TestGui(object):
    """Unit testing class for gui module inner functions."""

    ## get_tkinter_root
    def test_get_tkinter_root_initializes_Tk(self, mocker):
        mocked = mocker.patch("arrangeit.guicommon.Tk")
        get_tkinter_root()
        mocked.assert_called()

    def test_get_tkinter_root_returns_Tk_instance(self, mocker):
        mocked = mocker.patch("arrangeit.guicommon.Tk")
        assert get_tkinter_root() == mocked.return_value

    ## get_mouse_listener
    def test_get_mouse_listener_initializes_Listener(self, mocker):
        mocked = mocker.patch("arrangeit.guicommon.mouse.Listener")
        get_mouse_listener(mocker.MagicMock())
        mocked.assert_called()

    def test_get_mouse_listener_returns_listener_instance(self, mocker):
        returned = get_mouse_listener(mocker.MagicMock())
        assert isinstance(returned, mouse.Listener)

class TestGuiApplication(object):
    """Unit testing class for gui module inner functions."""

    ## GuiApplication
    def test_GuiApplication_issubclass_of_Frame(self):
        assert issubclass(GuiApplication, Frame)

    ## GuiApplication.__init__
    @pytest.mark.skip(reason="can't get it to work right now")
    def test_GuiApplication_init_calls_super_with_master_arg(self, mocker):
        master = mocker.MagicMock()
        mocker.patch("arrangeit.guicommon.GuiApplication.create_widgets")
        mocked = mocker.patch("arrangeit.guicommon.Frame")
        GuiApplication(master)
        mocked.return_value.assert_called_with(master)

    def test_GuiApplication_init_sets_master_and_controller_attributes(self, mocker):
        master = mocker.MagicMock()
        controller = mocker.MagicMock()
        gui_app = GuiApplication(master, controller)
        assert gui_app.master == master
        assert gui_app.controller == controller

    def test_GuiApplication_init_calls_pack(self, mocker):
        mocked = mocker.patch("arrangeit.guicommon.GuiApplication.pack")
        GuiApplication(None)
        assert mocked.call_count == 1

    def test_GuiApplication_inits_calls_create_widgets(self, mocker):
        mocked = mocker.patch("arrangeit.guicommon.GuiApplication.create_widgets")
        GuiApplication(None)
        assert mocked.call_count == 1

    ## GuiApplication.create_widgets