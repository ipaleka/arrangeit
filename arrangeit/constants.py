import os

from PIL import Image


WINDOW_MODEL_TYPES = {
    "wid": int,
    "rect": (int, int, int, int),
    "resizable": bool,
    "title": str,
    "name": str,
    "icon": Image.Image,
}
WINDOW_RECT_ELEMENTS = ("x", "y", "w", "h")

ROOT_ALPHA = 0.99  # 0.8

WINDOW_SHIFT_PIXELS = 2

TITLE_LABEL_ANCHOR = "w"
TITLE_LABEL_BG = "white"
TITLE_LABEL_FG = "black"
TITLE_LABEL_FONT_INCREASE = 0.1
TITLE_LABEL_HEIGHT = 3
TITLE_LABEL_PADX = 12
TITLE_LABEL_PADY = 6

ICON_WIDTH = 32
ICON_WIDTH_FRACTION = 0.25

ICON_LABEL_ANCHOR = "w"
ICON_LABEL_BG = "white"
ICON_LABEL_PADX = 2
ICON_LABEL_PADY = 2

NAME_LABEL_ANCHOR = "center"
NAME_LABEL_BG = "white"
NAME_LABEL_FG = "black"
NAME_LABEL_HEIGHT = 3
NAME_LABEL_PADX = 2
NAME_LABEL_PADY = 2

LOCATE, RESIZE, OTHER = 0, 1, 2
WINDOW_MIN_WIDTH = 100
WINDOW_MIN_HEIGHT = 40

BLANK_ICON = Image.open(
    os.path.join(os.path.dirname(__file__), "resources", "blank.png")
)
