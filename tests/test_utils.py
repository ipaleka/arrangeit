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

    ## get_snapping_sources_for_rect
    @pytest.mark.parametrize(
        "rect,expected",
        [
            (
                (10, 10, 100, 100),
                (
                    (0, 0, 120, 20),
                    (100, 0, 120, 120),
                    (0, 100, 120, 120),
                    (0, 0, 20, 120),
                ),
            ),
            (
                (100, 10, 200, 300),
                (
                    (90, 0, 310, 20),
                    (290, 0, 310, 320),
                    (90, 300, 310, 320),
                    (90, 0, 110, 320),
                ),
            ),
        ],
    )
    def test_get_snapping_sources_for_rect(self, rect, expected):
        assert utils.get_snapping_sources_for_rect(rect, 10) == expected

    ## intersects
    @pytest.mark.parametrize(
        "source,target,expected",
        [
            ((90, 0, 310, 20), (0, 10, 520, 30), True),
            ((90, 300, 310, 320), (0, 10, 520, 30), False),
            ((90, 0, 310, 20), (500, 10, 520, 440), False),
            ((290, 0, 310, 320), (500, 10, 520, 430), False),
            ((90, 300, 310, 320), (500, 10, 520, 430), False),
            ((0, 10, 520, 30), (370, 190, 390, 410), False),
            ((50, 50, 570, 70), (300, 60, 400, 80), True),
        ],
    )
    def test_intersects(self, source, target, expected):
        assert utils.intersects(source, target) == expected

    ## check_intersection
    def test_check_intersection_calls_intersects(self, mocker):
        mocked = mocker.patch("arrangeit.utils.intersects", return_value=False)
        sample_sources = utils.get_snapping_sources_for_rect((50, 20, 200, 20), 10)
        sample_targets1 = utils.get_snapping_sources_for_rect((300, 100, 200, 120), 10)
        sample_targets2 = utils.get_snapping_sources_for_rect((520, 400, 850, 420), 10)
        utils.check_intersection(sample_sources, [sample_targets1, sample_targets2])
        assert mocked.call_count == 16

    @pytest.mark.parametrize(
        "sources,targets,expected",
        [
            (
                (
                    (90, 0, 310, 20),
                    (290, 0, 310, 320),
                    (90, 300, 310, 320),
                    (90, 0, 110, 320),
                ),
                [
                    (
                        (0, 10, 520, 30),
                        (500, 10, 520, 430),
                        (0, 410, 520, 430),
                        (0, 10, 20, 430),
                    ),
                    (
                        (70, 190, 390, 210),
                        (370, 190, 390, 410),
                        (70, 390, 390, 410),
                        (70, 190, 90, 410),
                    ),
                ],
                ((90, 0, 310, 20), (0, 10, 520, 30)),
            ),
            (
                (
                    (
                        (90, 190, 360, 210),
                        (340, 190, 360, 410),
                        (90, 390, 360, 410),
                        (90, 190, 110, 410),
                    )
                ),
                [
                    (
                        (390, 390, 560, 410),
                        (540, 390, 560, 710),
                        (390, 690, 560, 710),
                        (390, 390, 410, 710),
                    ),
                    (
                        (590, 390, 860, 410),
                        (840, 390, 860, 910),
                        (590, 890, 860, 910),
                        (590, 390, 610, 910),
                    ),
                    (
                        (390, 390, 760, 410),
                        (740, 390, 760, 810),
                        (390, 790, 760, 810),
                        (390, 390, 410, 810),
                    ),
                ],
                False,
            ),
            (
                (
                    (
                        (
                            (390, 390, 910, 410),
                            (890, 390, 910, 910),
                            (390, 890, 910, 910),
                            (390, 390, 410, 910),
                        )
                    )
                ),
                [
                    (
                        (
                            (40, 30, 160, 50),
                            (140, 30, 160, 150),
                            (40, 130, 160, 150),
                            (40, 30, 60, 150),
                        )
                    ),
                    (
                        (
                            (990, 1190, 1310, 1210),
                            (1290, 1190, 1310, 1610),
                            (990, 1590, 1310, 1610),
                            (990, 1190, 1010, 1610),
                        )
                    ),
                    (
                        (
                            (
                                (385, 40, 605, 60),
                                (585, 40, 605, 460),
                                (385, 440, 605, 460),
                                (385, 40, 405, 460),
                            )
                        )
                    ),
                ],
                ((390, 390, 410, 910), (385, 40, 405, 460)),
            ),
        ],
    )
    def test_check_intersection_functionality(self, sources, targets, expected):
        assert utils.check_intersection(sources, targets) == expected
