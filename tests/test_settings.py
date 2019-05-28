import pytest
from PIL import Image

import arrangeit
from arrangeit import settings
from arrangeit.settings import SettingsMetaclass, Settings


class TestSettingsModule(object):
    """Unit testing class for settings module and SettingsMetaclass"""

    ## TestSettingsModule
    def test_settings_module_initializes_blank_icon(self):
        assert hasattr(settings, "blank_icon")
        assert isinstance(settings.blank_icon, Image.Image)

    ## SettingsMetaclass
    def test_SettingsMetaclass_is_metaclass(self):
        assert issubclass(SettingsMetaclass, type)

    def test_SettingsMetaclass_defines___getattr__(self):
        assert hasattr(SettingsMetaclass, "__getattr__")
        assert callable(SettingsMetaclass.__getattr__)


class TestSettings(object):
    """Unit testing class for :class:`Settings`."""

    ## TestSettings
    def test_Settings_metaclass_is_SettingsMetaclass(self):
        assert Settings.__class__ == arrangeit.settings.SettingsMetaclass

    ## TestSettings.get_constants
    def test_Settings_get_constants_returns_dictionary(self):
        constants = Settings.get_constants()
        assert isinstance(constants, dict)

    def test_Settings_get_constants_returns_valid_format_for_all(self):
        for key, value in Settings.get_constants().items():
            assert isinstance(key, str)
            assert key.strip("_").isupper()
            assert isinstance(value, (tuple,))
            assert len(value) == 2

    def test_Settings_get_constants_for_value_type(self):
        for _, (typ, value) in Settings.get_constants().items():
            assert value is not None
            assert isinstance(value, typ)

    def test_Settings_availability_for_all_constants(self):
        for name, (typ, value) in Settings.get_constants().items():
            assert hasattr(Settings, name)
