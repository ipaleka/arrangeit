import tkinter as tk
from tkinter.font import nametofont
from gettext import gettext as _

import pytest

from arrangeit.view import (
    click_left,
    get_tkinter_root,
    get_screenshot_widget,
    get_mouse_listener,
    move_cursor,
    WorkspacesCollection,
    WindowsList,
    Workspace,
    ListedWindow,
    Toolbar,
    Options,
)
from arrangeit.settings import Settings
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

    ## get_screenshot_widget
    def test_get_screenshot_widget_initializes_Label(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        get_screenshot_widget(mocker.MagicMock())
        mocked.assert_called()

    def test_get_screenshot_widget_calls_label_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label.place")
        get_screenshot_widget(mocker.MagicMock())
        mocked.assert_called()
        mocked.assert_called_with(
            x=Settings.SCREENSHOT_SHIFT_PIXELS, y=Settings.SCREENSHOT_SHIFT_PIXELS
        )

    def test_get_screenshot_widget_returns_label_instance(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        assert get_screenshot_widget(mocker.MagicMock()) == mocked.return_value

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


class TestWorkspacesCollection(object):
    """Unit testing class for :class:`WorkspacesCollection` class."""

    ## WorkspacesCollection
    def test_WorkspacesCollection_issubclass_of_Frame(self):
        assert issubclass(WorkspacesCollection, tk.Frame)

    @pytest.mark.parametrize("attr", ["master", "active"])
    def test_WorkspacesCollection_inits_attr_as_None(self, attr):
        assert getattr(WorkspacesCollection, attr) is None

    ## WorkspacesCollection.__init__
    def test_WorkspacesCollection_init_calls_super_with_master_arg(self, mocker):
        mocker.patch("arrangeit.view.tk.Frame.config")
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.tk.Frame.__init__")
        WorkspacesCollection(master=master)
        mocked.assert_called_with(master)

    def test_WorkspacesCollection_init_sets_master_attribute(self, mocker):
        master = mocker.MagicMock()
        workspaces = WorkspacesCollection(master)
        assert workspaces.master == master

    def test_WorkspacesCollection_init_calls_config_background(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Frame.config")
        master = mocker.MagicMock()
        WorkspacesCollection(master)
        assert mocked.call_count == 1
        calls = [mocker.call(background=Settings.WORKSPACE_NUMBER_LABEL_BG)]
        mocked.assert_has_calls(calls, any_order=True)

    ## WorkspacesCollection.add_workspaces
    def test_WorkspacesCollection_add_workspaces_initializes_Workspace(self, mocker):
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.Workspace")
        workspaces = WorkspacesCollection(master=master)
        args = [(0, "foo"), (1, "bar")]
        workspaces.add_workspaces(args)
        assert mocked.call_count == 2
        calls = [
            mocker.call(workspaces, number=0, name="foo"),
            mocker.call(workspaces, number=1, name="bar"),
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_WorkspacesCollection_add_workspaces_not_calling_place(self, mocker):
        master = mocker.MagicMock()
        mocker.patch("arrangeit.view.Workspace")
        workspaces = WorkspacesCollection(master=master)
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
        master = mocker.MagicMock()
        mocker.patch("arrangeit.view.Workspace")
        workspaces = WorkspacesCollection(master=master)
        mocked = mocker.patch("arrangeit.view.Workspace")
        workspaces.add_workspaces(args)
        assert mocked.return_value.place.call_count == len(args)
        relheight = 0.5 if len(args) < 5 else float(1 / ((len(args) - 1) // 2 + 1))
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
        mocker.patch(
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
        calls = [mocker.call(foreground=Settings.WORKSPACE_NUMBER_LABEL_FG)]
        widget0.number_label.config.assert_has_calls(calls, any_order=True)
        widget2.number_label.config.assert_has_calls(calls, any_order=True)
        calls = [mocker.call(foreground=Settings.WORKSPACE_NAME_LABEL_FG)]
        widget0.name_label.config.assert_has_calls(calls, any_order=True)
        widget2.name_label.config.assert_has_calls(calls, any_order=True)
        calls = [mocker.call(foreground=Settings.SELECTED_COLOR)]
        widget1.number_label.config.assert_has_calls(calls, any_order=True)
        widget1.name_label.config.assert_has_calls(calls, any_order=True)

    def test_WorkspacesCollection_select_active_calls_cursor_config(self, mocker):
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
        calls = [mocker.call(cursor=Settings.SELECT_CURSOR)]
        widget0.config.assert_has_calls(calls, any_order=True)
        widget2.config.assert_has_calls(calls, any_order=True)
        calls = [mocker.call(cursor=Settings.DEFAULT_CURSOR)]
        widget1.config.assert_has_calls(calls, any_order=True)

    def test_WorkspacesCollection_select_active_sets_active_attr(self, mocker):
        workspaces = WorkspacesCollection()
        mocker.patch(
            "arrangeit.view.WorkspacesCollection.winfo_children",
            return_value=[mocker.MagicMock(), mocker.MagicMock()],
        )
        workspaces.select_active(1000)
        assert workspaces.active == 1000

    ## WorkspacesCollection.on_workspace_label_button_down
    def test_WorkspacesCollection_on_workspace_label_button_down_calls_workspace_active(
        self, mocker
    ):
        master = mocker.MagicMock()
        workspaces = WorkspacesCollection(master=master)
        event = mocker.MagicMock()
        type(event.widget.master).number = mocker.PropertyMock(return_value=1002)
        workspaces.on_workspace_label_button_down(event)
        master.controller.workspace_activated.assert_called_with(1002)

    def test_WorkspacesCollection_on_workspace_label_button_returns_break(self, mocker):
        workspaces = WorkspacesCollection(mocker.MagicMock())
        returned = workspaces.on_workspace_label_button_down(mocker.MagicMock())
        assert returned == "break"


class TestWindowsList(object):
    """Unit testing class for :class:`WindowsList` class."""

    ## WindowsList
    def test_WindowsList_issubclass_of_Frame(self):
        assert issubclass(WindowsList, tk.Frame)

    @pytest.mark.parametrize("attr", ["master"])
    def test_WindowsList_inits_attr_as_None(self, attr):
        assert getattr(WindowsList, attr) is None

    ## WindowsList.__init__
    def test_WindowsList_init_calls_super_with_master_arg(self, mocker):
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.tk.Frame.__init__")
        WindowsList(master=master)
        mocked.assert_called_with(master)

    def test_WindowsList_init_sets_master_attribute(self, mocker):
        master = mocker.MagicMock()
        windows = WindowsList(master)
        assert windows.master == master

    ## WindowsList.add_windows
    def test_WindowsList_add_windows_initializes_ListedWindow(self, mocker):
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.ListedWindow")
        windows = WindowsList(master=master)
        windows_list = [
            (100, "foo", Settings.BLANK_ICON),
            (200, "bar", Settings.BLANK_ICON),
        ]
        windows.add_windows(windows_list)
        assert mocked.call_count == 2
        calls = [
            mocker.call(windows, wid=100, title="foo", icon=Settings.BLANK_ICON),
            mocker.call(windows, wid=200, title="bar", icon=Settings.BLANK_ICON),
        ]
        mocked.assert_has_calls(calls, any_order=True)

    @pytest.mark.parametrize(
        "args",
        [
            [(0, "foo", Settings.BLANK_ICON)],
            [(0, "foo", Settings.BLANK_ICON), (1, "bar", Settings.BLANK_ICON)],
            [
                (0, "foo", Settings.BLANK_ICON),
                (1, "bar", Settings.BLANK_ICON),
                (2, "foobar", Settings.BLANK_ICON),
            ],
            [
                (0, "foo", Settings.BLANK_ICON),
                (1, "bar", Settings.BLANK_ICON),
                (2, "foobar", Settings.BLANK_ICON),
                (3, "barfoo", Settings.BLANK_ICON),
            ],
            [
                (0, "foo", Settings.BLANK_ICON),
                (1, "bar", Settings.BLANK_ICON),
                (2, "foobar", Settings.BLANK_ICON),
                (3, "barfoo", Settings.BLANK_ICON),
                (4, "", Settings.BLANK_ICON),
            ],
        ],
    )
    def test_WindowsList_add_windows_calls_place_widget_on_position(self, mocker, args):
        master = mocker.MagicMock()
        windows = WindowsList(master=master)
        mocked = mocker.patch("arrangeit.view.WindowsList.place_widget_on_position")
        window = mocker.patch("arrangeit.view.ListedWindow")
        windows.add_windows(args)
        assert mocked.call_count == len(args)
        calls = []
        for current in range(len(args)):
            calls.append(mocker.call(window.return_value, current))
        mocked.assert_has_calls(calls, any_order=True)

    ## WindowsList.clear_list
    def test_WindowsList_clear_list_calls_winfo_children(self, mocker):
        mocked = mocker.patch(
            "arrangeit.view.WindowsList.winfo_children",
            return_value=[mocker.MagicMock()],
        )
        windows = WindowsList()
        windows.clear_list()
        mocked.assert_called_once()

    def test_WindowsList_clear_list_calls_widget_destroy(self, mocker):
        widget1 = mocker.MagicMock()
        widget2 = mocker.MagicMock()
        mocker.patch(
            "arrangeit.view.WindowsList.winfo_children", return_value=[widget1, widget2]
        )
        windows = WindowsList()
        windows.clear_list()
        widget1.destroy.assert_called_once()
        widget2.destroy.assert_called_once()

    ## WindowsList.place_widget_on_position
    def test_WindowsList_place_widget_on_position_calls_place_on_frame(self, mocker):
        master = mocker.MagicMock()
        windows = WindowsList(master=master)
        mocked = mocker.MagicMock()
        windows.place_widget_on_position(mocked, 0)
        calls = [
            mocker.call(
                relheight=Settings.LISTED_WINDOW_RELHEIGHT,
                relwidth=1.0,
                relx=0.0,
                rely=0,
            )
        ]
        mocked.place.assert_has_calls(calls, any_order=True)
        windows.place_widget_on_position(mocked, 4)
        calls = [
            mocker.call(
                relheight=Settings.LISTED_WINDOW_RELHEIGHT,
                relwidth=1.0,
                relx=0.0,
                rely=4 * Settings.LISTED_WINDOW_RELHEIGHT,
            )
        ]
        mocked.place.assert_has_calls(calls, any_order=True)

    ## WindowsList.place_children
    def test_WindowsList_place_children_calls_place_widget_on_position(self, mocker):
        windows = WindowsList(master=mocker.MagicMock())
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

    ## WindowsList.on_window_label_button_down
    def test_WindowsList_on_window_label_button_down_calls_listed_window_activated(
        self, mocker
    ):
        master = mocker.MagicMock()
        windows = WindowsList(master=master)
        event = mocker.MagicMock()
        type(event.widget.master).wid = mocker.PropertyMock(return_value=5432)
        windows.on_window_label_button_down(event)
        master.controller.listed_window_activated.assert_called_with(5432)

    def test_WindowsList_on_window_label_button_returns_break(self, mocker):
        windows = WindowsList(mocker.MagicMock())
        returned = windows.on_window_label_button_down(mocker.MagicMock())
        assert returned == "break"


class TestWorkspace(object):
    """Unit testing class for :class:`Workspace` class."""

    ## Workspace
    def test_Workspace_issubclass_of_Frame(self):
        assert issubclass(Workspace, tk.Frame)

    @pytest.mark.parametrize(
        "attr,value", [("master", None), ("number", 0), ("name", "")]
    )
    def test_Workspace_inits_attr_as_empty(self, attr, value):
        assert getattr(Workspace, attr) == value

    ## Workspace.__init__
    def test_Workspace_init_calls_super_with_master_arg(self, mocker):
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.tk.Frame.__init__")
        with pytest.raises(AttributeError):
            Workspace(master=master)
        mocked.assert_called_with(master)

    @pytest.mark.parametrize("attr", ["master", "number", "name"])
    def test_Workspace_init_sets_attributes(self, mocker, attr):
        mocker.patch("arrangeit.view.Workspace.setup_bindings")
        mocker.patch("arrangeit.view.Workspace.setup_widgets")
        mocked = mocker.MagicMock()
        kwargs = {attr: mocked}
        workspace = Workspace(**kwargs)
        assert getattr(workspace, attr) == mocked

    def test_Workspace_init_calls_setup_widgets(self, mocker):
        master = mocker.MagicMock()
        mocker.patch("arrangeit.view.Workspace.setup_bindings")
        mocked = mocker.patch("arrangeit.view.Workspace.setup_widgets")
        Workspace(master=master)
        mocked.assert_called_once()

    def test_Workspace_init_calls_setup_bindings(self, mocker):
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.Workspace.setup_bindings")
        Workspace(master=master)
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
        workspace = Workspace(mocker.MagicMock(), number=1002)
        mocked.call_count = 0
        workspace.setup_widgets()
        assert mocked.call_count == 1
        calls = [mocker.call(1002)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Workspace_setup_widgets_sets_number_label(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        workspace = Workspace(mocker.MagicMock(), number=0)
        workspace.setup_widgets()
        calls = [
            mocker.call(
                workspace,
                text="1",
                font=(
                    "TkDefaultFont",
                    increased_by_fraction(
                        nametofont("TkDefaultFont")["size"],
                        Settings.WORKSPACE_NUMBER_FONT_INCREASE,
                    ),
                ),
                foreground=Settings.WORKSPACE_NUMBER_LABEL_FG,
                background=Settings.WORKSPACE_NUMBER_LABEL_BG,
                anchor=Settings.WORKSPACE_NUMBER_LABEL_ANCHOR,
                padx=Settings.WORKSPACE_NUMBER_LABEL_PADX,
                pady=Settings.WORKSPACE_NUMBER_LABEL_PADY,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Workspace_setup_widgets_sets_name_label(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        workspace = Workspace(mocker.MagicMock(), name="foo name")
        workspace.setup_widgets()
        calls = [
            mocker.call(
                workspace,
                text="foo name",
                font=(
                    "TkDefaultFont",
                    increased_by_fraction(
                        nametofont("TkDefaultFont")["size"],
                        Settings.WORKSPACE_NAME_FONT_INCREASE,
                    ),
                ),
                height=Settings.WORKSPACE_NAME_LABEL_HEIGHT,
                foreground=Settings.WORKSPACE_NAME_LABEL_FG,
                background=Settings.WORKSPACE_NAME_LABEL_BG,
                anchor=Settings.WORKSPACE_NAME_LABEL_ANCHOR,
                padx=Settings.WORKSPACE_NAME_LABEL_PADX,
                pady=Settings.WORKSPACE_NAME_LABEL_PADY,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Workspace_setup_widgets_calls_label_place(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocker.patch("arrangeit.view.tk.Label.config")
        mocked = mocker.patch("arrangeit.view.tk.Label.place")
        workspace = Workspace(mocker.MagicMock(), mocker.MagicMock())
        mocked.call_count = 0
        workspace.setup_widgets()
        assert mocked.call_count == 2
        calls = [
            mocker.call(
                relheight=Settings.WORKSPACE_NUMBER_RELHEIGHT,
                relwidth=Settings.WORKSPACE_NUMBER_RELWIDTH,
            ),
            mocker.call(
                rely=Settings.WORKSPACE_NUMBER_RELHEIGHT,
                relheight=Settings.WORKSPACE_NAME_RELHEIGHT,
                relwidth=Settings.WORKSPACE_NAME_RELWIDTH,
            ),
        ]
        mocked.assert_has_calls(calls, any_order=True)

    ## Workspace.setup_bindings
    @pytest.mark.parametrize(
        "event,method", [("<Enter>", "on_widget_enter"), ("<Leave>", "on_widget_leave")]
    )
    def test_Workspace_setup_bindings_callbacks(self, mocker, event, method):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocker.patch("arrangeit.view.tk.Label.config")
        workspace = Workspace(mocker.MagicMock())
        callback = getattr(workspace, method)
        mocked = mocker.patch("arrangeit.view.Workspace.bind")
        workspace.setup_bindings()
        calls = [mocker.call(event, callback)]
        mocked.assert_has_calls(calls, any_order=True)

    @pytest.mark.parametrize(
        "event,method", [("<Button-1>", "on_workspace_label_button_down")]
    )
    def test_Workspace_setup_bindings_labels_master_callbacks(
        self, mocker, event, method
    ):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocker.patch("arrangeit.view.tk.Label.config")
        workspace = Workspace(mocker.MagicMock())
        callback = getattr(workspace.master, method)
        mocked = mocker.patch("arrangeit.view.tk.Label.bind")
        workspace.setup_bindings()
        calls = [mocker.call(event, callback), mocker.call(event, callback)]
        mocked.assert_has_calls(calls, any_order=True)

    ## Workspace.on_widget_enter
    def test_Workspace_on_widget_enter_sets_foreground(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocked = mocker.patch("arrangeit.view.tk.Label.config")
        workspace = Workspace(mocker.MagicMock())
        workspace.on_widget_enter(mocker.MagicMock())
        assert mocked.call_count == 2
        calls = [mocker.call(foreground=Settings.HIGHLIGHTED_COLOR)] * 2
        mocked.assert_has_calls(calls, any_order=True)

    def test_Workspace_on_widget_enter_not_setting_foreground_for_active(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocked = mocker.patch("arrangeit.view.tk.Label.config")
        master = mocker.MagicMock()
        type(master).active = mocker.PropertyMock(return_value=1000)
        workspace = Workspace(master, number=1000)
        workspace.on_widget_enter(mocker.MagicMock())
        assert mocked.call_count == 0

    def test_Workspace_on_widget_enter_returns_break(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocker.patch("arrangeit.view.tk.Label.config")
        workspace = Workspace(mocker.MagicMock())
        returned = workspace.on_widget_enter(mocker.MagicMock())
        assert returned == "break"

    ## Workspace.on_widget_leave
    def test_Workspace_on_widget_leave_sets_foreground(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocked = mocker.patch("arrangeit.view.tk.Label.config")
        workspace = Workspace(mocker.MagicMock())
        workspace.on_widget_leave(mocker.MagicMock())
        assert mocked.call_count == 2
        calls = [mocker.call(foreground=Settings.WORKSPACE_NUMBER_LABEL_FG)] * 2
        mocked.assert_has_calls(calls, any_order=True)

    def test_Workspace_on_widget_leave_not_setting_foreground_for_active(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocked = mocker.patch("arrangeit.view.tk.Label.config")
        master = mocker.MagicMock()
        type(master).active = mocker.PropertyMock(return_value=1000)
        workspace = Workspace(master, number=1000)
        workspace.on_widget_leave(mocker.MagicMock())
        assert mocked.call_count == 0

    def test_Workspace_on_widget_leave_returns_break(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocker.patch("arrangeit.view.tk.Label.config")
        workspace = Workspace(mocker.MagicMock())
        returned = workspace.on_widget_leave(mocker.MagicMock())
        assert returned == "break"


class TestListedWindow(object):
    """Unit testing class for :class:`ListedWindow` class."""

    ## ListedWindow
    def test_ListedWindow_issubclass_of_Frame(self):
        assert issubclass(ListedWindow, tk.Frame)

    @pytest.mark.parametrize(
        "attr,value",
        [("master", None), ("wid", 0), ("title", ""), ("icon", Settings.BLANK_ICON)],
    )
    def test_ListedWindow_inits_attr_as_empty(self, attr, value):
        assert getattr(ListedWindow, attr) == value

    ## ListedWindow.__init__
    def test_ListedWindow_init_calls_super_with_master_and_cursor_arg(self, mocker):
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.tk.Frame.__init__")
        with pytest.raises(AttributeError):
            ListedWindow(master=master)
        mocked.assert_called_with(master, cursor=Settings.SELECT_CURSOR)

    @pytest.mark.parametrize("attr", ["master", "wid", "title"])
    def test_ListedWindow_init_sets_attributes(self, mocker, attr):
        mocker.patch("arrangeit.view.ListedWindow.setup_bindings")
        mocker.patch("arrangeit.view.ListedWindow.setup_widgets")
        mocked = mocker.MagicMock()
        kwargs = {attr: mocked}
        window = ListedWindow(**kwargs)
        assert getattr(window, attr) == mocked

    def test_ListedWindow_init_calls_get_icon_image(self, mocker):
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.ListedWindow.get_icon_image")
        ListedWindow(master=master)
        mocked.assert_called_once()

    def test_ListedWindow_init_calls_setup_widgets(self, mocker):
        master = mocker.MagicMock()
        mocker.patch("arrangeit.view.ListedWindow.setup_bindings")
        mocked = mocker.patch("arrangeit.view.ListedWindow.setup_widgets")
        ListedWindow(master=master)
        mocked.assert_called_once()

    def test_ListedWindow_init_calls_setup_bindings(self, mocker):
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.ListedWindow.setup_bindings")
        ListedWindow(master=master)
        mocked.assert_called_once()

    ## ListedWindow.get_icon_image
    def test_ListedWindow_get_icon_image_calls_ImageTk_PhotoImage(self, mocker):
        mocker.patch("arrangeit.view.ListedWindow.setup_bindings")
        master = mocker.MagicMock()
        mocker.patch("arrangeit.view.ListedWindow.setup_widgets")
        mocked = mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        window = ListedWindow(master=master)
        mocked.call_count = 0
        window.get_icon_image(Settings.BLANK_ICON)
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
                        Settings.LISTED_WINDOW_NAME_FONT_INCREASE,
                    ),
                ),
                foreground=Settings.LISTED_WINDOW_LABEL_FG,
                background=Settings.LISTED_WINDOW_LABEL_BG,
                anchor=Settings.LISTED_WINDOW_LABEL_ANCHOR,
                padx=Settings.LISTED_WINDOW_LABEL_PADX,
                pady=Settings.LISTED_WINDOW_LABEL_PADY,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_ListedWindow_setup_widgets_sets_icon_label(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocked_icon = mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        mocked = mocker.patch("arrangeit.view.tk.Label")
        window = ListedWindow(mocker.MagicMock(), icon=Settings.BLANK_ICON)
        window.setup_widgets()
        calls = [
            mocker.call(
                window,
                image=mocked_icon.return_value,
                background=Settings.LISTED_ICON_LABEL_BG,
                anchor=Settings.LISTED_ICON_LABEL_ANCHOR,
                padx=Settings.LISTED_ICON_LABEL_PADX,
                pady=Settings.LISTED_ICON_LABEL_PADY,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_ListedWindow_setup_widgets_calls_label_place(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocker.patch("arrangeit.view.tk.Label.config")
        mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        mocked = mocker.patch("arrangeit.view.tk.Label.place")
        window = ListedWindow(mocker.MagicMock(), mocker.MagicMock())
        mocked.call_count = 0
        window.setup_widgets()
        assert mocked.call_count == 2
        calls = [
            mocker.call(
                x=Settings.ICON_WIDTH / 2 + Settings.LISTED_ICON_LABEL_PADX,
                relheight=1.0,
                relwidth=Settings.LISTED_WINDOW_RELWIDTH,
            ),
            mocker.call(
                x=Settings.LISTED_ICON_LABEL_PADX / 2,
                rely=0.5,
                relheight=1.0,
                anchor=Settings.LISTED_ICON_LABEL_ANCHOR,
            ),
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_ListedWindow_setup_widgets_calls_config_background(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocker.patch("arrangeit.view.tk.Label.config")
        mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        mocked = mocker.patch("arrangeit.view.tk.Frame.config")
        window = ListedWindow(mocker.MagicMock(), mocker.MagicMock())
        mocked.call_count = 0
        window.setup_widgets()
        assert mocked.call_count == 1
        calls = [mocker.call(background=Settings.LISTED_WINDOW_LABEL_BG)]
        mocked.assert_has_calls(calls, any_order=True)

    ## ListedWindow.setup_bindings
    @pytest.mark.parametrize(
        "event,method", [("<Enter>", "on_widget_enter"), ("<Leave>", "on_widget_leave")]
    )
    def test_ListedWindow_setup_bindings_callbacks(self, mocker, event, method):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocker.patch("arrangeit.view.tk.Label.config")
        mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        window = ListedWindow(mocker.MagicMock())
        callback = getattr(window, method)
        mocked = mocker.patch("arrangeit.view.ListedWindow.bind")
        window.setup_bindings()
        calls = [mocker.call(event, callback)]
        mocked.assert_has_calls(calls, any_order=True)

    @pytest.mark.parametrize(
        "event,method", [("<Button-1>", "on_window_label_button_down")]
    )
    def test_ListedWindow_setup_bindings_labels_master_callbacks(
        self, mocker, event, method
    ):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocker.patch("arrangeit.view.tk.Label.config")
        mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        window = ListedWindow(mocker.MagicMock())
        callback = getattr(window.master, method)
        mocked = mocker.patch("arrangeit.view.tk.Label.bind")
        window.setup_bindings()
        calls = [mocker.call(event, callback), mocker.call(event, callback)]
        mocked.assert_has_calls(calls, any_order=True)

    ## ListedWindow.on_widget_enter
    def test_ListedWindow_on_widget_enter_sets_foreground(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        mocked = mocker.patch("arrangeit.view.tk.Label.config")
        window = ListedWindow(mocker.MagicMock())
        window.on_widget_enter(mocker.MagicMock())
        assert mocked.call_count == 1
        calls = [mocker.call(foreground=Settings.HIGHLIGHTED_COLOR)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_ListedWindow_on_widget_enter_returns_break(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        window = ListedWindow(mocker.MagicMock())
        returned = window.on_widget_enter(mocker.MagicMock())
        assert returned == "break"

    ## ListedWindow.on_widget_leave
    def test_ListedWindow_on_widget_leave_sets_foreground(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        mocked = mocker.patch("arrangeit.view.tk.Label.config")
        window = ListedWindow(mocker.MagicMock())
        window.on_widget_leave(mocker.MagicMock())
        assert mocked.call_count == 1
        calls = [mocker.call(foreground=Settings.LISTED_WINDOW_LABEL_FG)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_ListedWindow_on_widget_leave_returns_break(self, mocker):
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        window = ListedWindow(mocker.MagicMock())
        returned = window.on_widget_leave(mocker.MagicMock())
        assert returned == "break"


class TestToolbar(object):
    """Unit testing class for :class:`Toolbar` class."""

    ## Toolbar
    def test_Toolbar_issubclass_of_Frame(self):
        assert issubclass(Toolbar, tk.Frame)

    @pytest.mark.parametrize("attr,value", [("master", None)])
    def test_Toolbar_inits_attributtes(self, attr, value):
        assert getattr(Toolbar, attr) == value

    ## Toolbar.__init__
    def test_Toolbar_init_calls_super_with_master_arg(self, mocker):
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.tk.Frame.__init__")
        with pytest.raises(AttributeError):
            Toolbar(master=master)
        mocked.assert_called_with(master)

    @pytest.mark.parametrize("attr", ["master"])
    def test_Toolbar_init_sets_attributes(self, mocker, attr):
        mocker.patch("arrangeit.view.Toolbar.setup_widgets")
        mocked = mocker.MagicMock()
        kwargs = {attr: mocked}
        toolbar = Toolbar(**kwargs)
        assert getattr(toolbar, attr) == mocked

    def test_Toolbar_init_calls_setup_widgets(self, mocker):
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.Toolbar.setup_widgets")
        Toolbar(master=master)
        mocked.assert_called_once()

    ## Toolbar.setup_widgets
    def test_Toolbar_setup_widgets_sets_options_button(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Button")
        master = mocker.MagicMock()
        toolbar = Toolbar(master)
        toolbar.setup_widgets()
        calls = [
            mocker.call(
                toolbar,
                font=(
                    "TkDefaultFont",
                    increased_by_fraction(
                        nametofont("TkDefaultFont")["size"],
                        Settings.TOOLBAR_BUTTON_FONT_INCREASE,
                    ),
                ),
                text=_("Options"),
                activeforeground=Settings.HIGHLIGHTED_COLOR,
                command=toolbar.on_options_click,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Toolbar_setup_widgets_sets_quit_button(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Button")
        master = mocker.MagicMock()
        toolbar = Toolbar(master)
        toolbar.setup_widgets()
        calls = [
            mocker.call(
                toolbar,
                font=(
                    "TkDefaultFont",
                    increased_by_fraction(
                        nametofont("TkDefaultFont")["size"],
                        Settings.TOOLBAR_BUTTON_FONT_INCREASE,
                    ),
                ),
                text=_("Quit"),
                activeforeground=Settings.HIGHLIGHTED_COLOR,
                command=master.controller.shutdown,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Toolbar_setup_widgets_calls_button_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Button.place")
        toolbar = Toolbar(mocker.MagicMock())
        mocked.call_count = 0
        toolbar.setup_widgets()
        assert mocked.call_count == 2
        calls = [
            mocker.call(
                rely=Settings.TOOLBAR_BUTTON_SHRINK_HEIGHT / 2,
                relx=Settings.TOOLBAR_BUTTON_SHRINK_WIDTH / 2,
                relheight=Settings.OPTIONS_BUTTON_RELHEIGHT
                - Settings.TOOLBAR_BUTTON_SHRINK_HEIGHT,
                relwidth=Settings.OPTIONS_BUTTON_RELWIDTH
                - Settings.TOOLBAR_BUTTON_SHRINK_WIDTH,
                anchor=Settings.OPTIONS_BUTTON_ANCHOR,
            ),
            mocker.call(
                rely=Settings.TOOLBAR_BUTTON_SHRINK_HEIGHT / 2,
                relx=0.5 + Settings.TOOLBAR_BUTTON_SHRINK_WIDTH / 2,
                relheight=Settings.QUIT_BUTTON_RELHEIGHT
                - Settings.TOOLBAR_BUTTON_SHRINK_HEIGHT,
                relwidth=Settings.QUIT_BUTTON_RELWIDTH
                - Settings.TOOLBAR_BUTTON_SHRINK_WIDTH,
                anchor=Settings.QUIT_BUTTON_ANCHOR,
            ),
        ]
        mocked.assert_has_calls(calls, any_order=True)


class TestOptions(object):
    """Unit testing class for :class:`Options` class."""

    ## Options
    def test_Options_issubclass_of_Toplevel(self):
        assert issubclass(Options, tk.Toplevel)

    @pytest.mark.parametrize("attr,value", [("master", None)])
    def test_Options_inits_attributtes(self, attr, value):
        assert getattr(Options, attr) == value

    ## Options.__init__
    def test_Options_init_calls_super_with_master_arg(self, mocker):
        master = tk.Frame()
        mocked = mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        # with pytest.raises(AttributeError):
        Options(master=master)
        mocked.assert_called_with(master)

    def test_Options_init_sets_master_attribute(self, mocker):
        mocker.patch("arrangeit.view.Options.setup_widgets")
        master = tk.Frame()
        assert Options(master).master == master

    def test_Options_init_calls_setup_widgets(self, mocker):
        master = tk.Frame()
        mocked = mocker.patch("arrangeit.view.Options.setup_widgets")
        Options(master=master)
        mocked.assert_called_once()
