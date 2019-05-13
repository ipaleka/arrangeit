import pytest

from arrangeit import utils


class TestUtils(object):
    """Testing class for :py:mod:`arrangeit.utils` module."""

    ## platform_path
    @pytest.mark.parametrize("name", ["Darwin", "Linux", "Windows"])
    def test_platform_path_returns_lowercased_system_name(self, mocker, name):
        mocker.patch("arrangeit.utils.system", return_value=name)
        assert utils.platform_path() == name.lower()

    ## get_class
    @pytest.mark.parametrize("name", ["app", "collector", "player"])
    def test_get_class_involves_default_val_for_no_arg(self, mocker, name):
        # calls function from utils module made of parameterized 'name'
        klass = getattr(utils, "get_{}".format(name))()
        platform = utils.platform_path()
        assert klass.__module__ == "arrangeit.{}.{}".format(platform, name)

    @pytest.mark.parametrize("name", ["app", "collector", "player"])
    @pytest.mark.parametrize("platform", ["darwin", "linux", "windows"])
    def test_get_function_involves_provided_argument(self, platform, name):
        # calls function from utils module made of parameterized 'name'
        klass = getattr(utils, "get_{}".format(name))(platform)
        assert klass.__module__ == "arrangeit.{}.{}".format(platform, name)

    @pytest.mark.parametrize("name", ["app", "collector", "player"])
    @pytest.mark.parametrize("platform", ["java", "foo", "android"])
    def test_get_function_raises_SystemExit_for_invalid_platform(self, platform, name):
        with pytest.raises(SystemExit) as exception:
            # calls function from utils module made of parameterized 'name'
            getattr(utils, "get_{}".format(name))(platform)
        assert "on your platform" in exception.value.code

    @pytest.mark.parametrize("function", ["get_app", "get_collector", "get_player"])
    def test_get_function_calls_get_class(self, mocker, function):
        mocker.patch("arrangeit.utils.get_class")
        # calls function from utils module named from parameterized name
        getattr(utils, function)()
        utils.get_class.assert_called_once()
