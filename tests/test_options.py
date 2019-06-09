import tkinter as tk
import tkinter.ttk as ttk
from gettext import gettext as _

import pytest

import arrangeit
from arrangeit import options
from arrangeit.options import (
    MESSAGES,
    WIDGETS,
    OptionsMetaclass,
    Options,
    OptionsDialog,
    ScaleOption,
    FloatScaleOption,
    CheckOption,
    ChoiceOption,
)
from arrangeit.settings import Settings
from .mock_helpers import mocked_for_options, mocked_for_options_setup_widgets


class TestOptionsModule(object):
    """Unit testing class for options module and OptionsMetaclass"""

    ## TestOptionsModule.OPTIONS
    def test_options_module_initializes_OPTIONS(self):
        assert hasattr(options, "OPTIONS")
        assert isinstance(options.OPTIONS, dict)

    def test_options_module_OPTIONS_is_dictionary(self):
        assert isinstance(options.OPTIONS, dict)

    def test_options_module_OPTIONS_has_valid_format_for_all(self):
        for key, value in options.OPTIONS.items():
            assert isinstance(key, str)
            assert key.strip("_").isupper()
            assert isinstance(value, (tuple,))
            assert len(value) == 2

    def test_options_module_OPTIONS_for_value_type(self):
        for _a, (typ, value) in options.OPTIONS.items():
            assert value is not None
            assert isinstance(value, typ)

    ## OptionsMetaclass
    def test_OptionsMetaclass_is_metaclass(self):
        assert issubclass(OptionsMetaclass, type)

    ## OptionsMetaclass.__getattr__
    def test_OptionsMetaclass_defines___getattr__(self):
        assert hasattr(OptionsMetaclass, "__getattr__")
        assert callable(OptionsMetaclass.__getattr__)

    def test_OptionsMetaclass___getattr___returns_None_for_invalid_name(self):
        Options.user_settings = {"foo": "bar"}
        value = Options.HIGHLIGHTED11_COLOR
        assert value is None


class TestOptions(object):
    """Unit testing class for :class:`Options`."""

    ## Options
    def test_Options_metaclass_is_OptionsMetaclass(self):
        assert Options.__class__ == arrangeit.options.OptionsMetaclass

    def test_Options_initializes_highlighted_color(self):
        assert hasattr(Options, "HIGHLIGHTED_COLOR")
        assert isinstance(Options.HIGHLIGHTED_COLOR[1], str)

    def test_Options_initializes_colors(self):
        assert hasattr(Options, "COLORS")
        assert isinstance(Options.COLORS, tuple)
        assert all(isinstance(val, str) for val in Options.COLORS)

    def test_Options_availability_for_all_constants_in_OPTIONS(self):
        for name, _a in options.OPTIONS.items():
            assert hasattr(Options, name)


class TestOptionsDialog(object):
    """Unit testing class for :class:`OptionsDialog` class."""

    ## OptionsDialog
    def test_OptionsDialog_issubclass_of_Toplevel(self):
        assert issubclass(OptionsDialog, tk.Toplevel)

    @pytest.mark.parametrize("attr,value", [("master", None)])
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

    ## OptionsDialog.setup_bindings
    @pytest.mark.parametrize("event,callback", [("<Destroy>", "on_destroy_options")])
    def test_OptionsDialog_setup_bindings_binds_callback(self, mocker, event, callback):
        mocker.patch("arrangeit.options.tk.Toplevel.__init__")
        mocker.patch("arrangeit.options.OptionsDialog.setup_widgets")
        mocker.patch("arrangeit.options.OptionsDialog.title")
        mocker.patch("arrangeit.options.OptionsDialog.geometry")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.bind")
        options = OptionsDialog(mocker.MagicMock())
        callback = getattr(options, callback)
        options.setup_bindings()
        calls = [mocker.call(event, callback)]
        mocked.assert_has_calls(calls, any_order=True)

    ## OptionsDialog.setup_widgets
    def test_OptionsDialog_setup_widgets_sets_message_var(self, mocker):
        mocked_for_options_setup_widgets(mocker)
        mocked = mocker.patch("arrangeit.options.tk.StringVar")
        mocker.patch("arrangeit.options.tk.Label")
        options = OptionsDialog(mocker.MagicMock())
        options.message = None
        options.setup_widgets()
        assert options.message is not None
        assert options.message == mocked.return_value

    def test_OptionsDialog_setup_widgets_calls_setup_appearance(self, mocker):
        mocked_for_options_setup_widgets(mocker)
        mocked = mocker.patch("arrangeit.options.OptionsDialog.setup_appearance")
        options = OptionsDialog(mocker.MagicMock())
        mocked.reset_mock()
        options.setup_widgets()
        mocked.assert_called_once()

    def test_OptionsDialog_setup_widgets_sets_label_for_message(self, mocker):
        mocked_for_options_setup_widgets(mocker)
        mocker.patch("arrangeit.options.tk.StringVar")
        mocked = mocker.patch("arrangeit.options.tk.Label")
        options = OptionsDialog(mocker.MagicMock())
        options.setup_widgets()
        calls = [mocker.call(options, textvariable=options.message, anchor="center")]
        mocked.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_widgets_calls_label_pack(self, mocker):
        mocked_for_options_setup_widgets(mocker)
        mocked = mocker.patch("arrangeit.options.tk.Label")
        options = OptionsDialog(mocker.MagicMock())
        mocked.reset_mock()
        options.setup_widgets()
        assert mocked.return_value.pack.call_count == 1

    def test_OptionsDialog_setup_widgets_sets_quit_button(self, mocker):
        mocked_for_options_setup_widgets(mocker)
        mocked = mocker.patch("arrangeit.options.tk.Button")
        options = OptionsDialog(mocker.MagicMock())
        options.setup_widgets()
        calls = [
            mocker.call(
                options,
                text=_("Continue"),
                activeforeground=Options.HIGHLIGHTED_COLOR,
                command=options.destroy,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_setup_widgets_calls_button_pack(self, mocker):
        mocked_for_options_setup_widgets(mocker)
        mocked = mocker.patch("arrangeit.options.tk.Button")
        options = OptionsDialog(mocker.MagicMock())
        mocked.reset_mock()
        options.setup_widgets()
        assert mocked.return_value.pack.call_count == 1

    ## OptionsDialog.widget_class_from_name
    @pytest.mark.parametrize(
        "name,typ",
        [
            ("ROOT_ALPHA", "FloatScale"),
            ("TRANSPARENCY_IS_ON", "Check"),
            ("SNAP_PIXELS", "Scale"),
            ("MAIN_BG", "Choice"),
        ],
    )
    def test_OptionsDialog_widget_class_from_name_returns_related_class(
        self, mocker, name, typ
    ):
        mocked_for_options(mocker)
        dialog = OptionsDialog(mocker.MagicMock())
        returned = dialog.widget_class_from_name(name)
        assert returned == getattr(options, "{}Option".format(typ))

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
            text=MESSAGES[NAME],
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
                text=MESSAGES[NAME],
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
                text=MESSAGES[NAME],
                **KWARGS
            )
        ]
        mocked.return_value.assert_has_calls(calls, any_order=True)

    def test_OptionsDialog_create_widget_calls_widget_pack(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.ScaleOption.pack")
        dialog = OptionsDialog(mocker.MagicMock())
        dialog.create_widget(None, "ROOT_ALPHA")
        mocked.assert_called_once()
        mocked.assert_called_with(fill=tk.X, side=tk.TOP)

    ## OptionsDialog.setup_appearance
    def test_OptionsDialog_setup_appearance_inits_LabelFrame(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.ttk.LabelFrame")
        options = OptionsDialog(mocker.MagicMock())
        options.setup_appearance()
        mocked.assert_called_once()
        mocked.assert_called_with(options, text=MESSAGES["appearance"])

    def test_OptionsDialog_setup_appearance_calls_LabelFrame_pack(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.ttk.LabelFrame")
        options = OptionsDialog(mocker.MagicMock())
        options.setup_appearance()
        mocked.return_value.pack.assert_called_once()
        mocked.return_value.pack.assert_called_with(fill=tk.BOTH, expand=True)

    def test_OptionsDialog_setup_appearance_calls_create_widget(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.ttk.LabelFrame")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.create_widget")
        options = OptionsDialog(mocker.MagicMock())
        options.setup_appearance()
        calls = len(WIDGETS["appearance"])
        assert mocked.call_count == calls

    def test_OptionsDialog_setup_appearance_calls_frame_placeholder(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.ttk.LabelFrame")
        mocker.patch("arrangeit.options.OptionsDialog.create_widget")
        mocked = mocker.patch("arrangeit.options.OptionsDialog.frame_placeholder")
        options = OptionsDialog(mocker.MagicMock())
        options.setup_appearance()
        calls = len(WIDGETS["appearance"]) / 4
        assert mocked.call_count == calls

    ## OptionsDialog.on_destroy_options
    def test_OptionsDialog_on_destroy_options_shows_root(self, mocker):
        mocked_for_options(mocker)
        options = OptionsDialog(mocker.MagicMock())
        options.on_destroy_options(mocker.MagicMock())
        options.master.show_root.assert_called_once()

    def test_OptionsDialog_on_destroy_options_destroys_options(self, mocker):
        mocked_for_options(mocker)
        mocked = mocker.patch("arrangeit.options.OptionsDialog.destroy")
        options = OptionsDialog(mocker.MagicMock())
        options.on_destroy_options(mocker.MagicMock())
        mocked.assert_called_once()

    ## OptionsDialog.change_setting
    def test_OptionsDialog_change_setting_calls_controller_change_setting(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.tk.Label.config")
        master = mocker.MagicMock()
        options = OptionsDialog(master)
        NAME = "BLUR_PIXELS"
        VALUE = 2
        options.message = mocker.MagicMock()
        options.change_setting(name=NAME, value=VALUE)
        master.controller.change_setting.assert_called_once()
        master.controller.change_setting.assert_called_with(NAME, VALUE)

    def test_OptionsDialog_change_setting_for_float_calls_controller_change_setting(
        self, mocker
    ):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.tk.Label.config")
        master = mocker.MagicMock()
        options = OptionsDialog(master)
        NAME = "ROOT_ALPHA"
        VALUE = 80
        options.message = mocker.MagicMock()
        options.change_setting(name=NAME, value=VALUE)
        master.controller.change_setting.assert_called_once()
        master.controller.change_setting.assert_called_with(NAME, VALUE)

    def test_OptionsDialog_change_setting_changes_message_var(self, mocker):
        mocked_for_options(mocker)
        mocker.patch("arrangeit.options.tk.StringVar")
        options = OptionsDialog(mocker.MagicMock())
        SAMPLE = "foobar"
        options.message = mocker.PropertyMock(return_value=SAMPLE)
        options.change_setting(name="foo", value=1)
        assert options.message != "foobar"

    def test_OptionsDialog_change_setting_not_called_upon_startup(self, mocker):
        mocked = mocker.patch("arrangeit.options.OptionsDialog.change_setting")
        OptionsDialog(tk.Frame(tk.Frame()))
        mocked.assert_not_called()


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
        scale = ScaleOption(
            master, text="foo", from_=1, to=10, resolution=1, tickinterval=3, digits=2
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
            master, text="foo", from_=1, to=10, resolution=1, tickinterval=3, digits=2
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

    ## FloatScaleOption.on_update_value
    def test_FloatScaleOption_on_update_value_calls_master_change_setting(self, mocker):
        mocker.patch("arrangeit.options.tk.Scale.config")
        mocker.patch("arrangeit.options.tk.Scale.set")
        mocker.patch("arrangeit.options.tk.Scale.__init__")
        callback = mocker.MagicMock()
        NAME = "ROOT_ALPHA"
        VALUE = 84
        scale = FloatScaleOption(mocker.MagicMock(), change_callback=callback, name=NAME)
        scale.on_update_value(VALUE)
        callback.assert_called_once()
        callback.assert_called_with(name=NAME, value=float(VALUE)/100.0)

    def test_ScaleOption_on_update_value_returns_break(self, mocker):
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
        mocked = mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        master = mocker.MagicMock()
        CheckOption(master=master, change_callback=mocker.MagicMock())
        mocked.assert_called_with(master)

    def test_CheckOption_init_sets_master_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.config")
        mocker.patch("arrangeit.options.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        master = mocker.MagicMock()
        assert CheckOption(master, change_callback=mocker.MagicMock()).master == master

    def test_CheckOption_init_sets_name_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.config")
        mocker.patch("arrangeit.options.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        assert CheckOption(mocker.MagicMock(), name="foo").name == "foo"

    def test_CheckOption_init_sets_change_callback_attribute(self, mocker):
        SAMPLE = "foo"
        mocker.patch("arrangeit.options.tk.Scale.config")
        mocker.patch("arrangeit.options.tk.Scale.set")
        mocker.patch("arrangeit.options.tk.Scale.__init__")
        assert (
            CheckOption(mocker.MagicMock(), change_callback=SAMPLE).change_callback
            == SAMPLE
        )

    def test_CheckOption_init_sets_var_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.config")
        mocker.patch("arrangeit.options.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        assert isinstance(CheckOption(mocker.MagicMock()).var, tk.IntVar)

    def test_CheckOption_init_configs_attributes(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.options.tk.Checkbutton.deselect")
        mocked = mocker.patch("arrangeit.options.tk.Checkbutton.config")
        master = mocker.MagicMock()
        TEXT = "foo"
        check = CheckOption(master, change_callback=mocker.MagicMock(), text=TEXT)
        mocked.assert_called_once()
        mocked.assert_called_with(
            text=TEXT, variable=check.var, command=check.on_update_value
        )

    def test_CheckOption_init_selects_for_initial_value_True(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.options.tk.Checkbutton.config")
        mocked = mocker.patch("arrangeit.options.tk.Checkbutton.select")
        master = mocker.MagicMock()
        VALUE = True
        CheckOption(master, change_callback=mocker.MagicMock(), initial=VALUE)
        mocked.assert_called_once()

    def test_CheckOption_init_deselects_for_initial_value_False(self, mocker):
        mocker.patch("arrangeit.options.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.options.tk.Checkbutton.config")
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
        check = CheckOption(mocker.MagicMock(), change_callback=mocker.MagicMock())
        returned = check.on_update_value(mocker.MagicMock())
        assert returned == "break"


class TestChoiceOption(object):
    """Unit testing class for :class:`ChoiceOption` class."""

    ## ChoiceOption
    def test_ChoiceOption_issubclass_of_OptionMenu(self):
        assert issubclass(ChoiceOption, tk.OptionMenu)

    @pytest.mark.parametrize(
        "attr,value", [("master", None), ("name", ""), ("var", None)]
    )
    def test_ChoiceOption_inits_attributes(self, attr, value):
        assert getattr(ChoiceOption, attr) == value

    ## ChoiceOption.__init__
    def test_ChoiceOption_init_sets_var_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        assert isinstance(ChoiceOption(mocker.MagicMock()).var, tk.StringVar)

    def test_ChoiceOption_init_sets_var_to_initial(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        mocked = mocker.patch("arrangeit.options.tk.StringVar.set")
        INITIAL = "foo"
        ChoiceOption(mocker.MagicMock(), initial=INITIAL)
        mocked.assert_called_once()
        mocked.assert_called_with(INITIAL)

    def test_ChoiceOption_init_calls_super_with_provided_arguments(self, mocker):
        mocked = mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        master = mocker.MagicMock()
        CHOICES = ("foo", "bar")
        option = ChoiceOption(
            master=master, change_callback=mocker.MagicMock(), choices=CHOICES
        )
        mocked.assert_called_with(
            master, option.var, *CHOICES, command=option.on_update_value
        )

    def test_ChoiceOption_init_sets_master_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        master = mocker.MagicMock()
        assert ChoiceOption(master, change_callback=mocker.MagicMock()).master == master

    def test_ChoiceOption_init_sets_name_attribute(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        assert ChoiceOption(mocker.MagicMock(), name="foo").name == "foo"

    ## ChoiceOption.on_update_value
    def test_ChoiceOption_on_update_value_calls_change_setting(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        SAMPLE = "foo"
        mocked = mocker.patch("arrangeit.options.tk.StringVar")
        mocked.return_value.get.return_value = SAMPLE
        NAME = "MAIN_BG"
        CHOICES = (SAMPLE, "bar")
        mocked_callback = mocker.MagicMock()
        choice = ChoiceOption(
            mocker.MagicMock(),
            change_callback=mocked_callback,
            name=NAME,
            initial="foo",
            choices=CHOICES,
        )
        choice.on_update_value(mocker.MagicMock())
        mocked_callback.assert_called_once()
        mocked_callback.assert_called_with(name=NAME, value=SAMPLE)

    def test_ChoiceOption_on_update_value_returns_break(self, mocker):
        mocker.patch("arrangeit.options.tk.OptionMenu.__init__")
        choice = ChoiceOption(mocker.MagicMock(), change_callback=mocker.MagicMock())
        returned = choice.on_update_value(mocker.MagicMock())
        assert returned == "break"
