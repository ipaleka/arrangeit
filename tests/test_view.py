import tkinter as tk
from tkinter.font import nametofont

import pytest

from arrangeit.data import WindowModel
from arrangeit.view import (
    click_left,
    get_tkinter_root,
    get_mouse_listener,
    move_cursor,
    ViewApplication,
    WorkspacesCollection,
    WindowsList,
)
from arrangeit.constants import (
    TITLE_LABEL_FG,
    TITLE_LABEL_BG,
    TITLE_LABEL_ANCHOR,
    TITLE_LABEL_FONT_INCREASE,
    TITLE_LABEL_HEIGHT,
    TITLE_LABEL_PADX,
    TITLE_LABEL_PADY,
    ICON_LABEL_BG,
    ICON_LABEL_ANCHOR,
    ICON_LABEL_PADX,
    ICON_LABEL_PADY,
    NAME_LABEL_ANCHOR,
    NAME_LABEL_BG,
    NAME_LABEL_FG,
    NAME_LABEL_HEIGHT,
    NAME_LABEL_PADX,
    NAME_LABEL_PADY,
    BLANK_ICON,
)
from arrangeit.utils import increased_by_fraction


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
    """Unit testing class for ViewApplication class."""

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

    ## ViewApplication.setup_title
    @pytest.mark.parametrize("name,typ", [("title", tk.StringVar)])
    def test_ViewApplication_setup_title_sets_tk_variable(self, mocker, name, typ):
        view = ViewApplication(None, mocker.MagicMock())
        setattr(view, name, None)
        view.setup_title()
        assert isinstance(getattr(view, name), typ)

    def test_ViewApplication_setup_title_sets_title_label(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_title()
        mocked.assert_called_with(
            view,
            textvariable=view.title,
            font=(
                "TkDefaultFont",
                increased_by_fraction(
                    nametofont("TkDefaultFont")["size"], TITLE_LABEL_FONT_INCREASE
                ),
            ),
            height=TITLE_LABEL_HEIGHT,
            foreground=TITLE_LABEL_FG,
            background=TITLE_LABEL_BG,
            anchor=TITLE_LABEL_ANCHOR,
            padx=TITLE_LABEL_PADX,
            pady=TITLE_LABEL_PADY,
        )

    def test_ViewApplication_setup_title_calls_label_grid(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.grid.call_count = 0
        view.setup_title()
        assert mocked.return_value.grid.call_count == 1

    ## ViewApplication.setup_icon
    def test_ViewApplication_setup_icon_sets_icon_label(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_icon()
        mocked.assert_called_with(
            view,
            bitmap="hourglass",
            background=ICON_LABEL_BG,
            anchor=ICON_LABEL_ANCHOR,
            padx=ICON_LABEL_PADX,
            pady=ICON_LABEL_PADY,
        )

    def test_ViewApplication_setup_icon_calls_label_grid(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.grid.call_count = 0
        view.setup_icon()
        assert mocked.return_value.grid.call_count == 1

    ## ViewApplication.setup_name
    def test_ViewApplication_setup_name_sets_tk_variable(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        view.name = None
        view.setup_name()
        assert isinstance(view.name, tk.StringVar)

    def test_ViewApplication_setup_name_sets_name_label(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_name()
        mocked.assert_called_with(
            view,
            textvariable=view.name,
            height=TITLE_LABEL_HEIGHT,
            foreground=TITLE_LABEL_FG,
            background=TITLE_LABEL_BG,
            anchor=NAME_LABEL_ANCHOR,
            padx=NAME_LABEL_PADX,
            pady=NAME_LABEL_PADY,
        )

    def test_ViewApplication_setup_name_calls_label_grid(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.grid.call_count = 0
        view.setup_name()
        assert mocked.return_value.grid.call_count == 1

    ## ViewApplication.setup_workspaces
    def test_ViewApplication_setup_workspaces_initializes_WorkspacesCollection(
        self, mocker
    ):
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_workspaces()
        assert isinstance(view.workspaces, WorkspacesCollection)

    def test_ViewApplication_setup_workspaces_sets_viewapp_as_parent(self, mocker):
        mocked = mocker.patch("arrangeit.view.WorkspacesCollection")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_workspaces()
        mocked.assert_called_with(view)

    def test_ViewApplication_setup_workspaces_calls_WorkspacesCollection_grid(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.view.WorkspacesCollection")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.grid.call_count = 0
        view.setup_workspaces()
        assert mocked.return_value.grid.call_count == 1

    ## ViewApplication.setup_windows
    def test_ViewApplication_setup_windows_initializes_WindowsList(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_windows()
        assert isinstance(view.windows, WindowsList)

    def test_ViewApplication_setup_windows_sets_viewapp_as_parent(self, mocker):
        mocked = mocker.patch("arrangeit.view.WindowsList")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_windows()
        mocked.assert_called_with(view)

    def test_ViewApplication_setup_windows_calls_WindowsList_grid(self, mocker):
        mocked = mocker.patch("arrangeit.view.WindowsList")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.grid.call_count = 0
        view.setup_windows()
        assert mocked.return_value.grid.call_count == 1

    ## ViewApplication.setup_widgets
    def test_ViewApplication_setup_widgets_calls_grid_columnconfigure(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Frame.grid_columnconfigure")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.call_count = 0
        mocked.calls = []
        view.setup_widgets()
        assert mocked.call_count == 2
        calls = [mocker.call(0, weight=7), mocker.call(2, weight=2)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_ViewApplication_setup_widgets_calls_setup_title(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_title")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.call_count = 0
        view.setup_widgets()
        assert mocked.call_count == 1

    def test_ViewApplication_setup_widgets_calls_setup_icon(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_icon")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.call_count = 0
        view.setup_widgets()
        assert mocked.call_count == 1

    def test_ViewApplication_setup_widgets_calls_setup_name(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_name")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.call_count = 0
        view.setup_widgets()
        assert mocked.call_count == 1

    def test_ViewApplication_setup_widgets_calls_setup_workspaces(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_workspaces")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.call_count = 0
        view.setup_widgets()
        assert mocked.call_count == 1

    def test_ViewApplication_setup_widgets_calls_setup_windows(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_windows")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.call_count = 0
        view.setup_widgets()
        assert mocked.call_count == 1

    ## ViewApplication.setup_bindings
    @pytest.mark.parametrize(
        "event,method",
        [
            ("<Button-1>", "on_mouse_left_down"),
            ("<Button-2>", "on_mouse_middle_down"),
            ("<Button-3>", "on_mouse_right_down"),
            ("<Key>", "on_key_pressed"),
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

    ## ViewApplication.startup
    @pytest.mark.parametrize("method", ["update", "deiconify"])
    def test_ViewApplication_startup_calls_master_showing_up_method(
        self, mocker, method
    ):
        mocker.patch("arrangeit.view.tk.StringVar")
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        master = mocker.MagicMock()
        ViewApplication(master, mocker.MagicMock()).startup()
        assert getattr(master, method).call_count == 1

    def test_ViewApplication_startup_calls_focus_set_on_view_frame(self, mocker):
        mocker.patch("arrangeit.view.tk.StringVar")
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocked = mocker.patch("arrangeit.view.tk.Frame.focus_set")
        ViewApplication(mocker.MagicMock(), mocker.MagicMock()).startup()
        assert mocked.call_count == 1

    def test_ViewApplication_startup_calls_configure_on_labels(self, mocker):
        mocker.patch("arrangeit.view.tk.StringVar")
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocked = mocker.patch("arrangeit.view.tk.Label.configure")
        ViewApplication(mocker.MagicMock(), mocker.MagicMock()).startup()
        assert mocked.call_count == 2

    ## ViewApplication.update_widgets
    @pytest.mark.parametrize(
        "attr,val,typ", [("title", "foo", tk.StringVar), ("name", "bar", tk.StringVar)]
    )
    def test_ViewApplication_update_widgets_sets_attr(self, mocker, attr, val, typ):
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(**{attr: val}, icon=BLANK_ICON)
        view.update_widgets(model)
        instance = getattr(view, attr)
        assert instance.get() == getattr(model, attr)
        assert isinstance(instance, typ)

    def test_ViewApplication_update_widgets_calls_ImageTk_PhotoImage(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(icon=BLANK_ICON)
        mocker.patch("arrangeit.view.tk.Label.configure")
        mocked = mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        view.update_widgets(model)
        mocked.call_count == 1
        mocked.assert_called_with(model.icon)

    def test_ViewApplication_update_widgets_sets_icon_image(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(icon=BLANK_ICON)
        mocker.patch("arrangeit.view.tk.Label.configure")
        mocked = mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        view.update_widgets(model)
        assert view.icon_image == mocked.return_value

    def test_ViewApplication_update_widgets_sets_icon(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(icon=BLANK_ICON)
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view.update_widgets(model)
        mocked.return_value.configure.call_count == 1


class TestWorkspacesCollection(object):
    """Unit testing class for WorkspacesCollection class."""

    ## WorkspacesCollection
    def test_WorkspacesCollection_issubclass_of_Frame(self):
        assert issubclass(WorkspacesCollection, tk.Frame)

    ## WorkspacesCollection.__init__
    def test_WorkspacesCollection_init_calls_super_with_parent_arg(self, mocker):
        parent = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.tk.Frame.__init__")
        with pytest.raises(AttributeError):
            WorkspacesCollection(parent=parent)
            mocked.assert_called_with(parent)

    def test_WorkspacesCollection_init_sets_parent_attribute(self, mocker):
        parent = mocker.MagicMock()
        workspaces = WorkspacesCollection(parent)
        assert workspaces.parent == parent

    # def test_WorkspacesCollection_init_calls_grid(self, mocker):
    #     mocked = mocker.patch("arrangeit.view.WorkspacesCollection.grid")
    #     WorkspacesCollection(None)
    #     assert mocked.call_count == 1


class TestWindowsList(object):
    """Unit testing class for WindowsList class."""

    ## WindowsList
    def test_WindowsList_issubclass_of_Frame(self):
        assert issubclass(WindowsList, tk.Frame)

    ## WindowsList.__init__
    def test_WindowsList_init_calls_super_with_parent_arg(self, mocker):
        parent = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.tk.Frame.__init__")
        with pytest.raises(AttributeError):
            WindowsList(parent=parent)
            mocked.assert_called_with(parent)

    def test_WindowsList_init_sets_parent_attribute(self, mocker):
        parent = mocker.MagicMock()
        windows = WindowsList(parent)
        assert windows.parent == parent

    # def test_WindowsList_init_calls_grid(self, mocker):
    #     mocked = mocker.patch("arrangeit.view.WindowsList.grid")
    #     WindowsList(None)
    #     assert mocked.call_count == 1
