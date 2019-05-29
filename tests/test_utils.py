import pytest

from arrangeit import utils


class TestUtils(object):
    """Testing class for :py:mod:`arrangeit.utils` module."""

    ## platform_path
    @pytest.mark.parametrize("name", ["Darwin", "Linux", "Windows"])
    def test_platform_path_returns_lowercased_system_name(self, mocker, name):
        mocker.patch("arrangeit.utils.system", return_value=name)
        assert utils.platform_path() == name.lower()

    ## platform_user_data_path
    def test_platform_user_data_path_calls_import_module(self, mocker):
        mocked = mocker.patch("arrangeit.utils.import_module")
        utils.platform_user_data_path()
        mocked.assert_called_once()
        mocked.assert_called_with("arrangeit.{}.utils".format(utils.platform_path()))

    def test_platform_user_data_path_calls_user_data_path(self, mocker):
        mocked = mocker.patch(
            "arrangeit.{}.utils.user_data_path".format(utils.platform_path())
        )
        utils.platform_user_data_path()
        mocked.assert_called_once()

    ## get_class
    @pytest.mark.parametrize("name", ["App", "Controller", "Collector"])
    def test_get_class_involves_default_val_for_no_arg(self, mocker, name):
        klass = utils.get_component_class(name)
        platform = utils.platform_path()
        assert klass.__module__ == "arrangeit.{}.{}".format(platform, name.lower())

    ## get_component_class
    @pytest.mark.parametrize("name", ["App", "Controller", "Collector"])
    def test_get_component_class_involves_provided_argument(self, mocker, name):
        with pytest.raises(SystemExit):
            utils.get_component_class(name, "fooplatform")

    @pytest.mark.parametrize("name", ["App", "Controller", "Collector"])
    @pytest.mark.parametrize("platform", ["java", "foo", "android"])
    def test_get_component_class_raises_SystemExit_for_invalid_platform(
        self, platform, name
    ):
        with pytest.raises(SystemExit) as exception:
            utils.get_component_class(name, platform)
        assert "on your platform" in exception.value.code

    @pytest.mark.parametrize("function", ["app", "gui", "collector"])
    def test_get_component_class_calls_get_class(self, mocker, function):
        mocked = mocker.patch("arrangeit.utils.get_class")
        utils.get_component_class("Foo", "bar")
        mocked.assert_called_once()
        mocked.assert_called_with("Foo", platform="bar")

    ## append_to_collection
    @pytest.mark.parametrize(
        "elem,collection,expected", [(1, [], [1]), (5, [2], [2, 5]), (9, [9], [9, 9])]
    )
    def test_append_to_collection_functionality(self, elem, collection, expected):
        utils.append_to_collection(elem, collection)
        assert collection == expected

    def test_append_to_collection_returns_True(self):
        assert utils.append_to_collection(1, [])

    ## get_value_if_valid_type
    @pytest.mark.parametrize(
        "value,typ", [(None, int), (None, float), (None, str), (None, (int, int))]
    )
    def test_get_value_if_valid_type_returns_None_for_None_value(self, value, typ):
        assert utils.get_value_if_valid_type(value, typ) is None

    @pytest.mark.parametrize(
        "value,typ",
        [
            (1, int),
            (0, int),
            (-500, int),
            (2.0, float),
            (-45.0, float),
            ("foo", str),
            ("", str),
            (True, bool),
            (False, bool),
        ],
    )
    def test_get_value_if_valid_type_for_single_type_returns_value(self, value, typ):
        assert utils.get_value_if_valid_type(value, typ) == value

    @pytest.mark.parametrize(
        "value,typ",
        [
            (1.0, int),
            ("", int),
            (2, float),
            ("-45.0", float),
            (2.5, str),
            (2, str),
            (1, bool),
            (0, bool),
            ("foo", bool),
            (-1, bool),
        ],
    )
    def test_get_value_if_valid_type_for_single_type_returns_None(self, value, typ):
        assert utils.get_value_if_valid_type(value, typ) is None

    @pytest.mark.parametrize(
        "value,typ",
        [
            ((2, 5.0), (int, float)),
            (("2", 5, 5.0), (str, int, float)),
            ((4.3, (2, 3)), (float, tuple)),
            ((2, True), (int, bool)),
            ((2, 5, 0, 3), (int, int, int, int)),
        ],
    )
    def test_get_value_if_valid_type_for_collection_type_returns_value(
        self, value, typ
    ):
        assert utils.get_value_if_valid_type(value, typ) == value

    @pytest.mark.parametrize(
        "value,typ",
        [
            ((2, 5.0), (float, float)),
            (("2", 5, 5.0), (str, int, int)),
            ((4.3, (2, 3)), (float, list)),
            ((2, True), (bool, bool)),
            ((2, 5, 0, 3), (int, int, str, int)),
        ],
    )
    def test_get_value_if_valid_type_for_collection_returns_empty(self, value, typ):
        assert utils.get_value_if_valid_type(value, typ) is ()

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

    ## increased_by_fraction
    @pytest.mark.parametrize(
        "value,fraction,expected",
        [
            (10, 0.1, 11),
            (16, 0.1, 18),
            (12, 0.2, 14),
            (15, 0.2, 18),
            (15, -0.2, 12),
            (10, -0.1, 9),
        ],
    )
    def test_increased_by_fraction(self, value, fraction, expected):
        assert utils.increased_by_fraction(value, fraction) == expected

    ## get_snapping_rects_for_rect
    @pytest.mark.parametrize(
        "rect,expected",
        [
            (
                (10, 10, 100, 100),
                (
                    (0, 0, 120, 20),
                    (100, 00, 20, 120),
                    (0, 100, 120, 20),
                    (0, 0, 20, 120),
                ),
            ),
            (
                (100, 10, 200, 300),
                (
                    (90, 0, 220, 20),
                    (290, 0, 20, 320),
                    (90, 300, 220, 20),
                    (90, 0, 20, 320),
                ),
            ),
        ],
    )
    def test_get_snapping_rects_for_rect(self, rect, expected):
        assert utils.get_snapping_rects_for_rect(rect, 10) == expected

