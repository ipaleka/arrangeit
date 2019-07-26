# arrangeit - cross-platform desktop utility for easy windows management
# Copyright (C) 1999-2019 Ivica Paleka

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>

import tkinter as tk
from tkinter.font import nametofont

import pytest

from arrangeit.data import WindowModel
from arrangeit.settings import Settings
from arrangeit.utils import increased_by_fraction
from arrangeit.view import (
    Resizable,
    Restored,
    Statusbar,
    Toolbar,
    ViewApplication,
    WindowsList,
    WorkspacesCollection,
)


class TestViewApplication(object):
    """Unit testing class for :class:`ViewApplication` class."""

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

    def test_ViewApplication_init_configures_background(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Frame.config")
        ViewApplication(None, mocker.MagicMock())
        mocked.assert_called_with(background=Settings.MAIN_BG)

    def test_ViewApplication_inits_calls_setup_bindings(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_bindings")
        ViewApplication(None, mocker.MagicMock())
        assert mocked.call_count == 1

    def test_ViewApplication_inits_calls_setup_widgets(self, mocker):
        mocker.patch("arrangeit.view.ViewApplication.setup_bindings")
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_widgets")
        ViewApplication(None, mocker.MagicMock())
        assert mocked.call_count == 1

    ## ViewApplication.reset_bindings
    @pytest.mark.parametrize(
        "event", ["<Button-1>", "<Button-2>", "<Button-3>", "<Key>"]
    )
    def test_ViewApplication_reset_bindings_unbind_all(self, mocker, event):
        controller = mocker.MagicMock()
        view = ViewApplication(None, controller)
        mocked = mocker.patch("arrangeit.view.ViewApplication.unbind_all")
        view.reset_bindings()
        calls = [mocker.call(event)]
        mocked.assert_has_calls(calls, any_order=True)

    @pytest.mark.parametrize("event,method", [("<Button-1>", "on_continue")])
    def test_ViewApplication_reset_bindings_labels_bind_callback(
        self, mocker, event, method
    ):
        controller = mocker.MagicMock()
        view = ViewApplication(None, controller)
        callback = getattr(controller, method)
        mocked = mocker.patch("arrangeit.view.tk.Label.bind")
        view.reset_bindings()
        calls = [mocker.call(event, callback)]
        assert mocked.call_count == 2
        mocked.assert_has_calls(calls, any_order=True)

    @pytest.mark.parametrize("event,method", [("<Button-1>", "on_continue")])
    def test_ViewApplication_reset_bindings_windowslist_bind_callback(
        self, mocker, event, method
    ):
        controller = mocker.MagicMock()
        view = ViewApplication(None, controller)
        callback = getattr(controller, method)
        mocked = mocker.patch("arrangeit.view.WindowsList.bind")
        view.reset_bindings()
        calls = [mocker.call(event, callback)]
        assert mocked.call_count == 1
        mocked.assert_has_calls(calls, any_order=True)

    @pytest.mark.parametrize("event,method", [("<Button-1>", "on_continue")])
    def test_ViewApplication_reset_bindings_workspaces_bind_callback(
        self, mocker, event, method
    ):
        controller = mocker.MagicMock()
        view = ViewApplication(None, controller)
        callback = getattr(controller, method)
        mocked = mocker.patch("arrangeit.view.WorkspacesCollection.bind")
        view.reset_bindings()
        calls = [mocker.call(event, callback)]
        assert mocked.call_count == 1
        mocked.assert_has_calls(calls, any_order=True)

    ## ViewApplication.get_root_wid
    def test_ViewApplication_get_root_wid_calls_master_frame(
        self, mocker
    ):
        mocker.patch("arrangeit.view.ViewApplication.setup_widgets")
        mocker.patch("arrangeit.view.ViewApplication.setup_bindings")
        mocker.patch("arrangeit.view.int")
        master = mocker.MagicMock()
        ViewApplication(master, mocker.MagicMock()).get_root_wid()
        master.frame.assert_called_once()
        master.frame.assert_called_with()

    def test_ViewApplication_get_root_wid_calls_int_and_returns_it(
        self, mocker
    ):
        mocker.patch("arrangeit.view.ViewApplication.setup_widgets")
        mocker.patch("arrangeit.view.ViewApplication.setup_bindings")
        mocked = mocker.patch("arrangeit.view.int")
        master = mocker.MagicMock()
        returned = ViewApplication(master, mocker.MagicMock()).get_root_wid()
        mocked.assert_called_once()
        mocked.assert_called_with(master.frame.return_value, 0)
        assert returned == mocked.return_value

    ## ViewApplication.hide_root
    @pytest.mark.parametrize("method", ["withdraw"])
    def test_ViewApplication_hide_root_calls_master_hiding_up_method(
        self, mocker, method
    ):
        mocker.patch("arrangeit.view.ViewApplication.setup_widgets")
        mocker.patch("arrangeit.view.ViewApplication.setup_bindings")
        master = mocker.MagicMock()
        ViewApplication(master, mocker.MagicMock()).hide_root()
        assert getattr(master, method).call_count == 1

    ## ViewApplication.show_root
    @pytest.mark.parametrize("method", ["update", "deiconify"])
    def test_ViewApplication_show_root_calls_master_showing_up_method(
        self, mocker, method
    ):
        mocker.patch("arrangeit.view.ViewApplication.setup_widgets")
        mocker.patch("arrangeit.view.ViewApplication.setup_bindings")
        master = mocker.MagicMock()
        ViewApplication(master, mocker.MagicMock()).show_root()
        assert getattr(master, method).call_count == 1

    ## ViewApplication.setup_bindings
    def test_ViewApplication_setup_bindings_unbinds_all_button_1(self, mocker):
        controller = mocker.MagicMock()
        view = ViewApplication(None, controller)
        mocked = mocker.patch("arrangeit.view.ViewApplication.unbind_all")
        view.setup_bindings()
        calls = [mocker.call("<Button-1>")]
        mocked.assert_has_calls(calls, any_order=True)

    @pytest.mark.parametrize(
        "event,method",
        [
            ("<Button-2>", "on_mouse_middle_down"),
            ("<Button-3>", "on_mouse_right_down"),
            ("<Key>", "on_key_pressed"),
        ],
    )
    def test_ViewApplication_setup_bindings_bind_all_callbacks(
        self, mocker, event, method
    ):
        controller = mocker.MagicMock()
        view = ViewApplication(None, controller)
        callback = getattr(controller, method)
        mocked = mocker.patch("arrangeit.view.ViewApplication.bind_all")
        view.setup_bindings()
        calls = [mocker.call(event, callback)]
        mocked.assert_has_calls(calls, any_order=True)

    @pytest.mark.parametrize(
        "event,method", [("<Button-1>", "on_mouse_left_down"), ("<Enter>", "on_focus")]
    )
    def test_ViewApplication_setup_bindings_bind_callbacks(self, mocker, event, method):
        controller = mocker.MagicMock()
        view = ViewApplication(None, controller)
        callback = getattr(controller, method)
        mocked = mocker.patch("arrangeit.view.ViewApplication.bind")
        view.setup_bindings()
        calls = [mocker.call(event, callback)]
        mocked.assert_has_calls(calls, any_order=True)

    @pytest.mark.parametrize("event,method", [("<Button-1>", "on_mouse_left_down")])
    def test_ViewApplication_setup_bindings_root_bind_callbacks(
        self, mocker, event, method
    ):
        mocker.patch("arrangeit.view.tk.StringVar")
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        controller = mocker.MagicMock()
        master = mocker.MagicMock()
        view = ViewApplication(master, controller)
        callback = getattr(controller, method)
        view.setup_bindings()
        calls = [mocker.call(event, callback)]
        master.bind.assert_has_calls(calls, any_order=True)

    @pytest.mark.parametrize("event,method", [("<Button-1>", "on_mouse_left_down")])
    def test_ViewApplication_setup_bindings_label_bind_callbacks(
        self, mocker, event, method
    ):
        controller = mocker.MagicMock()
        view = ViewApplication(None, controller)
        callback = getattr(controller, method)
        mocked = mocker.patch("arrangeit.view.tk.Label.bind")
        view.setup_bindings()
        calls = [mocker.call(event, callback)]
        mocked.assert_has_calls(calls, any_order=True)

    ## ViewApplication.setup_corner
    def test_ViewApplication_setup_corner_instantiates_CornerWidget(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        mocked = mocker.patch("arrangeit.view.CornerWidget")
        view.setup_corner()
        mocked.assert_called_once()
        mocked.assert_called_with(
            view.master, shift=Settings.SHIFT_CURSOR, background=Settings.CORNER_COLOR
        )

    def test_ViewApplication_setup_corner_sets_corner_attribute(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        mocked = mocker.patch("arrangeit.view.CornerWidget")
        view.setup_corner()
        assert view.corner == mocked.return_value

    ## ViewApplication.setup_icon
    def test_ViewApplication_setup_icon_sets_icon_label(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_icon()
        mocked.assert_called_with(
            view,
            bitmap="hourglass",
            background=Settings.ICON_LABEL_BG,
            padx=Settings.ICON_LABEL_PADX,
            pady=Settings.ICON_LABEL_PADY,
        )

    def test_ViewApplication_setup_icon_calls_label_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.place.reset_mock()
        view.setup_icon()
        assert mocked.return_value.place.call_count == 1
        mocked.return_value.place.assert_called_with(
            relx=Settings.TITLE_LABEL_RELWIDTH + Settings.NAME_LABEL_RELWIDTH / 2,
            anchor=Settings.ICON_LABEL_ANCHOR,
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
            height=Settings.NAME_LABEL_HEIGHT,
            foreground=Settings.NAME_LABEL_FG,
            background=Settings.NAME_LABEL_BG,
            anchor=Settings.NAME_LABEL_ANCHOR,
            padx=Settings.NAME_LABEL_PADX,
            pady=Settings.NAME_LABEL_PADY,
        )

    def test_ViewApplication_setup_name_calls_label_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.place.reset_mock()
        view.setup_name()
        assert mocked.return_value.place.call_count == 1
        mocked.return_value.place.assert_called_with(
            relx=Settings.TITLE_LABEL_RELWIDTH,
            relheight=Settings.NAME_LABEL_RELHEIGHT,
            relwidth=Settings.NAME_LABEL_RELWIDTH,
        )

    ## ViewApplication.setup_resizable
    def test_ViewApplication_setup_resizable_initializes_Resizable(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_resizable()
        assert isinstance(view.resizable, Resizable)

    def test_ViewApplication_setup_resizable_sets_viewapp_as_master(self, mocker):
        mocked = mocker.patch("arrangeit.view.Resizable")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_resizable()
        mocked.assert_called_with(view, background=Settings.TITLE_LABEL_BG)

    def test_ViewApplication_setup_resizable_calls_label_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label.place")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.reset_mock()
        view.setup_resizable()
        assert mocked.call_count == 1
        mocked.assert_called_with(
            x=-(Settings.PROPERTY_ICON_SIZE + Settings.PROPERTY_ICON_PADX),
            y=-(Settings.PROPERTY_ICON_SIZE + Settings.PROPERTY_ICON_PADY),
            relx=Settings.TITLE_LABEL_RELWIDTH,
            rely=Settings.TITLE_LABEL_RELHEIGHT,
        )

    ## ViewApplication.setup_restored
    def test_ViewApplication_setup_restored_initializes_Restored(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_restored()
        assert isinstance(view.restored, Restored)

    def test_ViewApplication_setup_restored_sets_viewapp_as_master(self, mocker):
        mocked = mocker.patch("arrangeit.view.Restored")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_restored()
        mocked.assert_called_with(view, background=Settings.TITLE_LABEL_BG)

    def test_ViewApplication_setup_restored_calls_label_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label.place")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.reset_mock()
        view.setup_restored()
        assert mocked.call_count == 1
        mocked.assert_called_with(
            x=-2 * (Settings.PROPERTY_ICON_SIZE + Settings.PROPERTY_ICON_PADX),
            y=-(Settings.PROPERTY_ICON_SIZE + Settings.PROPERTY_ICON_PADY),
            relx=Settings.TITLE_LABEL_RELWIDTH,
            rely=Settings.TITLE_LABEL_RELHEIGHT,
        )

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
                    Settings.TITLE_LABEL_FONT_INCREASE,
                ),
            ),
            height=Settings.TITLE_LABEL_HEIGHT,
            foreground=Settings.TITLE_LABEL_FG,
            background=Settings.TITLE_LABEL_BG,
            anchor=Settings.TITLE_LABEL_ANCHOR,
            padx=Settings.TITLE_LABEL_PADX,
            pady=Settings.TITLE_LABEL_PADY,
        )

    def test_ViewApplication_setup_title_calls_label_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.place.reset_mock()
        view.setup_title()
        assert mocked.return_value.place.call_count == 1
        mocked.return_value.place.assert_called_with(
            relheight=Settings.TITLE_LABEL_RELHEIGHT,
            relwidth=Settings.TITLE_LABEL_RELWIDTH,
        )

    ## ViewApplication.setup_statusbar
    def test_ViewApplication_setup_statusbar_initializes_statusbar(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_statusbar()
        assert isinstance(view.statusbar, Statusbar)

    def test_ViewApplication_setup_statusbar_sets_viewapp_as_master(self, mocker):
        mocked = mocker.patch("arrangeit.view.Statusbar")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_statusbar()
        mocked.assert_called_with(view)

    def test_ViewApplication_setup_statusbar_calls_Statusbar_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.Statusbar")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.place.reset_mock()
        view.setup_statusbar()
        assert mocked.return_value.place.call_count == 1
        mocked.return_value.place.assert_called_with(
            rely=Settings.TITLE_LABEL_RELHEIGHT + Settings.WINDOWS_LIST_RELHEIGHT,
            relheight=Settings.STATUSBAR_RELHEIGHT,
            relwidth=Settings.STATUSBAR_RELWIDTH,
        )

    ## ViewApplication.setup_toolbar
    def test_ViewApplication_setup_toolbar_initializes_Toolbar(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_toolbar()
        assert isinstance(view.toolbar, Toolbar)

    def test_ViewApplication_setup_toolbar_sets_viewapp_as_master(self, mocker):
        mocked = mocker.patch("arrangeit.view.Toolbar")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_toolbar()
        mocked.assert_called_with(view)

    def test_ViewApplication_setup_toolbar_calls_Toolbar_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.Toolbar")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.place.reset_mock()
        view.setup_toolbar()
        assert mocked.return_value.place.call_count == 1
        mocked.return_value.place.assert_called_with(
            rely=Settings.TITLE_LABEL_RELHEIGHT + Settings.WORKSPACES_FRAME_RELHEIGHT,
            relx=Settings.WINDOWS_LIST_RELWIDTH,
            relheight=Settings.TOOLBAR_RELHEIGHT,
            relwidth=Settings.TOOLBAR_RELWIDTH,
        )

    ## ViewApplication.setup_widgets
    def test_ViewApplication_setup_widgets_calls_setup_title(self, mocker):
        mocker.patch("arrangeit.view.ViewApplication.setup_bindings")
        mocker.patch("arrangeit.view.ViewApplication.setup_resizable")
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_title")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.reset_mock()
        view.setup_widgets()
        assert mocked.call_count == 1

    def test_ViewApplication_setup_widgets_calls_setup_resizable(self, mocker):
        mocker.patch("arrangeit.view.ViewApplication.setup_bindings")
        mocker.patch("arrangeit.view.ViewApplication.setup_title")
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_resizable")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.reset_mock()
        view.setup_widgets()
        assert mocked.call_count == 1

    def test_ViewApplication_setup_widgets_calls_setup_restored(self, mocker):
        mocker.patch("arrangeit.view.ViewApplication.setup_bindings")
        mocker.patch("arrangeit.view.ViewApplication.setup_title")
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_restored")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.reset_mock()
        view.setup_widgets()
        assert mocked.call_count == 1

    def test_ViewApplication_setup_widgets_calls_setup_icon(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_icon")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.reset_mock()
        view.setup_widgets()
        assert mocked.call_count == 1

    def test_ViewApplication_setup_widgets_calls_setup_name(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_name")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.reset_mock()
        view.setup_widgets()
        assert mocked.call_count == 1

    def test_ViewApplication_setup_widgets_calls_setup_workspaces(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_workspaces")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.reset_mock()
        view.setup_widgets()
        assert mocked.call_count == 1

    def test_ViewApplication_setup_widgets_calls_setup_statusbar(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_statusbar")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.reset_mock()
        view.setup_widgets()
        assert mocked.call_count == 1

    def test_ViewApplication_setup_widgets_calls_setup_toolbar(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_toolbar")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.reset_mock()
        view.setup_widgets()
        assert mocked.call_count == 1

    def test_ViewApplication_setup_widgets_calls_setup_windows(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_windows")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.reset_mock()
        view.setup_widgets()
        assert mocked.call_count == 1

    def test_ViewApplication_setup_widgets_calls_setup_corner(self, mocker):
        mocked = mocker.patch("arrangeit.view.ViewApplication.setup_corner")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.reset_mock()
        view.setup_widgets()
        assert mocked.call_count == 1

    ## ViewApplication.setup_windows
    def test_ViewApplication_setup_windows_initializes_WindowsList(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_windows()
        assert isinstance(view.windows, WindowsList)

    def test_ViewApplication_setup_windows_sets_viewapp_as_master(self, mocker):
        mocked = mocker.patch("arrangeit.view.WindowsList")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_windows()
        mocked.assert_called_with(view)

    def test_ViewApplication_setup_windows_calls_WindowsList_place(self, mocker):
        mocked = mocker.patch("arrangeit.view.WindowsList")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.place.reset_mock()
        view.setup_windows()
        assert mocked.return_value.place.call_count == 1
        mocked.return_value.place.assert_called_with(
            rely=Settings.TITLE_LABEL_RELHEIGHT,
            relheight=Settings.WINDOWS_LIST_RELHEIGHT,
            relwidth=Settings.WINDOWS_LIST_RELWIDTH,
        )

    ## ViewApplication.setup_workspaces
    def test_ViewApplication_setup_workspaces_initializes_WorkspacesCollection(
        self, mocker
    ):
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_workspaces()
        assert isinstance(view.workspaces, WorkspacesCollection)

    def test_ViewApplication_setup_workspaces_sets_viewapp_as_master(self, mocker):
        mocked = mocker.patch("arrangeit.view.WorkspacesCollection")
        view = ViewApplication(None, mocker.MagicMock())
        view.setup_workspaces()
        mocked.assert_called_with(view)

    def test_ViewApplication_setup_workspaces_calls_WorkspacesCollection_place(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.view.WorkspacesCollection")
        view = ViewApplication(None, mocker.MagicMock())
        mocked.return_value.place.reset_mock()
        view.setup_workspaces()
        assert mocked.return_value.place.call_count == 1
        mocked.return_value.place.assert_called_with(
            rely=Settings.NAME_LABEL_RELHEIGHT,
            relx=Settings.TITLE_LABEL_RELWIDTH,
            relheight=Settings.WORKSPACES_FRAME_RELHEIGHT,
            relwidth=Settings.WORKSPACES_FRAME_RELWIDTH,
        )

    ## ViewApplication.startup
    def test_ViewApplication_startup_calls_show_root(self, mocker):
        mocker.patch("arrangeit.view.tk.StringVar")
        mocker.patch("arrangeit.view.nametofont")
        mocker.patch("arrangeit.view.increased_by_fraction")
        mocked = mocker.patch("arrangeit.view.ViewApplication.show_root")
        ViewApplication(mocker.MagicMock(), mocker.MagicMock()).startup()
        mocked.assert_called_once()

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
        mocked.reset_mock()
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
        mocked = mocker.patch("arrangeit.view.tk.Label.config")
        master = mocker.MagicMock()
        master.winfo_width.return_value = 100
        view = ViewApplication(master, mocker.MagicMock())
        mocked.reset_mock()
        view.startup()
        assert mocked.call_count == 2
        calls = [
            mocker.call(wraplength=int(100 * Settings.TITLE_LABEL_RELWIDTH)),
            mocker.call(wraplength=int(100 * Settings.NAME_LABEL_RELWIDTH)),
        ]
        mocked.assert_has_calls(calls, any_order=True)

    ## ViewApplication.update_widgets
    @pytest.mark.parametrize(
        "attr,val,typ", [("title", "foo", tk.StringVar), ("name", "bar", tk.StringVar)]
    )
    def test_ViewApplication_update_widgets_sets_attr(self, mocker, attr, val, typ):
        mocker.patch("arrangeit.view.Resizable")
        mocker.patch("arrangeit.view.Restored")
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(**{attr: val}, icon=Settings.BLANK_ICON)
        view.update_widgets(model)
        instance = getattr(view, attr)
        assert instance.get() == getattr(model, attr)
        assert isinstance(instance, typ)

    def test_ViewApplication_update_widgets_calls_resizable_set_value(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        VALUE = False
        model = WindowModel(resizable=VALUE)
        mocker.patch("arrangeit.view.tk.Label.config")
        mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        mocker.patch("arrangeit.view.Restored.set_value")
        mocked = mocker.patch("arrangeit.view.Resizable.set_value")
        view.update_widgets(model)
        mocked.call_count == 1
        mocked.assert_called_with(VALUE)

    def test_ViewApplication_update_widgets_calls_restored_set_value(self, mocker):
        view = ViewApplication(None, mocker.MagicMock())
        VALUE = False
        model = WindowModel(restored=VALUE)
        mocker.patch("arrangeit.view.tk.Label.config")
        mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        mocker.patch("arrangeit.view.Resizable.set_value")
        mocked = mocker.patch("arrangeit.view.Restored.set_value")
        view.update_widgets(model)
        mocked.call_count == 1
        mocked.assert_called_with(VALUE)

    def test_ViewApplication_update_widgets_calls_ImageTk_PhotoImage(self, mocker):
        mocker.patch("arrangeit.view.Resizable")
        mocker.patch("arrangeit.view.Restored")
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(icon=Settings.BLANK_ICON)
        mocker.patch("arrangeit.view.tk.Label.config")
        mocked = mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        view.update_widgets(model)
        mocked.call_count == 1
        mocked.assert_called_with(model.icon)

    def test_ViewApplication_update_widgets_sets_icon_image(self, mocker):
        mocker.patch("arrangeit.view.Resizable")
        mocker.patch("arrangeit.view.Restored")
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(icon=Settings.BLANK_ICON)
        mocker.patch("arrangeit.view.tk.Label.config")
        mocked = mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        view.update_widgets(model)
        assert view.icon_image == mocked.return_value

    def test_ViewApplication_update_widgets_sets_icon(self, mocker):
        mocker.patch("arrangeit.view.Resizable")
        mocker.patch("arrangeit.view.Restored")
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(icon=Settings.BLANK_ICON)
        mocked = mocker.patch("arrangeit.view.tk.Label")
        view.update_widgets(model)
        mocked.return_value.config.call_count == 1

    def test_ViewApplication_update_widgets_calls_workspaces_select_active(
        self, mocker
    ):
        mocker.patch("arrangeit.view.Resizable")
        mocker.patch("arrangeit.view.Restored")
        mocker.patch("arrangeit.view.tk.Label.config")
        mocker.patch("arrangeit.view.ImageTk.PhotoImage")
        mocked = mocker.patch("arrangeit.view.WorkspacesCollection")
        view = ViewApplication(None, mocker.MagicMock())
        model = WindowModel(workspace=1002)
        view.update_widgets(model)
        mocked.return_value.select_active.call_count == 1
        calls = [mocker.call(1002)]
        mocked.return_value.select_active.assert_has_calls(calls, any_order=True)
