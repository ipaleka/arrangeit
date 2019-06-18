import os
import pytest
from PIL import ImageFilter

from arrangeit import utils
from arrangeit.settings import Settings

from .fixtures import (
    SAMPLE_SNAPPING_SOURCES_FOR_RECT,
    SAMPLE_CHECK_INTERSECTIONS,
    INTERSECTS_SAMPLES,
    OFFSET_INTERSECTING_PAIR_SAMPLES,
)


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
        assert exception.value.code == utils.MESSAGES["platform_error"]

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

    ## open_image
    def test_open_image_returns_Image(self, mocker):
        mocked = mocker.patch("arrangeit.utils.ImageOps.colorize")
        mocker.patch("arrangeit.utils.Image.open")
        returned = utils.open_image("resize.png")
        assert returned == mocked.return_value

    def test_open_image_calls_Image_open(self, mocker):
        mocker.patch("arrangeit.utils.ImageOps.colorize")
        mocker.patch("PIL.Image.Image.convert")
        mocked = mocker.patch("arrangeit.utils.Image.open")
        PATH = "resize.png"
        utils.open_image(PATH)
        mocked.assert_called_once()
        mocked.assert_called_with(
            os.path.join(os.path.dirname(utils.__file__), "resources", PATH)
        )

    def test_open_image_calls_Image_convert(self, mocker):
        mocker.patch("arrangeit.utils.ImageOps.colorize")
        mocked = mocker.patch("arrangeit.utils.Image.open")
        utils.open_image("resize.png")
        mocked.return_value.convert.assert_called_once()
        mocked.return_value.convert.assert_called_with("L")

    def test_open_image_calls_ImageOps_colorize(self, mocker):
        mocked_image = mocker.patch("arrangeit.utils.Image.open")
        mocked = mocker.patch("arrangeit.utils.ImageOps.colorize")
        BACKGROUND = "yelow"
        utils.open_image("resize.png", background=BACKGROUND)
        mocked.assert_called_once()
        mocked.assert_called_with(
            mocked_image.return_value.convert.return_value, "black", BACKGROUND
        )

    def test_open_image_calls_different_ImageOps_colorize_if_colorized_set(
        self, mocker
    ):
        mocked_image = mocker.patch("arrangeit.utils.Image.open")
        mocked = mocker.patch("arrangeit.utils.ImageOps.colorize")
        PATH, FOREGROUND, BACKGROUND = "resize.png", "red", "yelow"
        utils.open_image(
            PATH, background=BACKGROUND, colorized=True, foreground=FOREGROUND
        )
        mocked.assert_called_once()
        mocked.assert_called_with(
            mocked_image.return_value.convert.return_value, FOREGROUND, BACKGROUND
        )

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

    ## get_prepared_screenshot
    def test_get_prepared_screenshot_calls_filter(self, mocker):
        image = Settings.BLANK_ICON
        mocker.patch("PIL.ImageTk.PhotoImage")
        mocker.patch("PIL.ImageFilter.BoxBlur")
        mocked = mocker.patch("PIL.Image.Image.filter")
        utils.get_prepared_screenshot(image, grayscale=False)
        mocked.assert_called_once()

    def test_get_prepared_screenshot_calls_filter_with_blur_size(self, mocker):
        image = Settings.BLANK_ICON
        mocker.patch("PIL.ImageTk.PhotoImage")
        mocker.patch("PIL.ImageFilter.BoxBlur")
        BLUR = 5
        mocked = mocker.patch("PIL.Image.Image.filter")
        utils.get_prepared_screenshot(image, blur_size=BLUR, grayscale=False)
        mocked.assert_called_once()
        mocked.assert_called_with(ImageFilter.BoxBlur(BLUR))

    def test_get_prepared_screenshot_converts_to_grayscale_if_set(self, mocker):
        image = Settings.BLANK_ICON
        mocked_photo = mocker.patch("PIL.ImageTk.PhotoImage")
        mocker.patch("PIL.ImageFilter.BoxBlur")
        mocker.patch("PIL.Image.Image.filter")
        mocked = mocker.patch("PIL.Image.Image.convert")
        assert (
            utils.get_prepared_screenshot(image, grayscale=True)
            == mocked_photo.return_value
        )
        mocked.assert_called_once()
        mocked.assert_called_with("L")

    def test_get_prepared_screenshot_not_converting_to_grayscale(self, mocker):
        image = Settings.BLANK_ICON
        mocker.patch("PIL.ImageTk.PhotoImage")
        mocker.patch("PIL.ImageFilter.BoxBlur")
        mocker.patch("PIL.Image.Image.filter")
        mocked = mocker.patch("PIL.Image.Image.convert")
        utils.get_prepared_screenshot(image, grayscale=False)
        mocked.assert_not_called()

    def test_get_prepared_screenshot_returns_ImageTk_PhotoImage(self, mocker):
        mocker.patch("PIL.ImageFilter.BoxBlur")
        mocker.patch("PIL.Image.Image.filter")
        mocked = mocker.patch("PIL.ImageTk.PhotoImage")
        assert utils.get_prepared_screenshot(Settings.BLANK_ICON) == mocked.return_value

    ## _get_snapping_source_by_ordinal
    @pytest.mark.parametrize("rect,expected", SAMPLE_SNAPPING_SOURCES_FOR_RECT)
    def test__get_snapping_source_by_ordinal_ordinal(self, rect, expected):
        for i in range(4):
            assert utils._get_snapping_source_by_ordinal(rect, 10, i) == expected[i]

    ## get_snapping_sources_for_rect
    @pytest.mark.parametrize("rect,expected", SAMPLE_SNAPPING_SOURCES_FOR_RECT)
    def test_get_snapping_sources_for_rect_corner_None(self, rect, expected):
        assert utils.get_snapping_sources_for_rect(rect, 10) == expected
        assert utils.get_snapping_sources_for_rect(rect, 10, None) == expected

    @pytest.mark.parametrize("rect,expected", SAMPLE_SNAPPING_SOURCES_FOR_RECT)
    def test_get_snapping_sources_for_rect_corner_0(self, rect, expected):
        assert utils.get_snapping_sources_for_rect(rect, 10, 0) == (
            expected[0],
            expected[3],
        )

    @pytest.mark.parametrize("rect,expected", SAMPLE_SNAPPING_SOURCES_FOR_RECT)
    def test_get_snapping_sources_for_rect_corner_1(self, rect, expected):
        assert utils.get_snapping_sources_for_rect(rect, 10, 1) == (
            expected[0],
            expected[1],
        )

    @pytest.mark.parametrize("rect,expected", SAMPLE_SNAPPING_SOURCES_FOR_RECT)
    def test_get_snapping_sources_for_rect_corner_2(self, rect, expected):
        assert utils.get_snapping_sources_for_rect(rect, 10, 2) == (
            expected[2],
            expected[1],
        )

    @pytest.mark.parametrize("rect,expected", SAMPLE_SNAPPING_SOURCES_FOR_RECT)
    def test_get_snapping_sources_for_rect_corner_3(self, rect, expected):
        assert utils.get_snapping_sources_for_rect(rect, 10, 3) == (
            expected[2],
            expected[3],
        )

    ## _intersects
    @pytest.mark.parametrize("source,target,expected", INTERSECTS_SAMPLES)
    def test_intersects_functionality(self, source, target, expected):
        assert utils._intersects(source, target) == expected

    ## _offset_for_intersecting_pair
    def test_offset_for_intersecting_pair_returns_False(self, mocker):
        assert utils._offset_for_intersecting_pair(False, 10) == (0, 0)

    @pytest.mark.parametrize("pair,offset", OFFSET_INTERSECTING_PAIR_SAMPLES[0])
    def test_offset_for_intersecting_pair_corner_0_functionality(self, pair, offset):
        assert utils._offset_for_intersecting_pair(pair, 10) == offset

    @pytest.mark.parametrize("pair,offset", OFFSET_INTERSECTING_PAIR_SAMPLES[1])
    def test_offset_for_intersecting_pair_corner_1_functionality(self, pair, offset):
        assert utils._offset_for_intersecting_pair(pair, 10) == offset

    @pytest.mark.parametrize("pair,offset", OFFSET_INTERSECTING_PAIR_SAMPLES[2])
    def test_offset_for_intersecting_pair_corner_2_functionality(self, pair, offset):
        assert utils._offset_for_intersecting_pair(pair, 10) == offset

    @pytest.mark.parametrize("pair,offset", OFFSET_INTERSECTING_PAIR_SAMPLES[3])
    def test_offset_for_intersecting_pair_corner_3_functionality(self, pair, offset):
        assert utils._offset_for_intersecting_pair(pair, 10) == offset

    ## check_intersections
    def test_check_intersections_single_calls_intersects_and_returns_False(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.utils._intersects", return_value=False)
        sample_sources = utils.get_snapping_sources_for_rect((50, 20, 200, 20), 10)
        sample_targets1 = utils.get_snapping_sources_for_rect((300, 100, 200, 120), 10)
        sample_targets2 = utils.get_snapping_sources_for_rect((520, 400, 850, 420), 10)
        result = utils.check_intersections(
            sample_sources, [sample_targets1, sample_targets2]
        )
        assert mocked.call_count == 16
        assert result == False

    def test_check_intersections_calls_intersects_twice_and_returns_two_tuple(
        self, mocker
    ):
        mocked = mocker.patch("arrangeit.utils._intersects", return_value=True)
        sample_sources = utils.get_snapping_sources_for_rect((50, 20, 200, 20), 10)
        sample_targets1 = utils.get_snapping_sources_for_rect((300, 100, 200, 120), 10)
        sample_targets2 = utils.get_snapping_sources_for_rect((520, 400, 850, 420), 10)
        result = utils.check_intersections(
            sample_sources, [sample_targets1, sample_targets2]
        )
        assert mocked.call_count == 2
        assert result == (
            ((40, 10, 260, 30), (290, 90, 510, 110)),
            ((240, 10, 260, 50), (490, 90, 510, 230)),
        )

    @pytest.mark.parametrize("sources,targets,expected", SAMPLE_CHECK_INTERSECTIONS)
    def test_check_intersections_single_functionality_for_full_sources(
        self, sources, targets, expected
    ):
        assert utils.check_intersections(sources, targets) == expected[0]

    @pytest.mark.parametrize("sources,targets,expected", SAMPLE_CHECK_INTERSECTIONS)
    def test_check_intersections_single_functionality_for_two_sources_corner_0(
        self, sources, targets, expected
    ):
        assert (
            utils.check_intersections((sources[0], sources[3]), targets) == expected[1]
        )

    @pytest.mark.parametrize("sources,targets,expected", SAMPLE_CHECK_INTERSECTIONS)
    def test_check_intersections_single_functionality_for_two_sources_corner_1(
        self, sources, targets, expected
    ):
        assert (
            utils.check_intersections((sources[0], sources[1]), targets) == expected[2]
        )

    @pytest.mark.parametrize("sources,targets,expected", SAMPLE_CHECK_INTERSECTIONS)
    def test_check_intersections_single_functionality_for_two_sources_corner_2(
        self, sources, targets, expected
    ):
        assert (
            utils.check_intersections((sources[2], sources[1]), targets) == expected[3]
        )

    @pytest.mark.parametrize("sources,targets,expected", SAMPLE_CHECK_INTERSECTIONS)
    def test_check_intersections_single_functionality_for_two_sources_corner_3(
        self, sources, targets, expected
    ):
        assert (
            utils.check_intersections((sources[2], sources[3]), targets) == expected[4]
        )

    ## offset_for_intersections
    def test_offset_for_intersections_returns_empty_tuple_for_no_rectangles(
        self, mocker
    ):
        assert utils.offset_for_intersections(False, 10) == (0, 0)

    def test_offset_for_intersections_calls__offset_once_for_single_pair(self, mocker):
        mocked = mocker.patch("arrangeit.utils._offset_for_intersecting_pair")
        RECTS, SNAP = [(1732, 36, 1752, 316), (1725, 22, 1745, 868)], 10
        utils.offset_for_intersections(RECTS, SNAP)
        mocked.assert_called_once()
        mocked.assert_called_with(RECTS, SNAP)

    def test_offset_for_intersections_calls__offset_twice_for_two_pairs(self, mocker):
        mocked = mocker.patch("arrangeit.utils._offset_for_intersecting_pair")
        RECTS = [
            ((1732, 36, 1752, 316), (1725, 22, 1745, 868)),
            ((257, 52, 747, 72), (169, 51, 1123, 71)),
        ]
        SNAP = 10
        utils.offset_for_intersections(RECTS, SNAP)
        calls = [mocker.call(RECTS[1], SNAP)]
        mocked.assert_has_calls(calls, any_order=True)
        calls = [mocker.call(RECTS[0], SNAP)]
        mocked.assert_has_calls(calls, any_order=True)

    def test_offset_for_intersections_returns_opposite_tuple_element(self, mocker):
        SAMPLE = (7, 5)
        mocker.patch("arrangeit.utils._offset_for_intersecting_pair", return_value=SAMPLE)
        RECTS = [
            ((1732, 36, 1752, 316), (1725, 22, 1745, 868)),
            ((257, 52, 747, 72), (169, 51, 1123, 71)),
        ]
        SNAP = 10
        returned = utils.offset_for_intersections(RECTS, SNAP)
        assert returned == (SAMPLE[0], SAMPLE[1])
