import pytest
from PIL import Image

from arrangeit import constants


class TestConstants(object):
    """Unit testing class checking availability of global constants."""

    @pytest.mark.parametrize(
        "constant,typ",
        [
            ("TITLE_LABEL_ANCHOR", str),
            ("TITLE_LABEL_BG", str),
            ("TITLE_LABEL_FG", str),
            ("TITLE_LABEL_FONT_INCREASE", float),
            ("TITLE_LABEL_HEIGHT", int),
            ("TITLE_LABEL_PADX", int),
            ("TITLE_LABEL_PADY", int),
            ("ICON_WIDTH", int),
            ("ICON_WIDTH_FRACTION", float),
            ("ICON_LABEL_BG", str),
            ("ICON_LABEL_ANCHOR", str),
            ("ICON_LABEL_PADX", int),
            ("ICON_LABEL_PADY", int),
            ("NAME_LABEL_ANCHOR", str),
            ("NAME_LABEL_BG", str),
            ("NAME_LABEL_FG", str),
            ("NAME_LABEL_HEIGHT", int),
            ("NAME_LABEL_PADX", int),
            ("NAME_LABEL_PADY", int),
            ("WINDOW_MIN_WIDTH", int),
            ("WINDOW_MIN_HEIGHT", int),
            ("WINDOW_MODEL_TYPES", dict),
            ("WINDOW_RECT_ELEMENTS", tuple),
            ("WINDOW_SHIFT_PIXELS", int),
            ("LOCATE", int),
            ("RESIZE", int),
            ("OTHER", int),
            ("BLANK_ICON", Image.Image)
        ],
    )
    def test_constants_for_name_and_typ(self, constant, typ):
        assert getattr(constants, constant) is not None
        assert isinstance(getattr(constants, constant), typ)
