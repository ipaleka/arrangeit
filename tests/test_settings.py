from json import JSONDecodeError

import pytest
from PIL import Image

import arrangeit
from arrangeit import settings
from arrangeit.settings import SettingsMetaclass, Settings


class TestSettingsModule(object):
    """Unit testing class for settings module and SettingsMetaclass"""

    ## TestSettingsModule.SETTINGS
    def test_settings_module_initializes_SETTINGS(self):
        assert hasattr(settings, "SETTINGS")
        assert isinstance(settings.SETTINGS, dict)

    def test_settings_module_SETTINGS_is_dictionary(self):
        assert isinstance(settings.SETTINGS, dict)

    def test_settings_module_SETTINGS_has_valid_format_for_all(self):
        for key, value in settings.SETTINGS.items():
            assert isinstance(key, str)
            assert key.strip("_").isupper()
            assert isinstance(value, (tuple,))
            assert len(value) == 2

    def test_settings_module_SETTINGS_for_value_type(self):
        for _, (typ, value) in settings.SETTINGS.items():
            assert value is not None
            assert isinstance(value, typ)

    ## TestSettingsModule.read_user_settings
    def test_settings_read_user_settings_returns_dictionary(self):
        assert isinstance(settings.read_user_settings(), dict)

    def test_settings_read_user_settings_calls_platform_user_data_path(self, mocker):
        mocker.patch("arrangeit.settings.os")
        mocked = mocker.patch("arrangeit.settings.platform_user_data_path")
        settings.read_user_settings()
        mocked.assert_called_once()

    def test_settings_read_user_settings_checks_if_directory_exists(self, mocker):
        mocker.patch("arrangeit.settings.os.path.join", return_value="foo")
        mocker.patch("arrangeit.settings.open")
        mocked = mocker.patch("arrangeit.settings.os.path.exists", return_value=False)
        settings.read_user_settings()
        mocked.assert_called()
        mocked.assert_called_with("foo")

    def test_settings_read_user_settings_returns_empty_if_not_exists(self, mocker):
        mocker.patch("arrangeit.settings.os.path.join", return_value="foo")
        mocker.patch("arrangeit.settings.open")
        mocker.patch("arrangeit.settings.os.path.exists", return_value=False)
        assert settings.read_user_settings() == {}

    def test_settings_read_user_settings_calls_json_load(self, mocker):
        mocker.patch("arrangeit.settings.os.path.join", return_value="foo")
        mocker.patch("arrangeit.settings.os.path.exists", return_value=True)
        mocker.patch("arrangeit.settings.open")
        mocked = mocker.patch("arrangeit.settings.json.load")
        settings.read_user_settings()
        mocked.assert_called_once()

    def test_settings_read_user_settings_returns_read_data_dictionary(self, mocker):
        mocker.patch("arrangeit.settings.os.path.join", return_value="foo")
        mocker.patch("arrangeit.settings.os.path.exists", return_value=True)
        mocker.patch("arrangeit.settings.open")
        mocker.patch("arrangeit.settings.json.load", return_value={"foo": "bar"})
        assert settings.read_user_settings() == {"foo": "bar"}

    def test_settings_read_user_settings_returns_empty_for_exception(self, mocker):
        mocker.patch("arrangeit.settings.os.path.join", return_value="foo")
        mocker.patch("arrangeit.settings.os.path.exists", return_value=True)
        mocker.patch("arrangeit.settings.open")
        mocker.patch(
            "arrangeit.settings.json.load", side_effect=JSONDecodeError("", "", 0)
        )
        assert settings.read_user_settings() == {}

    ## TestSettingsModule.validate_user_settings
    def test_settings_validate_user_settings_returns_dictionary(self):
        assert isinstance(settings.validate_user_settings(), dict)

    def test_settings_validate_user_settings_returns_from_read_user(self, mocker):
        mocker.patch(
            "arrangeit.settings.read_user_settings", return_value={"ROOT_ALPHA": 0.80}
        )
        assert settings.validate_user_settings() == {"ROOT_ALPHA": 0.80}

    def test_settings_validate_user_settings_returns_only_valid_names_from_read_user(
        self, mocker
    ):
        mocker.patch(
            "arrangeit.settings.read_user_settings",
            return_value={"ROOT_ALPHA": 0.80, "foo": "bar", "foobar": 1},
        )
        assert settings.validate_user_settings() == {"ROOT_ALPHA": 0.80}

    def test_settings_validate_user_settings_returns_only_valid_types_from_read_user(
        self, mocker
    ):
        mocker.patch(
            "arrangeit.settings.read_user_settings",
            return_value={
                "ROOT_ALPHA": 1,
                "HIGHLIGHTED_COLOR": "blue",
                "TITLE_LABEL_BG": 2.0,
                "DEFAULT_CURSOR": 1,
            },
        )
        assert settings.validate_user_settings() == {"HIGHLIGHTED_COLOR": "blue"}

    ## SettingsMetaclass
    def test_SettingsMetaclass_is_metaclass(self):
        assert issubclass(SettingsMetaclass, type)

    ## SettingsMetaclass.__getattr__
    def test_SettingsMetaclass_defines___getattr__(self):
        assert hasattr(SettingsMetaclass, "__getattr__")
        assert callable(SettingsMetaclass.__getattr__)

    def test_SettingsMetaclass___getattr___uses_user_settings(self):
        Settings.user_settings = {"foo": "bar"}
        assert Settings.foo == "bar"

    @pytest.mark.parametrize(
        "constant",
        [
            "LOCATE",
            "RESIZE",
            "OTHER",
            "WINDOW_MODEL_TYPES",
            "WINDOW_MODEL_RECT_ELEMENTS",
            "ICON_SIZE",
            "BLANK_ICON",
        ],
    )
    def test_SettingsMetaclass___getattr___not_changing_core_constant(self, constant):
        value = getattr(Settings, constant)
        Settings.user_settings = {constant: "foo"}
        assert getattr(Settings, constant) != "foo"
        assert getattr(Settings, constant) == value

    def test_SettingsMetaclass___getattr___calls_validate_user_settings_just_once(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.settings.validate_user_settings")
        mocked.reset_mock()
        _ = Settings.ROOT_ALPHA
        _ = Settings.HIGHLIGHTED_COLOR
        _ = Settings.MIN_WIDTH
        assert mocked.call_count == 0

    def test_SettingsMetaclass___getattr___uses_SETTINGS_for_no_user_setting(self):
        Settings.user_settings = {"foo": "bar"}
        value = Settings.HIGHLIGHTED_COLOR
        assert value == settings.SETTINGS["HIGHLIGHTED_COLOR"][1]

    def test_SettingsMetaclass___getattr___returns_None_for_invalid_name(self):
        Settings.user_settings = {"foo": "bar"}
        value = Settings.HIGHLIGHTED11_COLOR
        assert value is None


class TestSettings(object):
    """Unit testing class for :class:`Settings`."""

    ## Settings
    def test_Settings_metaclass_is_SettingsMetaclass(self):
        assert Settings.__class__ == arrangeit.settings.SettingsMetaclass

    @pytest.mark.parametrize(
        "constant,value",
        [
            ("LOCATE", 0),
            ("RESIZE", 10),
            ("OTHER", 100),
            (
                "WINDOW_MODEL_TYPES",
                {
                    "wid": int,
                    "rect": (int, int, int, int),
                    "resizable": bool,
                    "title": str,
                    "name": str,
                    "icon": Image.Image,
                    "workspace": int,
                },
            ),
            ("WINDOW_MODEL_RECT_ELEMENTS", ("x", "y", "w", "h")),
            ("ICON_SIZE", 32),
        ],
    )
    def test_Settings_initializes_unchangeable_core_program_constant(
        self, constant, value
    ):
        assert hasattr(Settings, constant)
        assert getattr(Settings, constant) == value

    def test_Settings_initializes_blank_icon(self):
        assert hasattr(Settings, "BLANK_ICON")
        assert isinstance(Settings.BLANK_ICON, Image.Image)

    def test_Settings_availability_for_all_constants_in_SETTINGS(self):
        for name, _ in settings.SETTINGS.items():
            assert hasattr(Settings, name)

    ## Settings.is_setting
    def test_Settings_is_setting_returns_True_for_valid_setting(self, mocker):
        returned = Settings.is_setting("ROOT_ALPHA", 0.75)
        assert returned is True

    def test_Settings_is_setting_returns_False_for_invalid_setting(self, mocker):
        returned = Settings.is_setting("ROOT_ALPHA1", 0.75)
        assert returned is False

    def test_Settings_is_setting_returns_False_for_value_None(self, mocker):
        returned = Settings.is_setting("MAIN_BG", None)
        assert returned is False

    def test_Settings_is_setting_returns_False_for_invalid_value_type(self, mocker):
        returned = Settings.is_setting("MAIN_BG", 1)
        assert returned is False

    def test_Settings_is_setting_returns_False_for_core_setting(self, mocker):
        returned = Settings.is_setting("RESIZE", 187)
        assert returned is False

    ## Settings.setting_type
    def test_Settings_setting_type_returns_type_for_valid(self, mocker):
        returned = Settings.setting_type("ROOT_ALPHA")
        assert returned is float

    @pytest.mark.parametrize(
        "name,typ",
        [
            ("TRANSPARENCY_IS_ON", bool),
            ("SNAP_PIXELS", int),
            ("DEFAULT_CURSOR", str),
            ("ROOT_ALPHA", float),
        ],
    )
    def test_Settings_setting_type_returns_type_for_valid_setting_name(
        self, mocker, name, typ
    ):
        returned = Settings.setting_type(name)
        assert returned is typ

    def test_Settings_setting_type_returns_None_for_invalid(self, mocker):
        returned = Settings.setting_type("ROOT_ALPHA1")
        assert returned is None

    ## Settings.color_group
    def test_Settings_color_group_returns_list(self, mocker):
        returned = Settings.color_group("_BG")
        assert isinstance(returned, list)

    def test_Settings_color_group_returns_empty_list_for_no_group(self, mocker):
        returned = Settings.color_group("_BACKGRND")
        assert returned == []

    @pytest.mark.parametrize(
        "group,expected",
        [
            (
                "_CURSOR",
                ["SHIFT_CURSOR", "DEFAULT_CURSOR", "SELECT_CURSOR", "CORNER_CURSOR"],
            ),
            ("_SELF", ["SNAP_INCLUDE_SELF"]),
        ],
    )
    def test_Settings_color_group_returns_type_for_valid_setting_name(
        self, mocker, group, expected
    ):
        returned = Settings.color_group(group)
        assert returned == expected
