import tkinter as tk
from gettext import gettext as _

import pytest

import arrangeit
from arrangeit import options
from arrangeit.options import MESSAGES, OptionsMetaclass, Options, OptionsDialog, ScaleOption, CheckOption, ChoiceOption


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
    def test_Options_issubclass_of_Toplevel(self):
        assert issubclass(OptionsDialog, tk.Toplevel)

    @pytest.mark.parametrize("attr,value", [("master", None)])
    def test_Options_inits_attributes(self, attr, value):
        assert getattr(OptionsDialog, attr) == value

    ## OptionsDialog.__init__
    def test_Options_init_calls_super_with_master_arg(self, mocker):
        mocker.patch("arrangeit.view.OptionsDialog.setup_bindings")
        mocker.patch("arrangeit.view.OptionsDialog.setup_widgets")
        mocker.patch("arrangeit.view.OptionsDialog.geometry")
        master = mocker.MagicMock()
        mocked = mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        OptionsDialog(master=master)
        mocked.assert_called_with(master)

    def test_Options_init_sets_master_attribute(self, mocker):
        mocker.patch("arrangeit.view.OptionsDialog.setup_widgets")
        mocker.patch("arrangeit.view.OptionsDialog.setup_bindings")
        mocker.patch("arrangeit.view.OptionsDialog.geometry")
        mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        master = mocker.MagicMock()
        assert OptionsDialog(master).master == master

    def test_Options_init_calls_setup_widgets(self, mocker):
        mocker.patch("arrangeit.view.OptionsDialog.geometry")
        mocker.patch("arrangeit.view.OptionsDialog.setup_bindings")
        mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        mocked = mocker.patch("arrangeit.view.OptionsDialog.setup_widgets")
        OptionsDialog(mocker.MagicMock())
        mocked.assert_called_once()

    def test_Options_init_calls_setup_bindings(self, mocker):
        mocker.patch("arrangeit.view.OptionsDialog.geometry")
        mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        mocker.patch("arrangeit.view.OptionsDialog.setup_widgets")
        mocked = mocker.patch("arrangeit.view.OptionsDialog.setup_bindings")
        OptionsDialog(mocker.MagicMock())
        mocked.assert_called_once()

    def test_Options_init_calls_geometry_on_root_position(self, mocker):
        mocker.patch("arrangeit.view.OptionsDialog.setup_widgets")
        mocker.patch("arrangeit.view.OptionsDialog.setup_bindings")
        mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        mocked = mocker.patch("arrangeit.view.OptionsDialog.geometry")
        master = mocker.MagicMock()
        OptionsDialog(master)
        mocked.assert_called_once()
        mocked.assert_called_with(
            "+{}+{}".format(
                master.master.winfo_x.return_value, master.master.winfo_y.return_value
            )
        )

    ## OptionsDialog.setup_widgets
    def test_Options_setup_widgets_sets_message_label(self, mocker):
        mocker.patch("arrangeit.view.OptionsDialog.setup_bindings")
        mocker.patch("arrangeit.view.OptionsDialog.geometry")
        mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        mocker.patch("arrangeit.view.OptionsDialog.destroy")
        mocker.patch("arrangeit.view.tk.Button")
        mocked = mocker.patch("arrangeit.view.tk.Label")
        options = OptionsDialog(mocker.MagicMock())
        options.setup_widgets()
        calls = [mocker.call(options, text="", anchor="center")]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Options_setup_widgets_calls_label_pack(self, mocker):
        mocker.patch("arrangeit.view.OptionsDialog.geometry")
        mocker.patch("arrangeit.view.OptionsDialog.setup_bindings")
        mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        mocker.patch("arrangeit.view.OptionsDialog.destroy")
        mocker.patch("arrangeit.view.tk.Button")
        mocked = mocker.patch("arrangeit.view.tk.Label")
        options = OptionsDialog(mocker.MagicMock())
        mocked.reset_mock()
        options.setup_widgets()
        assert mocked.return_value.pack.call_count == 1

    def test_Options_setup_widgets_sets_quit_button(self, mocker):
        mocker.patch("arrangeit.view.OptionsDialog.setup_bindings")
        mocker.patch("arrangeit.view.OptionsDialog.geometry")
        mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        mocker.patch("arrangeit.view.OptionsDialog.destroy")
        mocker.patch("arrangeit.view.tk.Label")
        mocked = mocker.patch("arrangeit.view.tk.Button")
        options = OptionsDialog(mocker.MagicMock())
        options.setup_widgets()
        calls = [
            mocker.call(
                options,
                text=_("Cancel"),
                activeforeground=Options.HIGHLIGHTED_COLOR,
                command=options.destroy,
            )
        ]
        mocked.assert_has_calls(calls, any_order=True)

    def test_Options_setup_widgets_calls_button_pack(self, mocker):
        mocker.patch("arrangeit.view.OptionsDialog.geometry")
        mocker.patch("arrangeit.view.OptionsDialog.setup_bindings")
        mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        mocker.patch("arrangeit.view.OptionsDialog.destroy")
        mocker.patch("arrangeit.view.tk.Label")
        mocked = mocker.patch("arrangeit.view.tk.Button")
        options = OptionsDialog(mocker.MagicMock())
        mocked.reset_mock()
        options.setup_widgets()
        assert mocked.return_value.pack.call_count == 1

    ## OptionsDialog.setup_bindings
    @pytest.mark.parametrize("event,callback", [("<Destroy>", "on_destroy_options")])
    def test_Options_setup_bindings_binds_callback(self, mocker, event, callback):
        mocker.patch("arrangeit.view.OptionsDialog.setup_widgets")
        mocker.patch("arrangeit.view.OptionsDialog.geometry")
        mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        mocked = mocker.patch("arrangeit.view.OptionsDialog.bind")
        options = OptionsDialog(mocker.MagicMock())
        callback = getattr(options, callback)
        options.setup_bindings()
        calls = [mocker.call(event, callback)]
        mocked.assert_has_calls(calls, any_order=True)

    ## OptionsDialog.on_destroy_options
    def test_Options_on_destroy_options_shows_root(self, mocker):
        mocker.patch("arrangeit.view.OptionsDialog.setup_widgets")
        mocker.patch("arrangeit.view.OptionsDialog.setup_bindings")
        mocker.patch("arrangeit.view.OptionsDialog.geometry")
        mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        mocker.patch("arrangeit.view.OptionsDialog.destroy")
        options = OptionsDialog(mocker.MagicMock())
        options.on_destroy_options(mocker.MagicMock())
        options.master.master.update.assert_called_once()
        options.master.master.deiconify.assert_called_once()

    def test_Options_on_destroy_options_destroys_options(self, mocker):
        mocker.patch("arrangeit.view.OptionsDialog.setup_widgets")
        mocker.patch("arrangeit.view.OptionsDialog.setup_bindings")
        mocker.patch("arrangeit.view.OptionsDialog.geometry")
        mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        mocked = mocker.patch("arrangeit.view.OptionsDialog.destroy")
        options = OptionsDialog(mocker.MagicMock())
        options.on_destroy_options(mocker.MagicMock())
        mocked.assert_called_once()

    ## OptionsDialog.change_setting
    def test_Options_change_setting_calls_run_task(self, mocker):
        mocker.patch("arrangeit.view.OptionsDialog.setup_widgets")
        mocker.patch("arrangeit.view.OptionsDialog.setup_bindings")
        mocker.patch("arrangeit.view.OptionsDialog.geometry")
        mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        mocker.patch("arrangeit.view.tk.Label.config")
        master = mocker.MagicMock()
        options = OptionsDialog(master)
        NAME = "foo"
        VALUE = 2
        options.message = mocker.MagicMock()
        options.change_setting(name=NAME, value=VALUE)
        master.controller.app.run_task.assert_called_once()
        master.controller.app.run_task.assert_called_with("change_setting", NAME, VALUE)

    def test_Options_change_setting_displays_message(self, mocker):
        mocker.patch("arrangeit.view.OptionsDialog.setup_widgets")
        mocker.patch("arrangeit.view.OptionsDialog.setup_bindings")
        mocker.patch("arrangeit.view.OptionsDialog.geometry")
        mocker.patch("arrangeit.view.tk.Toplevel.__init__")
        master = mocker.MagicMock()
        options = OptionsDialog(master)
        options.message = mocker.MagicMock()
        options.change_setting(name="foo", value=1)
        options.message.config.assert_called_once()
        options.message.config.assert_called_with(text=MESSAGES["setting_changed"])


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
        mocker.patch("arrangeit.view.tk.Scale.config")
        mocker.patch("arrangeit.view.tk.Scale.set")
        mocked = mocker.patch("arrangeit.view.tk.Scale.__init__")
        master = mocker.MagicMock()
        ScaleOption(master=master)
        mocked.assert_called_with(master)

    def test_ScaleOption_init_sets_master_attribute(self, mocker):
        mocker.patch("arrangeit.view.tk.Scale.config")
        mocker.patch("arrangeit.view.tk.Scale.set")
        mocker.patch("arrangeit.view.tk.Scale.__init__")
        master = mocker.MagicMock()
        assert ScaleOption(master).master == master

    def test_ScaleOption_init_sets_name_attribute(self, mocker):
        mocker.patch("arrangeit.view.tk.Scale.config")
        mocker.patch("arrangeit.view.tk.Scale.set")
        mocker.patch("arrangeit.view.tk.Scale.__init__")
        assert ScaleOption(mocker.MagicMock(), name="foo").name == "foo"

    def test_ScaleOption_init_configs_attributes(self, mocker):
        mocker.patch("arrangeit.view.tk.Scale.__init__")
        mocker.patch("arrangeit.view.tk.Scale.set")
        mocked = mocker.patch("arrangeit.view.tk.Scale.config")
        master = mocker.MagicMock()
        scale = ScaleOption(
            master,
            text="foo",
            from_=0.2,
            to=0.8,
            resolution=0.1,
            tickinterval=0.3,
            digits=2,
        )
        mocked.assert_called_once()
        mocked.assert_called_with(
            label="foo",
            from_=0.2,
            to=0.8,
            resolution=0.1,
            tickinterval=0.3,
            digits=2,
            orient=tk.HORIZONTAL,
            command=scale.on_update_value,
        )

    def test_ScaleOption_init_sets_initial(self, mocker):
        mocker.patch("arrangeit.view.tk.Scale.__init__")
        mocker.patch("arrangeit.view.tk.Scale.config")
        mocked = mocker.patch("arrangeit.view.tk.Scale.set")
        master = mocker.MagicMock()
        INITIAL = 0.4
        ScaleOption(master, initial=INITIAL)
        mocked.assert_called_once()
        mocked.assert_called_with(INITIAL)

    ## ScaleOption.on_update_value
    def test_ScaleOption_on_update_value_calls_master_change_setting(self, mocker):
        mocker.patch("arrangeit.view.tk.Scale.config")
        mocker.patch("arrangeit.view.tk.Scale.set")
        mocker.patch("arrangeit.view.tk.Scale.__init__")
        master = mocker.MagicMock()
        NAME = "ROOT_ALPHA"
        VALUE = 0.4
        scale = ScaleOption(master, name=NAME)
        scale.on_update_value(VALUE)
        master.change_setting.assert_called_once()
        master.change_setting.assert_called_with(name=NAME, value=VALUE)

    def test_ScaleOption_on_update_value_returns_break(self, mocker):
        mocker.patch("arrangeit.view.tk.Scale.__init__")
        mocker.patch("arrangeit.view.tk.Scale.set")
        mocker.patch("arrangeit.view.tk.Scale.config")
        scale = ScaleOption(mocker.MagicMock())
        returned = scale.on_update_value(0.4)
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
        mocker.patch("arrangeit.view.tk.Checkbutton.config")
        mocker.patch("arrangeit.view.tk.Checkbutton.deselect")
        mocked = mocker.patch("arrangeit.view.tk.Checkbutton.__init__")
        master = mocker.MagicMock()
        CheckOption(master=master)
        mocked.assert_called_with(master)

    def test_CheckOption_init_sets_master_attribute(self, mocker):
        mocker.patch("arrangeit.view.tk.Checkbutton.config")
        mocker.patch("arrangeit.view.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.view.tk.Checkbutton.__init__")
        master = mocker.MagicMock()
        assert CheckOption(master).master == master

    def test_CheckOption_init_sets_name_attribute(self, mocker):
        mocker.patch("arrangeit.view.tk.Checkbutton.config")
        mocker.patch("arrangeit.view.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.view.tk.Checkbutton.__init__")
        assert CheckOption(mocker.MagicMock(), name="foo").name == "foo"

    def test_CheckOption_init_sets_var_attribute(self, mocker):
        mocker.patch("arrangeit.view.tk.Checkbutton.config")
        mocker.patch("arrangeit.view.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.view.tk.Checkbutton.__init__")
        assert isinstance(CheckOption(mocker.MagicMock()).var, tk.IntVar)

    def test_CheckOption_init_configs_attributes(self, mocker):
        mocker.patch("arrangeit.view.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.view.tk.Checkbutton.deselect")
        mocked = mocker.patch("arrangeit.view.tk.Checkbutton.config")
        master = mocker.MagicMock()
        TEXT = "foo"
        check = CheckOption(master, text=TEXT)
        mocked.assert_called_once()
        mocked.assert_called_with(
            text=TEXT, variable=check.var, command=check.on_update_value
        )

    def test_CheckOption_init_selects_for_initial_value_True(self, mocker):
        mocker.patch("arrangeit.view.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.view.tk.Checkbutton.config")
        mocked = mocker.patch("arrangeit.view.tk.Checkbutton.select")
        master = mocker.MagicMock()
        VALUE = True
        CheckOption(master, initial=VALUE)
        mocked.assert_called_once()

    def test_CheckOption_init_deselects_for_initial_value_False(self, mocker):
        mocker.patch("arrangeit.view.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.view.tk.Checkbutton.config")
        mocked = mocker.patch("arrangeit.view.tk.Checkbutton.deselect")
        master = mocker.MagicMock()
        VALUE = False
        CheckOption(master, initial=VALUE)
        mocked.assert_called_once()

    ## CheckOption.on_update_value
    def test_CheckOption_on_update_value_calls_master_change_setting(self, mocker):
        mocker.patch("arrangeit.view.tk.Checkbutton.config")
        mocker.patch("arrangeit.view.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.view.tk.Checkbutton.__init__")
        master = mocker.MagicMock()
        NAME = "SNAPPING_IS_ON"
        check = CheckOption(master, name=NAME)
        check.on_update_value(mocker.MagicMock())
        master.change_setting.assert_called_once()
        master.change_setting.assert_called_with(name=NAME, value=False)

    def test_CheckOption_on_update_value_returns_break(self, mocker):
        mocker.patch("arrangeit.view.tk.Checkbutton.__init__")
        mocker.patch("arrangeit.view.tk.Checkbutton.deselect")
        mocker.patch("arrangeit.view.tk.Checkbutton.config")
        check = CheckOption(mocker.MagicMock())
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
        mocker.patch("arrangeit.view.tk.OptionMenu.__init__")
        assert isinstance(ChoiceOption(mocker.MagicMock()).var, tk.StringVar)

    def test_ChoiceOption_init_sets_var_to_initial(self, mocker):
        mocker.patch("arrangeit.view.tk.OptionMenu.__init__")
        mocked = mocker.patch("arrangeit.view.tk.StringVar.set")
        INITIAL = "foo"
        ChoiceOption(mocker.MagicMock(), initial=INITIAL)
        mocked.assert_called_once()
        mocked.assert_called_with(INITIAL)

    def test_ChoiceOption_init_calls_super_with_provided_arguments(self, mocker):
        mocked = mocker.patch("arrangeit.view.tk.OptionMenu.__init__")
        master = mocker.MagicMock()
        CHOICES = ("foo", "bar")
        option = ChoiceOption(master=master, choices=CHOICES)
        mocked.assert_called_with(
            master, option.var, *CHOICES, command=option.on_update_value
        )

    def test_ChoiceOption_init_sets_master_attribute(self, mocker):
        mocker.patch("arrangeit.view.tk.OptionMenu.__init__")
        master = mocker.MagicMock()
        assert ChoiceOption(master).master == master

    def test_ChoiceOption_init_sets_name_attribute(self, mocker):
        mocker.patch("arrangeit.view.tk.OptionMenu.__init__")
        assert ChoiceOption(mocker.MagicMock(), name="foo").name == "foo"

    ## ChoiceOption.on_update_value
    def test_ChoiceOption_on_update_value_calls_master_change_setting(self, mocker):
        mocker.patch("arrangeit.view.tk.OptionMenu.__init__")
        master = mocker.MagicMock()
        NAME = "MAIN_BG"
        CHOICES = ("foo", "bar")
        check = ChoiceOption(master, name=NAME, initial="foo", choices=CHOICES)
        check.on_update_value(mocker.MagicMock())
        master.change_setting.assert_called_once()
        master.change_setting.assert_called_with(name=NAME, value="foo")

    def test_ChoiceOption_on_update_value_returns_break(self, mocker):
        mocker.patch("arrangeit.view.tk.OptionMenu.__init__")
        check = ChoiceOption(mocker.MagicMock())
        returned = check.on_update_value(mocker.MagicMock())
        assert returned == "break"
