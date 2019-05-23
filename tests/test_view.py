import tkinter as tk
from tkinter.font import nametofont

from PIL import ImageTk
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
    Workspace,
    ListedWindow,
)
from arrangeit import constants
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
                    nametofont("TkDefaultFont")["size"],
                    constants.TITLE_LABEL_FONT_INCREASE,
                ),
            ),
            height=constants.TITLE_LABEL_HEIGHT,
            foreground=constants.TITLE_LABEL_FG,
            background=constants.TITLE_LABEL_BG,
            anchor=constants.TITLE_LABEL_ANCHOR,
            padx=constants.TITLE_LABEL_PADX,
            pady=constants.TITLE_LABEL_PADY,
        )

    def test_ViewApplication_setup_title_calls_label_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.place.call_count = 0
        view.setup_title()
        assert mocked.return_value.place.call_count == 1
        mocked.return_value.place.assert_called_with(
            relheight=constants.TITLE_LABEL_RELHEIGHT,
            relwidth=constants.TITLE_LABEL_RELWIDTH,
        )

    ## ViewApplication.setup_icon
    def test_ViewApplication_setup_icon_sets_icon_label(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_icon()
        mocked.assert_called_with(
            view,
            bitmap="hourglass",
            background=constants.ICON_LABEL_BG,
            anchor=constants.ICON_LABEL_ANCHOR,
            padx=constants.ICON_LABEL_PADX,
            pady=constants.ICON_LABEL_PADY,
        )

    def test_ViewApplication_setup_icon_calls_label_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.place.call_count = 0
        view.setup_icon()
        assert mocked.return_value.place.call_count == 1
        mocked.return_value.place.assert_called_with(
            relx=constants.TITLE_LABEL_RELWIDTH + constants.NAME_LABEL_RELWIDTH / 2,
            anchor=constants.ICON_LABEL_ANCHOR,
            y=constants.ICON_LABEL_PADY,
        )

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
            height=constants.NAME_LABEL_HEIGHT,
            foreground=constants.NAME_LABEL_FG,
            background=constants.NAME_LABEL_BG,
            anchor=constants.NAME_LABEL_ANCHOR,
            padx=constants.NAME_LABEL_PADX,
            pady=constants.NAME_LABEL_PADY,
        )

    def test_ViewApplication_setup_name_calls_label_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.place.call_count = 0
        view.setup_name()
        assert mocked.return_value.place.call_count == 1
        mocked.return_value.place.assert_called_with(
            relx=constants.TITLE_LABEL_RELWIDTH,
            relheight=constants.NAME_LABEL_RELHEIGHT,
            relwidth=constants.NAME_LABEL_RELWIDTH,
        )

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

    def test_ViewApplication_setup_workspaces_calls_WorkspacesCollection_place(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.view.WorkspacesCollection")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.place.call_count = 0
        view.setup_workspaces()
        assert mocked.return_value.place.call_count == 1
        mocked.return_value.place.assert_called_with(
            rely=constants.NAME_LABEL_RELHEIGHT,
            relx=constants.TITLE_LABEL_RELWIDTH,
            relheight=constants.WORKSPACES_FRAME_RELHEIGHT,
            relwidth=constants.WORKSPACES_FRAME_RELWIDTH,
        )

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

    def test_ViewApplication_setup_windows_calls_WindowsList_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.WindowsList")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.place.call_count = 0
        view.setup_windows()
        assert mocked.return_value.place.call_count == 1
        mocked.return_value.place.assert_called_with(
            rely=constants.TITLE_LABEL_RELHEIGHT,
            relheight=constants.WINDOWS_LIST_RELHEIGHT,
            relwidth=constants.WINDOWS_LIST_RELWIDTH,
        )

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

    def test_ViewApplication_startup_calls_place_on_view_frame(self, mocker):
        mocker.patch("arrangeit.view.tk.StringVar")
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocked = mocker.patch("arrangeit.view.tk.Frame.place")
        master = mocker.MagicMock()
        view = ViewApplication(master, mocker.MagicMock())
        mocked.call_count = 0
        view.startup()
        assert mocked.call_count == 1
        mocked.assert_called_with(
            width=master.winfo_width.return_value,
            height=master.winfo_height.return_value,
        )

    def test_ViewApplication_startup_calls_configure_on_labels(self, mocker):
        mocker.patch("arrangeit.view.tk.StringVar")
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocked = mocker.patch("arrangeit.view.tk.Label.configure")
        master = mocker.MagicMock()
        master.winfo_width.return_value = 100
        ViewApplication(master, mocker.MagicMock()).startup()
        assert mocked.call_count == 2
        calls = [
            mocker.call(wraplength=int(100 * constants.TITLE_LABEL_RELWIDTH)),
            mocker.call(wraplength=int(100 * constants.NAME_LABEL_RELWIDTH)),
        ]
        mocked.assert_has_calls(calls, any_order=True)

    ## ViewApplication.update_widgets
    @pytest.mark.parametrize(
        "attr,val,typ", [("title", "foo", tk.StringVar), ("name", "bar", tk.StringVar)]
    )
    def test_ViewApplication_update_widgets_sets_attr(self, mocker, attr, val, typ):
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(**{attr: val}, icon=constants.BLANK_ICON)
        view.update_widgets(model)
        instance = getattr(view, attr)
        assert instance.get() == getattr(model, attr)
        assert isinstance(instance, typ)

    def test_ViewApplication_update_widgets_calls_ImageTk_PhotoImage(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(icon=constants.BLANK_ICON)
        mocker.patch("arrangeit.view.tk.Label.configure")
        mocked = mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        view.update_widgets(model)
        mocked.call_count == 1
        mocked.assert_called_with(model.icon)

    def test_ViewApplication_update_widgets_sets_icon_image(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(icon=constants.BLANK_ICON)
        mocker.patch("arrangeit.view.tk.Label.configure")
        mocked = mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        view.update_widgets(model)
        assert view.icon_image == mocked.return_value

    def test_ViewApplication_update_widgets_sets_icon(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(icon=constants.BLANK_ICON)
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view.update_widgets(model)
        mocked.return_value.configure.call_count == 1

    def test_ViewApplication_update_widgets_calls_workspaces_select_active(
        self, mocker
    ):
        mocker.patch("arrangeit.view.tk.Label.configure")
        mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        mocked = mocker.patch("arrangeit.view.WorkspacesCollection")
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(workspace=1002)
        view.update_widgets(model)
        mocked.return_value.select_active.call_count == 1
        calls = [mocker.call(1002)]
        mocked.return_value.select_active.assert_has_calls(calls, any_order=True)


class TestWorkspacesCollection(object):
    """Unit testing class for WorkspacesCollection class."""

    ## WorkspacesCollection
    def test_WorkspacesCollection_issubclass_of_Frame(self):
        assert issubclass(WorkspacesCollection, tk.Frame)

    ## WorkspacesCollection.__init__
    def test_WorkspacesCollection_init_calls_super_with_parent_arg(self, mocker):
        mocker.patch("arrangeit.view.tk.Frame.config")
        parent = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.tk.Frame.__init__")
        WorkspacesCollection(parent=parent)
        mocked.assert_called_with(parent)

    def test_WorkspacesCollection_init_sets_parent_attribute(self, mocker):
        parent = mocker.MagicMock()
        workspaces = WorkspacesCollection(parent)
        assert workspaces.parent == parent

    def test_WorkspacesCollection_init_calls_config_background(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Frame.config")
        parent = mocker.MagicMock()
        WorkspacesCollection(parent)
        assert mocked.call_count == 1
        calls = [mocker.call(background=constants.WORKSPACE_NUMBER_LABEL_BG)]
        mocked.assert_has_calls(calls, any_order=True)

    ## WorkspacesCollection.add_workspaces
    def test_WorkspacesCollection_add_workspaces_initializes_Workspace(self, mocker):
        parent = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.Workspace")
        workspaces = WorkspacesCollection(parent=parent)
        args = [(0, "foo"), (1, "bar")]
        workspaces.add_workspaces(args)
        assert mocked.call_count == 2
        calls = [
            mocker.call(workspaces, number=0, name="foo"),
            mocker.call(workspaces, number=1, name="bar"),
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_WorkspacesCollection_add_workspaces_not_calling_place(self, mocker):
        parent = mocker.MagicMock()
        mocker.patch("arrangeit.view.Workspace")
        workspaces = WorkspacesCollection(parent=parent)
        mocked = mocker.patch("arrangeit.view.tk.Frame")
        workspaces.add_workspaces([(0, "foo")])
        mocked.return_value.place.assert_not_called()

    @pytest.mark.parametrize(
        "args",
        [
            [(0, "foo"), (1, "bar")],
            [(0, "foo"), (1, "bar"), (2, "foobar")],
            [(0, "foo"), (1, "bar"), (2, "foobar"), (3, "barfoo")],
            [(0, "foo"), (1, "bar"), (2, "foobar"), (3, "barfoo"), (4, "")],
        ],
    )
    def test_WorkspacesCollection_add_workspaces_calls_place_on_frame(
        self, mocker, args
    ):
        parent = mocker.MagicMock()
        mocker.patch("arrangeit.view.Workspace")
        workspaces = WorkspacesCollection(parent=parent)
        mocked = mocker.patch("arrangeit.view.Workspace")
        workspaces.add_workspaces(args)
        assert mocked.return_value.place.call_count == len(args)
        relheight = float(1 / ((len(args) - 1) // 2 + 1))
        calls = []
        for i in range(len(args)):
            calls.append(
                mocker.call(
                    relheight=relheight,
                    relwidth=0.5,
                    relx=(i % 2) * 0.5,
                    rely=(i // 2) * relheight,
                )
            )
        mocked.return_value.place.assert_has_calls(calls, any_order=True)

    ## WorkspacesCollection.select_active
    def test_WorkspacesCollection_select_active_for_single_workspace(self, mocker):
        workspaces = WorkspacesCollection()
        children = mocker.patch(
            "arrangeit.view.WorkspacesCollection.winfo_children",
            return_value=[mocker.MagicMock()],
        )
        returned = workspaces.select_active(1000)
        assert returned is True

    def test_WorkspacesCollection_select_active_calls_label_config(self, mocker):
        workspaces = WorkspacesCollection()
        widget0 = mocker.MagicMock()
        type(widget0).number = mocker.PropertyMock(return_value=1000)
        widget1 = mocker.MagicMock()
        type(widget1).number = mocker.PropertyMock(return_value=1001)
        widget2 = mocker.MagicMock()
        type(widget2).number = mocker.PropertyMock(return_value=1002)
        mocker.patch(
            "arrangeit.view.WorkspacesCollection.winfo_children",
            return_value=[widget0, widget1, widget2],
        )
        workspaces.select_active(1001)
        calls = [mocker.call(foreground=constants.WORKSPACE_NUMBER_LABEL_FG)]
        widget0.number_label.config.assert_has_calls(calls, any_order=True)
        widget2.number_label.config.assert_has_calls(calls, any_order=True)
        calls = [mocker.call(foreground=constants.WORKSPACE_NAME_LABEL_FG)]
        widget0.name_label.config.assert_has_calls(calls, any_order=True)
        widget2.name_label.config.assert_has_calls(calls, any_order=True)
        calls = [mocker.call(foreground=constants.SELECTED_COLOR)]
        widget1.number_label.config.assert_has_calls(calls, any_order=True)
        widget1.name_label.config.assert_has_calls(calls, any_order=True)


class TestWindowsList(object):
    """Unit testing class for WindowsList class."""

    ## WindowsList
    def test_WindowsList_issubclass_of_Frame(self):
        assert issubclass(WindowsList, tk.Frame)

    ## WindowsList.__init__
    def test_WindowsList_init_calls_super_with_parent_arg(self, mocker):
        parent = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.tk.Frame.__init__")
        WindowsList(parent=parent)
        mocked.assert_called_with(parent)

    def test_WindowsList_init_sets_parent_attribute(self, mocker):
        parent = mocker.MagicMock()
        windows = WindowsList(parent)
        assert windows.parent == parent

    ## WindowsList.add_windows
    def test_WindowsList_add_windows_initializes_ListedWindow(self, mocker):
        parent = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.ListedWindow")
        windows = WindowsList(parent=parent)
        windows_list = [
            (100, "foo", constants.BLANK_ICON),
            (200, "bar", constants.BLANK_ICON),
        ]
        windows.add_windows(windows_list)
        assert mocked.call_count == 2
        calls = [
            mocker.call(windows, wid=100, title="foo", icon=constants.BLANK_ICON),
            mocker.call(windows, wid=200, title="bar", icon=constants.BLANK_ICON),
        ]
        mocked.assert_has_calls(calls, any_order=True)

    @pytest.mark.parametrize(
        "args",
        [
            [(0, "foo", constants.BLANK_ICON)],
            [(0, "foo", constants.BLANK_ICON), (1, "bar", constants.BLANK_ICON)],
            [
                (0, "foo", constants.BLANK_ICON),
                (1, "bar", constants.BLANK_ICON),
                (2, "foobar", constants.BLANK_ICON),
            ],
            [
                (0, "foo", constants.BLANK_ICON),
                (1, "bar", constants.BLANK_ICON),
                (2, "foobar", constants.BLANK_ICON),
                (3, "barfoo", constants.BLANK_ICON),
            ],
            [
                (0, "foo", constants.BLANK_ICON),
                (1, "bar", constants.BLANK_ICON),
                (2, "foobar", constants.BLANK_ICON),
                (3, "barfoo", constants.BLANK_ICON),
                (4, "", constants.BLANK_ICON),
            ],
        ],
    )
    def test_WindowsList_add_windows_calls_place_widget_on_position(self, mocker, args):
        parent = mocker.MagicMock()
        windows = WindowsList(parent=parent)
        mocked = mocker.patch("arrangeit.view.WindowsList.place_widget_on_position")
        window = mocker.patch("arrangeit.view.ListedWindow")
        windows.add_windows(args)
        assert mocked.call_count == len(args)
        calls = []
        for current in range(len(args)):
            calls.append(mocker.call(window.return_value, current))
        mocked.assert_has_calls(calls, any_order=True)

    ## WindowsList.place_widget_on_position
    def test_WindowsList_place_widget_on_position_calls_place_on_frame(self, mocker):
        parent = mocker.MagicMock()
        windows = WindowsList(parent=parent)
        mocked = mocker.MagicMock()
        windows.place_widget_on_position(mocked, 0)
        calls = [
            mocker.call(
                relheight=constants.LISTED_WINDOW_RELHEIGHT,
                relwidth=1.0,
                relx=0.0,
                rely=0,
            )
        ]
        mocked.place.assert_has_calls(calls, any_order=True)
        windows.place_widget_on_position(mocked, 4)
        calls = [
            mocker.call(
                relheight=constants.LISTED_WINDOW_RELHEIGHT,
                relwidth=1.0,
                relx=0.0,
                rely=4 * constants.LISTED_WINDOW_RELHEIGHT,
            )
        ]
        mocked.place.assert_has_calls(calls, any_order=True)

    ## WindowsList.place_children
    def test_WindowsList_place_children_calls_place_widget_on_position(self, mocker):
        windows = WindowsList(parent=mocker.MagicMock())
        mocked = mocker.patch("arrangeit.view.WindowsList.place_widget_on_position")
        widget0 = mocker.MagicMock()
        widget1 = mocker.MagicMock()
        widget2 = mocker.MagicMock()
        children = mocker.patch(
            "arrangeit.view.WindowsList.winfo_children",
            return_value=[widget0, widget1, widget2],
        )
        windows.place_children()
        assert children.call_count == 1
        assert mocked.call_count == 3
        calls = [
            mocker.call(widget0, 0),
            mocker.call(widget1, 1),
            mocker.call(widget2, 2),
        ]
        mocked.assert_has_calls(calls, any_order=True)


class TestWorkspace(object):
    """Unit testing class for Workspace class."""

    ## Workspace
    def test_Workspace_issubclass_of_Frame(self):
        assert issubclass(Workspace, tk.Frame)

    ## Workspace.__init__
    def test_Workspace_init_calls_super_with_parent_arg(self, mocker):
        parent = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.tk.Frame.__init__")
        with pytest.raises(AttributeError):
            Workspace(parent=parent)
        mocked.assert_called_with(parent)

    @pytest.mark.parametrize("attr", ["parent", "number", "name"])
    def test_Workspace_init_sets_attributes(self, mocker, attr):
        mocked = mocker.MagicMock()
        kwargs = {attr: mocked}
        workspace = Workspace(**kwargs)
        assert getattr(workspace, attr) == mocked

    def test_Workspace_init_calls_setup_widgets(self, mocker):
        parent = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.Workspace.setup_widgets")
        Workspace(parent=parent)
        mocked.assert_called_once()

    ## Workspace.get_humanized_number
    @pytest.mark.parametrize("number", [1002, 2007, 5, 0])
    def test_Workspace_get_humanized_number(self, mocker, number):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        workspace = Workspace(mocker.MagicMock(), number=number)
        returned = workspace.get_humanized_number(number)
        assert isinstance(returned, str)
        assert returned == str(number % 1000 + 1)

    ## Workspace.setup_widgets
    def test_Workspace_setup_widgets_calls_get_humanized_number(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocked = mocker.patch("arrangeit.view.Workspace.get_humanized_number")
        window = Workspace(mocker.MagicMock(), number=1002)
        mocked.call_count = 0
        window.setup_widgets()
        assert mocked.call_count == 1
        calls = [mocker.call(1002)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Workspace_setup_widgets_sets_number_label(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        window = Workspace(mocker.MagicMock(), number=0)
        window.setup_widgets()
        calls = [
            mocker.call(
                window,
                text="1",
                font=(
                    "TkDefaultFont",
                    increased_by_fraction(
                        nametofont("TkDefaultFont")["size"],
                        constants.WORKSPACE_NUMBER_FONT_INCREASE,
                    ),
                ),
                foreground=constants.WORKSPACE_NUMBER_LABEL_FG,
                background=constants.WORKSPACE_NUMBER_LABEL_BG,
                anchor=constants.WORKSPACE_NUMBER_LABEL_ANCHOR,
                padx=constants.WORKSPACE_NUMBER_LABEL_PADX,
                pady=constants.WORKSPACE_NUMBER_LABEL_PADY,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Workspace_setup_widgets_sets_name_label(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        window = Workspace(mocker.MagicMock(), name="foo name")
        window.setup_widgets()
        calls = [
            mocker.call(
                window,
                text="foo name",
                font=(
                    "TkDefaultFont",
                    increased_by_fraction(
                        nametofont("TkDefaultFont")["size"],
                        constants.WORKSPACE_NAME_FONT_INCREASE,
                    ),
                ),
                height=constants.WORKSPACE_NAME_LABEL_HEIGHT,
                foreground=constants.WORKSPACE_NAME_LABEL_FG,
                background=constants.WORKSPACE_NAME_LABEL_BG,
                anchor=constants.WORKSPACE_NAME_LABEL_ANCHOR,
                padx=constants.WORKSPACE_NAME_LABEL_PADX,
                pady=constants.WORKSPACE_NAME_LABEL_PADY,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Workspace_setup_widgets_calls_label_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label.place")
        window = Workspace(None, mocker.MagicMock())
        mocked.call_count = 0
        window.setup_widgets()
        assert mocked.call_count == 2
        calls = [
            mocker.call(
                relheight=constants.WORKSPACE_NUMBER_RELHEIGHT,
                relwidth=constants.WORKSPACE_NUMBER_RELWIDTH,
            ),
            mocker.call(
                rely=constants.WORKSPACE_NUMBER_RELHEIGHT,
                relheight=constants.WORKSPACE_NAME_RELHEIGHT,
                relwidth=constants.WORKSPACE_NAME_RELWIDTH,
            ),
        ]
        mocked.assert_has_calls(calls, any_order=True)


class TestListedWindow(object):
    """Unit testing class for Workspace class."""

    ## ListedWindow
    def test_ListedWindow_issubclass_of_Frame(self):
        assert issubclass(ListedWindow, tk.Frame)

    ## ListedWindow.__init__
    def test_ListedWindow_init_calls_super_with_parent_arg(self, mocker):
        parent = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.tk.Frame.__init__")
        with pytest.raises(AttributeError):
            ListedWindow(parent=parent)
        mocked.assert_called_with(parent)

    @pytest.mark.parametrize("attr", ["parent", "wid", "title"])
    def test_ListedWindow_init_sets_attributes(self, mocker, attr):
        mocked = mocker.MagicMock()
        kwargs = {attr: mocked}
        window = ListedWindow(**kwargs)
        assert getattr(window, attr) == mocked

    def test_ListedWindow_init_calls_get_icon_image(self, mocker):
        parent = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.ListedWindow.get_icon_image")
        ListedWindow(parent=parent)
        mocked.assert_called_once()

    def test_ListedWindow_init_calls_setup_widgets(self, mocker):
        parent = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.ListedWindow.setup_widgets")
        ListedWindow(parent=parent)
        mocked.assert_called_once()

    ## ListedWindow.get_icon_image
    def test_ListedWindow_get_icon_image_calls_ImageTk_PhotoImage(self, mocker):
        parent = mocker.MagicMock()
        mocker.patch("arrangeit.view.ListedWindow.setup_widgets")
        mocked = mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        window = ListedWindow(parent=parent)
        mocked.call_count = 0
        window.get_icon_image(constants.BLANK_ICON)
        mocked.assert_called_once()

    ## ListedWindow.setup_widgets
    def test_ListedWindow_setup_widgets_sets_title_label(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        window = ListedWindow(mocker.MagicMock(), title="foo")
        window.setup_widgets()
        calls = [
            mocker.call(
                window,
                text="foo",
                font=(
                    "TkDefaultFont",
                    increased_by_fraction(
                        nametofont("TkDefaultFont")["size"],
                        constants.LISTED_WINDOW_NAME_FONT_INCREASE,
                    ),
                ),
                foreground=constants.LISTED_WINDOW_LABEL_FG,
                background=constants.LISTED_WINDOW_LABEL_BG,
                anchor=constants.LISTED_WINDOW_LABEL_ANCHOR,
                padx=constants.LISTED_WINDOW_LABEL_PADX,
                pady=constants.LISTED_WINDOW_LABEL_PADY,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_ListedWindow_setup_widgets_sets_icon_label(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocked_icon = mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        mocked = mocker.patch("arrangeit.view.tk.Label")
        window = ListedWindow(mocker.MagicMock(), icon=constants.BLANK_ICON)
        window.setup_widgets()
        calls = [
            mocker.call(
                window,
                image=mocked_icon.return_value,
                background=constants.LISTED_ICON_LABEL_BG,
                anchor=constants.LISTED_ICON_LABEL_ANCHOR,
                padx=constants.LISTED_ICON_LABEL_PADX,
                pady=constants.LISTED_ICON_LABEL_PADY,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_ListedWindow_setup_widgets_calls_label_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label.place")
        window = ListedWindow(None, mocker.MagicMock())
        mocked.call_count = 0
        window.setup_widgets()
        assert mocked.call_count == 2
        calls = [
            mocker.call(
                x=constants.ICON_WIDTH / 2 + constants.LISTED_ICON_LABEL_PADX,
                relheight=1.0,
                relwidth=constants.LISTED_WINDOW_RELWIDTH,
            ),
            mocker.call(
                x=constants.LISTED_ICON_LABEL_PADX / 2,
                rely=0.5,
                relheight=1.0,
                anchor=constants.LISTED_ICON_LABEL_ANCHOR,
            ),
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_ListedWindow_setup_widgets_calls_config_background(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Frame.config")
        window = ListedWindow(None, mocker.MagicMock())
        mocked.call_count = 0
        window.setup_widgets()
        assert mocked.call_count == 1
        calls = [mocker.call(background=constants.LISTED_WINDOW_LABEL_BG)]
        mocked.assert_has_calls(calls, any_order=True)

