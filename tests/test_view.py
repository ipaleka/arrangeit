import tkinter as tk

import pytest

from arrangeit.data import WindowModel
from arrangeit.view import (
    click_left,
    get_tkinter_root,
    get_mouse_listener,
    move_cursor,
    ViewApplication,
)
from arrangeit.constants import (
    TITLE_LABEL_FG,
    TITLE_LABEL_BG,
    TITLE_LABEL_ANCHOR,
    TITLE_LABEL_PADX,
    TITLE_LABEL_PADY,
)


class TestViewFunctions(object):
    """Unit testing class for view module inner functions."""

    ## get_tkinter_root
    def test_get_tkinter_root_initializes_Tk(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Tk")
        get_tkinter_root()
        mocked.assert_called()

    def test_get_tkinter_root_returns_Tk_instance(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Tk")
        assert get_tkinter_root() == mocked.return_value

    ## get_mouse_listener
    def test_get_mouse_listener_initializes_Listener(self, mocker):
        mocked = mocker.patch("arrangeit.view.mouse.Listener")
        get_mouse_listener(mocker.MagicMock())
        mocked.assert_called()

    def test_get_mouse_listener_returns_listener_instance(self, mocker):
        mocked = mocker.patch("pynput.mouse.Listener")
        returned = get_mouse_listener(mocker.MagicMock())
        assert returned == mocked.return_value

    ## click_left
    def test_click_left_initializes_Controller(self, mocker):
        mocked = mocker.patch("arrangeit.view.mouse.Controller")
        click_left()
        mocked.assert_called()

    def test_click_left_calls_press_and_release(self, mocker):
        mocked = mocker.patch("pynput.mouse.Controller")
        click_left()
        mocked.return_value.press.assert_called_once()
        mocked.return_value.release.assert_called_once()

    ## move_cursor
    def test_move_cursor_initializes_Controller(self, mocker):
        mocked = mocker.patch("arrangeit.view.mouse.Controller")
        move_cursor(0, 0)
        mocked.assert_called()

    def test_move_cursor_calls_position_with_provided_x_and_y(self, mocker):
        mocked = mocker.patch("pynput.mouse.Controller")
        xy = (101, 202)
        move_cursor(*xy)
        assert mocked.return_value.position == xy


class TestViewApplication(object):
    """Unit testing class for view module inner functions."""

    ## ViewApplication
    def test_ViewApplication_issubclass_of_Frame(self):
        assert issubclass(ViewApplication, tk.Frame)

    ## ViewApplication.__init__
    def test_ViewApplication_init_calls_super_with_master_arg(self, mocker):
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.tk.Frame.__init__")
        with pytest.raises(AttributeError):
            ViewApplication(master=master, controller=mocker.MagicMock())
            mocked.assert_called_with(master)

    def test_ViewApplication_init_sets_master_and_controller_attributes(self, mocker):
        master = mocker.MagicMock()
        controller = mocker.MagicMock()
        mocker.patch("arrangeit.view.ViewApplication.setup_bindings")
        mocker.patch("arrangeit.view.ViewApplication.setup_widgets")
        view = ViewApplication(master, controller)
        assert view.master == master
        assert view.controller == controller

    def test_ViewApplication_init_calls_pack(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.pack")
        ViewApplication(None, mocker.MagicMock())
        assert mocked.call_count == 1

    def test_ViewApplication_inits_calls_setup_bindings(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_bindings")
        ViewApplication(None, mocker.MagicMock())
        assert mocked.call_count == 1

    def test_ViewApplication_inits_calls_setup_widgets(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_widgets")
        ViewApplication(None, mocker.MagicMock())
        assert mocked.call_count == 1

    ## ViewApplication.setup_widgets
    @pytest.mark.parametrize("name,typ", [("title", tk.StringVar)])
    def test_ViewApplication_setup_widgets_sets_tk_variable(self, mocker, name, typ):
        view = ViewApplication(None, mocker.MagicMock())
        setattr(view, name, None)
        view.setup_widgets()
        assert isinstance(getattr(view, name), typ)

    def test_ViewApplication_setup_widgets_sets_title_label(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_widgets()
        mocked.assert_called_with(
            textvariable=view.title,
            foreground=TITLE_LABEL_FG,
            background=TITLE_LABEL_BG,
            anchor=TITLE_LABEL_ANCHOR,
            padx=TITLE_LABEL_PADX,
            pady=TITLE_LABEL_PADY,
        )

    ## ViewApplication.setup_bindings
    @pytest.mark.parametrize(
        "event,method",
        [
            ("<Escape>", "on_escape_key_pressed"),
            ("<Button-1>", "on_mouse_left_down"),
            ("<Button-2>", "on_mouse_middle_down"),
            ("<Button-3>", "on_mouse_right_down"),
        ],
    )
    def test_ViewApplication_setup_bindings_callbacks(self, mocker, event, method):
        controller = mocker.MagicMock()
        view = ViewApplication(None, controller)
        callback = getattr(controller, method)
        mocked = mocker.patch("arrangeit.view.ViewApplication.bind_all")
        view.setup_bindings()
        calls = [mocker.call(event, callback)]
        mocked.assert_has_calls(calls, any_order=True)

    ## ViewApplication.update_widgets
    @pytest.mark.parametrize("attr,val,typ", [("title", "foo", tk.StringVar)])
    def test_ViewApplication_update_widgets_set_attr(self, mocker, attr, val, typ):
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(**{attr: val})
        view.update_widgets(model)
        instance = getattr(view, attr)
        assert instance.get() == getattr(model, attr)
        assert isinstance(instance, typ)
