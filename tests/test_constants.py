import pytest

from arrangeit import constants


class TestConstants(object):
    """Unit testing class checking availability of global constants."""

    @pytest.mark.parametrize(
        "constant,typ",
        [
            ("WINDOW_MODEL_TYPES", dict),
            ("WINDOW_RECT_ELEMENTS", tuple),
            ("WINDOW_SHIFT_PIXELS", int),
            ("TITLE_LABEL_FG", str),
            ("TITLE_LABEL_BG", str),
            ("TITLE_LABEL_ANCHOR", str),
            ("TITLE_LABEL_PADX", int),
            ("TITLE_LABEL_PADY", int),
            ("LOCATE", int),
            ("RESIZE", int),
            ("OTHER", int),
            ("WINDOW_MIN_WIDTH", int),
            ("WINDOW_MIN_HEIGHT", int),
        ],
    )
    def test_constants_for_name_and_typ(self, constant, typ):
        assert getattr(constants, constant) is not None
        assert isinstance(getattr(constants, constant), typ)
