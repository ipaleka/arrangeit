import tkinter as tk
from gettext import gettext as _
from importlib import import_module

import pytest

from arrangeit import options
from arrangeit.options import (
    MESSAGES,
    CLASSES,
    WIDGETS,
    COLORS,
    OptionsDialog,
    ScaleOption,
    FloatScaleOption,
    CheckOption,
    ColorOption,
    ThemeOption,
)
from arrangeit.settings import Settings
from .mock_helpers import mocked_for_options, mocked_for_options_setup


class TestOptionsModule(object):
    """Unit testing class for options module and OptionsMetaclass"""

    ## TestOptionsModule.MESSAGES
    def test_options_module_MESSAGES_is_dictionary(self):
        assert isinstance(MESSAGES, dict)

    ## TestOptionsModule.CLASSES
    def test_options_module_CLASSES(self):
        module = import_module("arrangeit.options")
        for typ, value in CLASSES.items():
            assert isinstance(typ, type)
            klass = "{}Option".format(value)
            assert isinstance(getattr(module, klass), type)

    ## TestOptionsModule.WIDGETS
    def test_options_module_WIDGETS_is_dictionary(self):
        assert isinstance(WIDGETS, dict)

    def test_options_module_WIDGETS_has_valid_format_for_all(self):
        for key, values in WIDGETS.items():
            assert isinstance(key, str)
            for element in values:
                assert isinstance(element, (tuple,))
                assert len(element) == 2
                assert isinstance(element[0], str)
                assert isinstance(element[1], (dict,))
                assert element[0].strip("_").isupper()

    ## TestOptionsModule.COLORS
    def test_options_module_COLORS_is_dictionary(self):
        assert isinstance(COLORS, tuple)
        for value in COLORS:
            assert isinstance(value, str)


class TestOptionsDialog(object):
    """Unit testing class for :class:`OptionsDialog` class."""

    ## OptionsDialog
    def test_OptionsDialog_issubclass_of_Toplevel(self):
        assert issubclass(OptionsDialog, tk.Toplevel)

    @pytest.mark.parametrize(
        "attr,value", [("master", None), ("message", None), ("timer", None)]
    )
    def test_OptionsDialog_inits_attributes(self, attr, value):
        assert getattr(OptionsDialog, attr) == value

    ## OptionsDialog.__init__
    def test_OptionsDialog_init_calls_super_with_master_arg(self, mocker):
        mocked_for_options(mocker)
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.options.tk.Toplevel.__init__")
        OptionsDialog(master=master)
        mocked.assert_called_with(master)

    def test_OptionsDialog_init_sets_master_attribute(self, mocker):
        mocked_for_options(mocker)
        master = mocker.MagicMock()
        assert OptionsDialog(master).master == master

    def test_OptionsDialog_init_calls_setup_widgets(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.OptionsDialog.setup_widgets")
        OptionsDialog(mocker.MagicMock())
        mocked.assert_called_once()

    def test_OptionsDialog_init_calls_setup_bindings(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.OptionsDialog.setup_bindings")
        OptionsDialog(mocker.MagicMock())
        mocked.assert_called_once()

    def test_OptionsDialog_init_sets_options_dialog_title(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.OptionsDialog.title")
        OptionsDialog(mocker.MagicMock())
        mocked.assert_called_once()
        mocked.assert_called_with(MESSAGES["options_title"])

    def test_OptionsDialog_init_calls_geometry_on_root_position(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.OptionsDialog.geometry")
        master = mocker.MagicMock()
        OptionsDialog(master)
        mocked.assert_called_once()
        mocked.assert_called_with(
            "+{}+{}".format(
                master.master.winfo_x.return_value, master.master.winfo_y.return_value
            )
        )

    ## OptionsDialog.create_frame
    def test_OptionsDialog_create_frame_instantiates_ttk_Frame(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.ttk.Frame")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.create_frame(None)
        mocked.assert_called_once()
        mocked.assert_called_with(None)

    def test_OptionsDialog_create_frame_returns_frame(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.ttk.Frame")
        dialog = OptionsDialog(mocker.MagicMock())
        returned = dialog.create_frame(None)
        assert returned == mocked.return_value

    ## OptionsDialog.create_separator
    def test_OptionsDialog_create_separator_instantiates_ttk_Separator(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.ttk.Separator")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.create_separator(None)
        mocked.assert_called_once()
        mocked.assert_called_with(None, orient=tk.HORIZONTAL)

    def test_OptionsDialog_create_separator_instantiates_vertical_ttk_Separator(
        self, mocker
    ):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.ttk.Separator")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.create_separator(None, vertical=True)
        mocked.assert_called_once()
        mocked.assert_called_with(None, orient=tk.VERTICAL)

    ## OptionsDialog.create_widget
    def test_OptionsDialog_create_widget_calls_widget_class_from_name(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.OptionsDialog.widget_class_from_name")
        dialog = OptionsDialog(mocker.MagicMock())
        NAME = "ROOT_ALPHA"
        dialog.create_widget(None, NAME)
        mocked.assert_called_once()
        mocked.assert_called_with(NAME)

    def test_OptionsDialog_create_widget_instantiates_widget(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.OptionsDialog.widget_class_from_name")
        dialog = OptionsDialog(mocker.MagicMock())
        NAME = "TRANSPARENCY_IS_ON"
        dialog.create_widget(None, NAME)
        mocked.return_value.assert_called_once()
        mocked.return_value.assert_called_with(
            None,
            name=NAME,
            change_callback=dialog.change_setting,
            initial=getattr(Settings, NAME),
            label=MESSAGES[NAME],
        )

    def test_OptionsDialog_create_widget_instantiates_widget_with_kwargs(self, mocker):
        mocked_for_options(mocker)
        mocked_callback = mocker.patch("arrangeit.options.OptionsDialog.change_setting")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.widget_class_from_name")
        dialog = OptionsDialog(mocker.MagicMock())
        NAME = "SHIFT_CURSOR"
        INITIAL = 4
        mocked_settings = mocker.patch("arrangeit.options.Settings")
        type(mocked_settings).SHIFT_CURSOR = mocker.PropertyMock(return_value=INITIAL)
        KWARGS = {"from_": 1, "to": 15, "resolution": 1, "tickinterval": 2, "digits": 1}
        dialog.create_widget(None, NAME, **KWARGS)
        assert mocked.return_value.call_count == 1
        calls = [
            mocker.call(
                None,
                name=NAME,
                change_callback=mocked_callback,
                initial=INITIAL,
                label=MESSAGES[NAME],
                **KWARGS
            )
        ]
        mocked.return_value.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_create_widget_instantiates_float_scale_widget(self, mocker):
        mocked_for_options(mocker)
        mocked_callback = mocker.patch("arrangeit.options.OptionsDialog.change_setting")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.widget_class_from_name")
        dialog = OptionsDialog(mocker.MagicMock())
        NAME = "ROOT_ALPHA"
        INITIAL = 0.95
        mocked_settings = mocker.patch("arrangeit.options.Settings")
        type(mocked_settings).ROOT_ALPHA = mocker.PropertyMock(return_value=INITIAL)
        KWARGS = {
            "from_": 50,
            "to": 99,
            "resolution": 5,
            "tickinterval": 20,
            "digits": 3,
        }
        dialog.create_widget(None, NAME, **KWARGS)
        assert mocked.return_value.call_count == 1
        calls = [
            mocker.call(
                None,
                name=NAME,
                change_callback=mocked_callback,
                initial=INITIAL,
                label=MESSAGES[NAME],
                **KWARGS
            )
        ]
        mocked.return_value.assert_has_calls(calls, any_order=True)

    ## OptionsDialog.setup_bindings
    @pytest.mark.parametrize("event,callback", [("<Destroy>", "on_destroy_options")])
    def test_OptionsDialog_setup_bindings_binds_callback(self, mocker, event, callback):
        mocker.patch("arrangeit.options.tk.Toplevel.__init__")
        mocker.patch("arrangeit.options.OptionsDialog.setup_widgets")
        mocker.patch("arrangeit.options.OptionsDialog.title")
        mocker.patch("arrangeit.options.OptionsDialog.geometry")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.bind")
        dialog = OptionsDialog(mocker.MagicMock())
        callback = getattr(dialog, callback)
        dialog.setup_bindings()
        calls = [mocker.call(event, callback)]
        mocked.assert_has_calls(calls, any_order=True)

    ## OptionsDialog.setup_files_section
    def test_OptionsDialog_setup_files_section_inits_LabelFrame(self, mocker):
        mocked_for_options_setup(mocker, without_files=True)
        mocked = mocker.patch("arrangeit.options.ttk.LabelFrame")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.setup_files_section()
        calls = [mocker.call(dialog, text=MESSAGES["files"], labelanchor="nw")]
        mocked.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_files_section_sets_save_default_button(self, mocker):
        mocked_for_options_setup(mocker, without_files=True)
        mocked_frame = mocker.patch("arrangeit.options.ttk.LabelFrame")
        mocked = mocker.patch("arrangeit.options.tk.Button")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.setup_files_section()
        calls = [
            mocker.call(
                mocked_frame.return_value,
                text=_("Save data to default file"),
                activeforeground=Settings.HIGHLIGHTED_COLOR,
                command=dialog.on_save_default,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_files_section_calls_button_pack(self, mocker):
        mocked_for_options_setup(mocker, without_files=True)
        mocker.patch("arrangeit.options.ttk.LabelFrame")
        mocked = mocker.patch("arrangeit.options.tk.Button")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.setup_files_section()
        calls = [
            mocker.call(
                side=tk.LEFT,
                padx=Settings.OPTIONS_WIDGETS_PADX,
                pady=Settings.OPTIONS_WIDGETS_PADY,
            )
        ]
        mocked.return_value.pack.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_files_section_returns_LabelFrame(self, mocker):
        mocked_for_options_setup(mocker, without_files=True)
        mocker.patch("arrangeit.options.tk.Button")
        mocked = mocker.patch("arrangeit.options.ttk.LabelFrame")
        dialog = OptionsDialog(mocker.MagicMock())
        returned = dialog.setup_files_section()
        assert returned == mocked.return_value

    ## OptionsDialog.setup_section
    def test_OptionsDialog_setup_section_inits_LabelFrame(self, mocker):
        mocked_for_options_setup(mocker, without_section=True)
        mocked = mocker.patch("arrangeit.options.ttk.LabelFrame")
        dialog = OptionsDialog(mocker.MagicMock())
        NAME = "colors"
        dialog.setup_section(name=NAME)
        calls = [mocker.call(dialog, text=MESSAGES[NAME], labelanchor="nw")]
        mocked.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_section_calls_create_widget(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.ttk.LabelFrame")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.create_widget")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.setup_section("appearance")
        calls = len(WIDGETS["appearance"])
        assert mocked.call_count == calls

    def test_OptionsDialog_setup_section_calls_widget_pack(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.ttk.LabelFrame")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.create_widget")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.setup_section("appearance")
        mocked.return_value.pack.assert_called_with(
            fill=tk.X,
            side=tk.TOP,
            padx=Settings.OPTIONS_WIDGETS_PADX,
            pady=Settings.OPTIONS_WIDGETS_PADY,
        )

    def test_OptionsDialog_setup_section_calls_widget_label_pack(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.ttk.LabelFrame")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.create_widget")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.setup_section("colors", denominator=2)
        mocked.return_value.label.pack.assert_called_with(
            fill=tk.X, side=tk.TOP, padx=Settings.OPTIONS_WIDGETS_PADX, pady=0
        )

    def test_OptionsDialog_setup_section_calls_create_frame(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.ttk.LabelFrame")
        mocker.patch("arrangeit.options.OptionsDialog.create_widget")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.create_frame")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.setup_section("appearance")
        calls = len(WIDGETS["appearance"]) / 4
        assert mocked.call_count == calls

    def test_OptionsDialog_setup_section_calls_Frame_pack(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.ttk.LabelFrame")
        mocker.patch("arrangeit.options.OptionsDialog.create_widget")
        mocked = mocker.patch("arrangeit.options.ttk.Frame.pack")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.setup_section("appearance")
        mocked.assert_called_with(fill=tk.X, side=tk.LEFT, expand=True)

    def test_OptionsDialog_setup_section_calls_create_separator(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.ttk.LabelFrame")
        mocker.patch("arrangeit.options.OptionsDialog.create_widget")
        mocked_frame = mocker.patch("arrangeit.options.OptionsDialog.create_frame")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.create_separator")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.setup_section("appearance")
        calls = [mocker.call(mocked_frame.return_value)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_section_calls_Separator_pack(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.ttk.LabelFrame")
        mocker.patch("arrangeit.options.OptionsDialog.create_widget")
        mocker.patch("arrangeit.options.OptionsDialog.create_frame")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.create_separator")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.setup_section("appearance")
        calls = [mocker.call(fill=tk.X, expand=True)]
        mocked.return_value.pack.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_section_returns_section(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.ttk.LabelFrame")
        mocker.patch("arrangeit.options.OptionsDialog.create_widget")
        mocker.patch("arrangeit.options.OptionsDialog.create_frame")
        mocker.patch("arrangeit.options.OptionsDialog.create_separator")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.setup_section")
        section = OptionsDialog(mocker.MagicMock()).setup_section("appearance")
        assert section == mocked.return_value

    ## OptionsDialog.setup_widgets
    def test_OptionsDialog_setup_widgets_sets_message_var(self, mocker):
        mocked_for_options_setup(mocker)
        mocked = mocker.patch("arrangeit.options.tk.StringVar")
        mocker.patch("arrangeit.options.tk.Label")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.message = None
        dialog.setup_widgets()
        assert dialog.message is not None
        assert dialog.message == mocked.return_value

    def test_OptionsDialog_setup_widgets_calls_setup_section_for_appearance(
        self, mocker
    ):
        mocked_for_options_setup(mocker, without_section=True)
        mocker.patch("arrangeit.options.tk.StringVar")
        mocker.patch("arrangeit.options.tk.Label")
        mocker.patch("arrangeit.options.OptionsDialog.setup_files_section")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.setup_section")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.setup_widgets()
        calls = [mocker.call("appearance")]
        mocked.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_widgets_calls_setup_section_for_colors(self, mocker):
        mocked_for_options_setup(mocker, without_section=True)
        mocker.patch("arrangeit.options.tk.StringVar")
        mocker.patch("arrangeit.options.tk.Label")
        mocker.patch("arrangeit.options.ttk.LabelFrame")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.setup_section")
        dialog = OptionsDialog(mocker.MagicMock())
        mocked.reset_mock()
        dialog.setup_widgets()
        calls = [mocker.call("colors", denominator=2)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_widgets_calls_setup_files_section(self, mocker):
        mocked_for_options_setup(mocker, without_files=True)
        mocker.patch("arrangeit.options.tk.StringVar")
        mocker.patch("arrangeit.options.tk.Label")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.setup_files_section")
        dialog = OptionsDialog(mocker.MagicMock())
        mocked.reset_mock()
        dialog.setup_widgets()
        calls = [mocker.call()]
        mocked.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_widgets_calls_LabelFrame_pack(self, mocker):
        mocked_for_options_setup(mocker, without_section=True, without_files=True)
        mocker.patch("arrangeit.options.OptionsDialog.create_widget")
        mocked = mocker.patch("arrangeit.options.ttk.LabelFrame")
        dialog = OptionsDialog(mocker.MagicMock())
        mocked.reset_mock()
        dialog.setup_widgets()
        assert mocked.return_value.pack.call_count == 3
        mocked.return_value.pack.assert_called_with(
            fill=tk.BOTH,
            padx=Settings.OPTIONS_WIDGETS_PADX,
            pady=Settings.OPTIONS_WIDGETS_PADY,
            expand=True,
        )

    def test_OptionsDialog_setup_widgets_sets_label_for_message(self, mocker):
        mocked_for_options_setup(mocker)
        mocker.patch("arrangeit.options.tk.StringVar")
        mocked = mocker.patch("arrangeit.options.tk.Label")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.setup_widgets()
        calls = [
            mocker.call(
                dialog,
                textvariable=dialog.message,
                height=Settings.OPTIONS_MESSAGE_HEIGHT,
                anchor="center",
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_widgets_calls_label_pack(self, mocker):
        mocked_for_options_setup(mocker)
        mocked = mocker.patch("arrangeit.options.tk.Label")
        dialog = OptionsDialog(mocker.MagicMock())
        mocked.reset_mock()
        dialog.setup_widgets()
        calls = [mocker.call(fill=tk.X, pady=Settings.OPTIONS_WIDGETS_PADY)]
        mocked.return_value.pack.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_widgets_sets_quit_button(self, mocker):
        mocked_for_options_setup(mocker)
        mocked = mocker.patch("arrangeit.options.tk.Button")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.setup_widgets()
        calls = [
            mocker.call(
                dialog,
                text=_("Continue"),
                activeforeground=Settings.HIGHLIGHTED_COLOR,
                command=dialog.destroy,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_widgets_calls_button_pack(self, mocker):
        mocked_for_options_setup(mocker)
        mocked = mocker.patch("arrangeit.options.tk.Button")
        dialog = OptionsDialog(mocker.MagicMock())
        mocked.reset_mock()
        dialog.setup_widgets()
        calls = [
            mocker.call(
                padx=Settings.OPTIONS_WIDGETS_PADX * 2,
                pady=Settings.OPTIONS_WIDGETS_PADY * 2,
                anchor="se",
            )
        ]
        mocked.return_value.pack.assert_has_calls(calls, any_order=True)

    ## OptionsDialog.widget_class_from_name
    def test_OptionsDialog_widget_class_from_name_calls_setting_type(self, mocker):
        mocked = mocker.patch("arrangeit.settings.Settings.setting_type")
        mocked_for_options(mocker)
        dialog = OptionsDialog(mocker.MagicMock())
        NAME = "SELECTED_COLOR"
        with pytest.raises(KeyError):
            dialog.widget_class_from_name(NAME)
        mocked.assert_called_once()
        mocked.assert_called_with(NAME)

    def test_OptionsDialog_widget_class_from_name_for_typ_None(self, mocker):
        mocked = mocker.patch(
            "arrangeit.settings.Settings.setting_type", return_value=None
        )
        mocked_for_options(mocker)
        dialog = OptionsDialog(mocker.MagicMock())
        NAME = "_FG"
        dialog.widget_class_from_name(NAME)
        mocked.assert_called_once()
        mocked.assert_called_with(NAME)

    @pytest.mark.parametrize(
        "name,typ",
        [
            ("ROOT_ALPHA", "FloatScale"),
            ("TRANSPARENCY_IS_ON", "Check"),
            ("SNAP_PIXELS", "Scale"),
            ("MAIN_BG", "Color"),
            ("_BG", "Theme"),
            ("_FG", "Theme"),
        ],
    )
    def test_OptionsDialog_widget_class_from_name_returns_related_class(
        self, mocker, name, typ
    ):
        mocked_for_options(mocker)
        dialog = OptionsDialog(mocker.MagicMock())
        returned = dialog.widget_class_from_name(name)
        assert returned == getattr(options, "{}Option".format(typ))

    ## OptionsDialog.change_setting
    def test_OptionsDialog_change_setting_calls_controller_change_setting(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.tk.Label.config")
        mocker.patch("arrangeit.options.OptionsDialog.after")
        master = mocker.MagicMock()
        dialog = OptionsDialog(master)
        NAME = "BLUR_PIXELS"
        VALUE = 2
        dialog.message = mocker.MagicMock()
        dialog.change_setting(name=NAME, value=VALUE)
        master.controller.change_setting.assert_called_once()
        master.controller.change_setting.assert_called_with(NAME, VALUE)

    def test_OptionsDialog_change_setting_for_float_calls_controller_change_setting(
        self, mocker
    ):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.tk.Label.config")
        mocker.patch("arrangeit.options.OptionsDialog.after")
        master = mocker.MagicMock()
        dialog = OptionsDialog(master)
        NAME = "ROOT_ALPHA"
        VALUE = 80
        dialog.message = mocker.MagicMock()
        dialog.change_setting(name=NAME, value=VALUE)
        master.controller.change_setting.assert_called_once()
        master.controller.change_setting.assert_called_with(NAME, VALUE)

    def test_OptionsDialog_change_setting_changes_message_var(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.tk.StringVar")
        mocker.patch("arrangeit.options.OptionsDialog.after")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.message = mocker.MagicMock()
        dialog.change_setting(name="foo", value=1)
        dialog.message.set.assert_called_once()
        dialog.message.set.assert_called_with(MESSAGES["setting_changed"])

    def test_OptionsDialog_change_setting_calls_set_timer(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.tk.Label.config")
        mocker.patch("arrangeit.options.OptionsDialog.after")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.set_timer")
        master = mocker.MagicMock()
        dialog = OptionsDialog(master)
        dialog.message = mocker.MagicMock()
        dialog.change_setting(name="BLUR_PIXELS", value=2)
        mocked.assert_called_once()
        mocked.assert_called_with()

    def test_OptionsDialog_change_setting_not_called_upon_startup(self, mocker):
        mocked = mocker.patch("arrangeit.options.OptionsDialog.change_setting")
        options = OptionsDialog(tk.Frame(tk.Frame()))
        mocked.assert_not_called()
        options.destroy()

    ## OptionsDialog.set_timer
    def test_OptionsDialog_set_timer_calls_after_cancel_if_timer_exists(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.OptionsDialog.after")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.after_cancel")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.message = mocker.MagicMock()
        TIMER = 4875
        dialog.timer = TIMER
        dialog.set_timer()
        calls = [mocker.call(TIMER)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_set_timer_calls_after(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.tk.StringVar")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.after")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.message = mocker.PropertyMock(return_value="foobar")
        dialog.set_timer()
        calls = [mocker.call(Settings.OPTIONS_TIMER_DELAY, dialog.message.set, "")]
        mocked.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_set_timer_sets_timer_attribute(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.tk.StringVar")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.after")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.message = mocker.PropertyMock(return_value="foobar")
        dialog.set_timer()
        assert dialog.timer == mocked.return_value

    ## OptionsDialog.on_destroy_options
    def test_OptionsDialog_on_destroy_options_shows_root(self, mocker):
        mocked_for_options(mocker)
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.on_destroy_options(mocker.MagicMock())
        dialog.master.show_root.assert_called_once()

    def test_OptionsDialog_on_destroy_options_destroys_options(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.OptionsDialog.destroy")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.on_destroy_options(mocker.MagicMock())
        mocked.assert_called_once()

    ## OptionsDialog.on_save_default
    def test_OptionsDialog_on_save_default_calls_controller_save(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.tk.Label.config")
        mocker.patch("arrangeit.options.OptionsDialog.after")
        mocker.patch("arrangeit.options.OptionsDialog.set_timer")
        master = mocker.MagicMock()
        dialog = OptionsDialog(master)
        dialog.message = mocker.MagicMock()
        dialog.on_save_default()
        master.controller.save.assert_called_once()
        master.controller.save.assert_called_with()

    def test_OptionsDialog_on_save_default_changes_message_var(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.tk.StringVar")
        mocker.patch("arrangeit.options.OptionsDialog.set_timer")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.message = mocker.MagicMock()
        dialog.on_save_default()
        dialog.message.set.assert_called_once()
        dialog.message.set.assert_called_with(MESSAGES["save_default"])

    def test_OptionsDialog_on_save_default_calls_set_timer(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.tk.StringVar")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.set_timer")
        master = mocker.MagicMock()
        dialog = OptionsDialog(master)
        dialog.message = mocker.MagicMock()
        dialog.on_save_default()
        mocked.assert_called_once()
        mocked.assert_called_with()


class TestScaleOption(object):
    """Unit testing class for :class:`ScaleOption` class."""

    ## ScaleOption
    def test_ScaleOption_issubclass_of_Scale(self):
        assert issubclass(ScaleOption, tk.Scale)

    @pytest.mark.parametrize("attr,value", [("master", None), ("name", "")])
    def test_ScaleOption_inits_attributes(self, attr, value):
        assert getattr(ScaleOption, attr) == value

    ## ScaleOption.__init__
    def test_ScaleOption_init_calls_super_with_master_arg(self, mocker):
        mocker.patch("arrangeit.options.tk.Scale.config")
        mocker.patch("arrangeit.options.tk.Scale.set")
        mocked = mocker.patch("arrangeit.options.tk.Scale.__init__")
        master = mocker.MagicMock()
        ScaleOption(master=master, change_callback=mocker.MagicMock())
        mocked.assert_called_with(master)

    def test_ScaleOption_init_sets_master_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.Scale.config")
        mocker.patch("arrangeit.options.tk.Scale.set")
        mocker.patch("arrangeit.options.tk.Scale.__init__")
        master = mocker.MagicMock()
        assert ScaleOption(master, change_callback=mocker.MagicMock()).master == master

    def test_ScaleOption_init_sets_name_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.Scale.config")
        mocker.patch("arrangeit.options.tk.Scale.set")
        mocker.patch("arrangeit.options.tk.Scale.__init__")
        assert ScaleOption(mocker.MagicMock(), name="foo").name == "foo"

    def test_ScaleOption_init_sets_change_callback_attribute(self, mocker):
        SAMPLE = "foo"
        mocker.patch("arrangeit.options.tk.Scale.config")
        mocker.patch("arrangeit.options.tk.Scale.set")
        mocker.patch("arrangeit.options.tk.Scale.__init__")
        assert (
            ScaleOption(mocker.MagicMock(), change_callback=SAMPLE).change_callback
            == SAMPLE
        )

    def test_ScaleOption_init_configs_attributes(self, mocker):
        mocker.patch("arrangeit.options.tk.Scale.__init__")
        mocker.patch("arrangeit.options.tk.Scale.set")
        mocked = mocker.patch("arrangeit.options.tk.Scale.config")
        master = mocker.MagicMock()
        ScaleOption(
            master, label="foo", from_=1, to=10, resolution=1, tickinterval=3, digits=2
        )
        calls = [
            mocker.call(
                label="foo",
                from_=1,
                to=10,
                resolution=1,
                tickinterval=3,
                digits=2,
                orient=tk.HORIZONTAL,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_ScaleOption_init_sets_initial(self, mocker):
        mocker.patch("arrangeit.options.tk.Scale.__init__")
        mocker.patch("arrangeit.options.tk.Scale.config")
        mocked = mocker.patch("arrangeit.options.tk.Scale.set")
        master = mocker.MagicMock()
        INITIAL = 0.4
        ScaleOption(master, change_callback=mocker.MagicMock(), initial=INITIAL)
        mocked.assert_called_once()
        mocked.assert_called_with(INITIAL)

    def test_ScaleOption_init_configs_command(self, mocker):
        mocker.patch("arrangeit.options.tk.Scale.__init__")
        mocker.patch("arrangeit.options.tk.Scale.set")
        mocked = mocker.patch("arrangeit.options.tk.Scale.config")
        master = mocker.MagicMock()
        scale = ScaleOption(
            master, label="foo", from_=1, to=10, resolution=1, tickinterval=3, digits=2
        )
        calls = [mocker.call(command=scale.on_update_value)]
        mocked.assert_has_calls(calls, any_order=True)

    ## ScaleOption.on_update_value
    def test_ScaleOption_on_update_value_calls_master_change_setting(self, mocker):
        mocker.patch("arrangeit.options.tk.Scale.config")
        mocker.patch("arrangeit.options.tk.Scale.set")
        mocker.patch("arrangeit.options.tk.Scale.__init__")
        callback = mocker.MagicMock()
        NAME = "SNAP_PIXELS"
        VALUE = 4
        scale = ScaleOption(mocker.MagicMock(), change_callback=callback, name=NAME)
        scale.on_update_value(VALUE)
        callback.assert_called_once()
        callback.assert_called_with(name=NAME, value=VALUE)

    def test_ScaleOption_on_update_value_returns_break(self, mocker):
        mocker.patch("arrangeit.options.tk.Scale.__init__")
        mocker.patch("arrangeit.options.tk.Scale.set")
        mocker.patch("arrangeit.options.tk.Scale.config")
        scale = ScaleOption(mocker.MagicMock(), change_callback=mocker.MagicMock())
        returned = scale.on_update_value(0.4)
        assert returned == "break"


class TestFloatScaleOption(object):
    """Unit testing class for :class:`FloatScaleOption` class."""

    ## FloatScaleOption
    def test_FloatScaleOption_issubclass_of_ScaleOption(self):
        assert issubclass(FloatScaleOption, ScaleOption)

    ## FloatScaleOption.__init__
    def test_FloatScaleOption_init_multiplies_initial_by_100(self, mocker):
        mocked = mocker.patch("arrangeit.options.ScaleOption.__init__")
        master = mocker.MagicMock()
        INITIAL = 2
        FloatScaleOption(master, initial=INITIAL)
        mocked.assert_called_once()
        mocked.assert_called_with(master, initial=INITIAL * 100)

    ## FloatScaleOption.on_update_value
    def test_FloatScaleOption_on_update_value_calls_master_change_setting(self, mocker):
        mocker.patch("arrangeit.options.tk.Scale.config")
        mocker.patch("arrangeit.options.tk.Scale.set")
        mocker.patch("arrangeit.options.tk.Scale.__init__")
        callback = mocker.MagicMock()
        NAME = "ROOT_ALPHA"
        VALUE = 84
        scale = FloatScaleOption(
            mocker.MagicMock(), change_callback=callback, name=NAME
        )
        scale.on_update_value(VALUE)
        callback.assert_called_once()
        callback.assert_called_with(name=NAME, value=float(VALUE) / 100.0)

    def test_FloatScaleOption_on_update_value_returns_break(self, mocker):
        mocker.patch("arrangeit.options.tk.Scale.__init__")
        mocker.patch("arrangeit.options.tk.Scale.set")
        mocker.patch("arrangeit.options.tk.Scale.config")
        scale = FloatScaleOption(mocker.MagicMock(), change_callback=mocker.MagicMock())
        returned = scale.on_update_value(45)
        assert returned == "break"


class TestCheckOption(object):
    """Unit testing class for :class:`CheckOption` class."""

    ## CheckOption
    def test_CheckOption_issubclass_of_Checkbutton(self):
        assert issubclass(CheckOption, tk.Checkbutton)

    @pytest.mark.parametrize(
        "attr,value", [("master", None), ("name", ""), ("var", None)]
    )
    def test_CheckOption_inits_attributes(self, attr, value):
        assert getattr(CheckOption, attr) == value

    ## CheckOption.__init__
    def test_CheckOption_init_calls_super_with_master_arg(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.config")
        mocker.patch("arrangeit.options.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.options.tk.IntVar")
        mocked = mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        master = mocker.MagicMock()
        CheckOption(master=master, change_callback=mocker.MagicMock())
        mocked.assert_called_with(master)

    def test_CheckOption_init_sets_master_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.config")
        mocker.patch("arrangeit.options.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.options.tk.IntVar")
        master = mocker.MagicMock()
        assert CheckOption(master, change_callback=mocker.MagicMock()).master == master

    def test_CheckOption_init_sets_name_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.config")
        mocker.patch("arrangeit.options.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.options.tk.IntVar")
        assert CheckOption(mocker.MagicMock(), name="foo").name == "foo"

    def test_CheckOption_init_sets_change_callback_attribute(self, mocker):
        SAMPLE = "foo"
        mocker.patch("arrangeit.options.tk.Scale.config")
        mocker.patch("arrangeit.options.tk.Scale.set")
        mocker.patch("arrangeit.options.tk.Scale.__init__")
        mocker.patch("arrangeit.options.tk.IntVar")
        assert (
            CheckOption(mocker.MagicMock(), change_callback=SAMPLE).change_callback
            == SAMPLE
        )

    def test_CheckOption_init_sets_var_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.config")
        mocker.patch("arrangeit.options.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        mocked = mocker.patch("arrangeit.options.tk.IntVar")
        assert CheckOption(mocker.MagicMock()).var == mocked.return_value

    def test_CheckOption_init_configs_attributes(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.options.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.options.tk.IntVar")
        mocked = mocker.patch("arrangeit.options.tk.Checkbutton.config")
        master = mocker.MagicMock()
        TEXT = "foo"
        check = CheckOption(master, change_callback=mocker.MagicMock(), label=TEXT)
        mocked.assert_called_once()
        mocked.assert_called_with(
            text=TEXT, variable=check.var, command=check.on_update_value
        )

    def test_CheckOption_init_selects_for_initial_value_True(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.options.tk.Checkbutton.config")
        mocker.patch("arrangeit.options.tk.IntVar")
        mocked = mocker.patch("arrangeit.options.tk.Checkbutton.select")
        master = mocker.MagicMock()
        VALUE = True
        CheckOption(master, change_callback=mocker.MagicMock(), initial=VALUE)
        mocked.assert_called_once()

    def test_CheckOption_init_deselects_for_initial_value_False(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.options.tk.Checkbutton.config")
        mocker.patch("arrangeit.options.tk.IntVar")
        mocked = mocker.patch("arrangeit.options.tk.Checkbutton.deselect")
        master = mocker.MagicMock()
        VALUE = False
        CheckOption(master, change_callback=mocker.MagicMock(), initial=VALUE)
        mocked.assert_called_once()

    ## CheckOption.on_update_value
    def test_CheckOption_on_update_value_calls_master_change_setting(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.config")
        mocker.patch("arrangeit.options.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.options.tk.IntVar")
        master = mocker.MagicMock()
        NAME = "SNAPPING_IS_ON"
        VALUE = True
        mocked_settings = mocker.patch("arrangeit.options.Settings")
        type(mocked_settings).SNAPPING_IS_ON = mocker.PropertyMock(return_value=VALUE)
        callback = mocker.MagicMock()
        check = CheckOption(master, change_callback=callback, name=NAME)
        check.on_update_value(mocker.MagicMock())
        callback.assert_called_once()
        callback.assert_called_with(name=NAME, value=VALUE)

    def test_CheckOption_on_update_value_returns_break(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.options.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.options.tk.Checkbutton.config")
        mocker.patch("arrangeit.options.tk.IntVar")
        check = CheckOption(mocker.MagicMock(), change_callback=mocker.MagicMock())
        returned = check.on_update_value(mocker.MagicMock())
        assert returned == "break"


class TestColorOption(object):
    """Unit testing class for :class:`ColorOption` class."""

    ## ColorOption
    def test_ColorOption_issubclass_of_OptionMenu(self):
        assert issubclass(ColorOption, tk.OptionMenu)

    @pytest.mark.parametrize(
        "attr,value", [("master", None), ("name", ""), ("var", None), ("label", None)]
    )
    def test_ColorOption_inits_attributes(self, attr, value):
        assert getattr(ColorOption, attr) == value

    ## ColorOption.__init__
    def test_ColorOption_init_sets_var_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        mocker.patch("arrangeit.options.tk.Label")
        mocked = mocker.patch("arrangeit.options.tk.StringVar")
        assert ColorOption(mocker.MagicMock()).var == mocked.return_value

    def test_ColorOption_init_calls_StringVar_set(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        mocker.patch("arrangeit.options.tk.Label")
        mocked = mocker.patch("arrangeit.options.tk.StringVar")
        master = mocker.MagicMock()
        INITIAL = "white"
        ColorOption(master, change_callback=mocker.MagicMock(), initial=INITIAL)
        mocked.return_value.set.assert_called_once()
        mocked.return_value.set.assert_called_with(INITIAL)

    def test_ColorOption_init_calls_super_with_provided_arguments(self, mocker):
        mocker.patch("arrangeit.options.tk.StringVar")
        mocker.patch("arrangeit.options.tk.Label")
        mocked = mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        master = mocker.MagicMock()
        CHOICES = ("foo", "bar")
        INITIAL = "foo"
        option = ColorOption(
            master=master,
            change_callback=mocker.MagicMock(),
            initial=INITIAL,
            choices=CHOICES,
        )
        mocked.assert_called_with(
            master, option.var, INITIAL, *CHOICES, command=option.on_update_value
        )

    def test_ColorOption_init_sets_COLORS_as_initial_choices(self, mocker):
        mocked = mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        mocker.patch("arrangeit.options.tk.StringVar")
        mocker.patch("arrangeit.options.tk.Label")
        master = mocker.MagicMock()
        INITIAL = "white"
        option = ColorOption(
            master=master, change_callback=mocker.MagicMock(), initial=INITIAL
        )
        mocked.assert_called_with(
            master, option.var, INITIAL, *COLORS, command=option.on_update_value
        )

    def test_ColorOption_init_sets_master_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        mocker.patch("arrangeit.options.tk.StringVar")
        mocker.patch("arrangeit.options.tk.Label")
        master = mocker.MagicMock()
        assert ColorOption(master, change_callback=mocker.MagicMock()).master == master

    def test_ColorOption_init_sets_name_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        mocker.patch("arrangeit.options.tk.StringVar")
        mocker.patch("arrangeit.options.tk.Label")
        assert ColorOption(mocker.MagicMock(), name="foo").name == "foo"

    def test_CheckOption_init_sets_change_callback_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        mocker.patch("arrangeit.options.tk.StringVar")
        mocker.patch("arrangeit.options.tk.Label")
        assert (
            ColorOption(mocker.MagicMock(), change_callback="foo").change_callback
            == "foo"
        )

    def test_CheckOption_init_instantiates_and_sets_label_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        mocker.patch("arrangeit.options.tk.StringVar")
        mocked = mocker.patch("arrangeit.options.tk.Label")
        LABEL = "foobar"
        master = mocker.MagicMock()
        option = ColorOption(master, label=LABEL)
        mocked.assert_called_once()
        mocked.assert_called_with(master, text=LABEL, anchor="sw")
        assert option.label == mocked.return_value

    ## ColorOption.on_update_value
    def test_ColorOption_on_update_value_calls_change_setting(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        SAMPLE = "foo"
        mocked = mocker.patch("arrangeit.options.tk.StringVar")
        mocked.return_value.get.return_value = SAMPLE
        NAME = "MAIN_BG"
        CHOICES = (SAMPLE, "bar")
        mocked_callback = mocker.MagicMock()
        choice = ColorOption(
            mocker.MagicMock(),
            change_callback=mocked_callback,
            name=NAME,
            initial="foo",
            choices=CHOICES,
        )
        choice.on_update_value(mocker.MagicMock())
        mocked_callback.assert_called_once()
        mocked_callback.assert_called_with(name=NAME, value=SAMPLE)

    def test_ColorOption_on_update_value_returns_break(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        choice = ColorOption(mocker.MagicMock(), change_callback=mocker.MagicMock())
        returned = choice.on_update_value(mocker.MagicMock())
        assert returned == "break"


class TestThemeOption(object):
    """Unit testing class for :class:`ThemeOption` class."""

    ## ThemeOption
    def test_ThemeOption_issubclass_of_ColorOption(self):
        assert issubclass(ThemeOption, ColorOption)

    ## ThemeOption.__init__
    def test_ThemeOption_init_sets_initial_BG_from_Settings(self, mocker):
        mocker.patch("arrangeit.options.tk.StringVar")
        mocked = mocker.patch("arrangeit.options.ColorOption.__init__")
        master = mocker.MagicMock()
        INITIAL = Settings.MAIN_BG
        ThemeOption(master=master, name="_BG", initial="red")
        mocked.assert_called_once()
        mocked.assert_called_with(master=master, name="_BG", initial=INITIAL)

    def test_ThemeOption_init_sets_initial_FG_from_Settings(self, mocker):
        mocker.patch("arrangeit.options.tk.StringVar")
        mocked = mocker.patch("arrangeit.options.ColorOption.__init__")
        master = mocker.MagicMock()
        INITIAL = Settings.MAIN_FG
        ThemeOption(master=master, name="_FG", initial="red")
        mocked.assert_called_once()
        mocked.assert_called_with(master=master, name="_FG", initial=INITIAL)
