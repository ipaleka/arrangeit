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

    ## get_"function"
    @pytest.mark.parametrize("name", ["app", "collector", "player"])
    def test_get_function_involves_provided_argument(self, mocker, name):
        with pytest.raises(SystemExit):
            # calls function from utils module made of parameterized 'name'
            getattr(utils, "get_{}".format(name))("fooplatform")

    @pytest.mark.parametrize("name", ["app", "collector", "player"])
    @pytest.mark.parametrize("platform", ["java", "foo", "android"])
    def test_get_function_raises_SystemExit_for_invalid_platform(self, platform, name):
        with pytest.raises(SystemExit) as exception:
            # calls function from utils module made of parameterized 'name'
            getattr(utils, "get_{}".format(name))(platform)
        assert "on your platform" in exception.value.code

    @pytest.mark.parametrize("function", ["get_app", "get_collector", "get_player"])
    def test_get_function_calls_get_class(self, mocker, function):
        mocked = mocker.patch("arrangeit.utils.get_class")
        getattr(utils, function)()
        mocked.assert_called_once()



    ## append_to_collection
    @pytest.mark.parametrize(
        "elem,collection,expected",
        [
            (1, [], [1,]),
            (5, [2,], [2,5]),
            (9, [9,], [9,9]),
        ],
    )
    def test_append_to_collection_functionality(self, elem, collection, expected):
        utils.append_to_collection(elem, collection)
        assert collection == expected

    def test_append_to_collection_returns_True(self):
        assert utils.append_to_collection(1, [])

    ## quarter_by_smaller
    @pytest.mark.parametrize(
        "w,h,expected",
        [
            (3200, 1080, (480, 270)),
            (1920, 1080, (480, 270)),
            (1280, 960, (426, 240)),
            (800, 600, (266, 150)),
            (600, 800, (150, 84)),
            (1920, 2160, (480, 270)),
        ],
    )
    def test_quarter_by_smaller(self, w, h, expected):
        assert utils.quarter_by_smaller(w, h) == expected
