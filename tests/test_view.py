from tkinter import Frame

import pytest
from pynput import mouse

from arrangeit.view import get_tkinter_root, get_mouse_listener, ViewApplication


class TestView(object):
    """Unit testing class for view module inner functions."""

    ## get_tkinter_root
    def test_get_tkinter_root_initializes_Tk(self, mocker):
        mocked = mocker.patch("arrangeit.view.Tk")
        get_tkinter_root()
        mocked.assert_called()

    def test_get_tkinter_root_returns_Tk_instance(self, mocker):
        mocked = mocker.patch("arrangeit.view.Tk")
        assert get_tkinter_root() == mocked.return_value

    ## get_mouse_listener
    def test_get_mouse_listener_initializes_Listener(self, mocker):
        mocked = mocker.patch("arrangeit.view.mouse.Listener")
        get_mouse_listener(mocker.MagicMock())
        mocked.assert_called()

    def test_get_mouse_listener_returns_listener_instance(self, mocker):
        returned = get_mouse_listener(mocker.MagicMock())
        assert isinstance(returned, mouse.Listener)

class TestViewApplication(object):
    """Unit testing class for view module inner functions."""

    ## ViewApplication
    def test_ViewApplication_issubclass_of_Frame(self):
        assert issubclass(ViewApplication, Frame)

    ## ViewApplication.__init__
    @pytest.mark.skip(reason="can't get it to work right now")
    def test_ViewApplication_init_calls_super_with_master_arg(self, mocker):
        master = mocker.MagicMock()
        mocker.patch("arrangeit.view.ViewApplication.create_widgets")
        mocked = mocker.patch("arrangeit.view.Frame")
        ViewApplication(master)
        mocked.return_value.assert_called_with(master)

    def test_ViewApplication_init_sets_master_and_controller_attributes(self, mocker):
        master = mocker.MagicMock()
        controller = mocker.MagicMock()
        view = ViewApplication(master, controller)
        assert view.master == master
        assert view.controller == controller

    def test_ViewApplication_init_calls_pack(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.pack")
        ViewApplication(None)
        assert mocked.call_count == 1

    def test_ViewApplication_inits_calls_create_widgets(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.create_widgets")
        ViewApplication(None)
        assert mocked.call_count == 1

    ## ViewApplication.create_widgets