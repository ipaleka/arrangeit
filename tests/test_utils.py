import pytest

from arrangeit import utils


class TestUtils(object):
    """Testing class for :py:mod:`arrangeit.utils` module."""

    ## platform_path
    @pytest.mark.parametrize("name", ["Darwin", "Linux", "Windows"])
    def test_platform_path_returns_lowercased_system_name(self, mocker, name):
        mocker.patch("arrangeit.utils.system", return_value=name)
        assert utils.platform_path() == name.lower()

    ## get_collector
    def test_get_collector_involves_default_val_for_no_arg(self, mocker):
        klass = utils.get_collector()
        platform = utils.platform_path()
        assert klass.__module__ == "arrangeit.{}.collector".format(platform)

    @pytest.mark.parametrize("name", ["darwin", "linux", "windows"])
    def test_get_collector_involves_provided_argument(self, name):
        klass = utils.get_collector(name)
        assert klass.__module__ == "arrangeit.{}.collector".format(name)

    @pytest.mark.parametrize("name", ["java", "foo", "android"])
    def test_get_collector_raises_SystemExit_for_invalid_platform(self, name):
        with pytest.raises(SystemExit) as exception:
            utils.get_collector(name)
        assert "on your platform" in exception.value.code

    ## get_player
    def test_get_player_involves_default_val_for_no_arg(self, mocker):
        klass = utils.get_player()
        platform = utils.platform_path()
        assert klass.__module__ == "arrangeit.{}.player".format(platform)

    @pytest.mark.parametrize("name", ["darwin", "linux", "windows"])
    def test_get_player_involves_provided_argument(self, name):
        klass = utils.get_player(name)
        assert klass.__module__ == "arrangeit.{}.player".format(name)

    @pytest.mark.parametrize("name", ["java", "foo", "android"])
    def test_get_player_raises_SystemExit_for_invalid_platform(self, name):
        with pytest.raises(SystemExit) as exception:
            utils.get_player(name)
        assert "on your platform" in exception.value.code
