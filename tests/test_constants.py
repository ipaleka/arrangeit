import pytest
from PIL import Image

from arrangeit import constants




class TestConstants(object):
    """Unit testing class checking availability of global """

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
            ("TITLE_LABEL_RELWIDTH", float),
            ("TITLE_LABEL_RELHEIGHT", float),
            ("ICON_WIDTH", int),
            ("NAME_LABEL_RELHEIGHT", float),
            ("NAME_LABEL_RELWIDTH", float),
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
            ("WORKSPACES_FRAME_RELHEIGHT", float),
            ("WORKSPACES_FRAME_RELWIDTH", float),
            ("WORKSPACE_LABEL_ANCHOR", str),
            ("WORKSPACE_LABEL_BG", str),
            ("WORKSPACE_LABEL_FG", str),
            ("WORKSPACE_TITLE_NAME_FONT_INCREASE", float),
            ("WORKSPACE_LABEL_PADX", int),
            ("WORKSPACE_LABEL_PADY", int),
            ("WINDOWS_LIST_RELHEIGHT", float),
            ("WINDOWS_LIST_RELWIDTH", float),
            ("LISTED_WINDOW_RELWIDTH", float),
            ("LISTED_WINDOW_RELHEIGHT", float),
            ("LISTED_WINDOW_LABEL_ANCHOR", str),
            ("LISTED_WINDOW_LABEL_BG", str),
            ("LISTED_WINDOW_LABEL_FG", str),
            ("LISTED_WINDOW_NAME_FONT_INCREASE", float),
            ("LISTED_WINDOW_LABEL_PADX", int),
            ("LISTED_WINDOW_LABEL_PADY", int),
            ("LISTED_ICON_LABEL_ANCHOR", str),
            ("LISTED_ICON_LABEL_BG", str),
            ("LISTED_ICON_LABEL_PADX", int),
            ("LISTED_ICON_LABEL_PADY", int),
            ("LOCATE", int),
            ("RESIZE", int),
            ("OTHER", int),
            ("BLANK_ICON", Image.Image)
        ],
    )
    def test_constants_for_name_and_typ(self, constant, typ):
        assert getattr(constants, constant) is not None
        assert isinstance(getattr(constants, constant), typ)
