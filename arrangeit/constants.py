WINDOW_MODEL_TYPES = {
    "wid": int,
    "rect": (int, int, int, int),
    "resizable": bool,
    "title": str,
    "name": str,
}
WINDOW_RECT_ELEMENTS = ("x", "y", "w", "h")

ROOT_ALPHA = 0.8

WINDOW_SHIFT_PIXELS = 2

TITLE_LABEL_FG = "black"
TITLE_LABEL_BG = "white"
TITLE_LABEL_ANCHOR = "nw"
TITLE_LABEL_PADX = 12
TITLE_LABEL_PADY = 6

LOCATE, RESIZE, OTHER = 0, 1, 2