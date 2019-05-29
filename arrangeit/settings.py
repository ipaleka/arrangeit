import os
import json

from PIL import Image

from arrangeit.utils import platform_user_data_path


"""
DO NOT EDIT THIS FILE FOR USER SIDE CONFIGURATION - for such purpose use
user_settings.json file created and located in arrangeit user data directory.
"""

CONSTANTS = {
    "LOCATE": (int, 0),
    "RESIZE": (int, 1),
    "OTHER": (int, 2),
    "BLANK_ICON": (
        Image.Image,
        Image.open(os.path.join(os.path.dirname(__file__), "resources", "blank.png")),
    ),
    "WINDOW_MODEL_TYPES": (
        dict,
        {
            "wid": int,
            "rect": (int, int, int, int),
            "resizable": bool,
            "title": str,
            "name": str,
            "icon": Image.Image,
            "workspace": int,
        },
    ),
    "WINDOW_MODEL_RECT_ELEMENTS": (tuple, ("x", "y", "w", "h")),
    "WINDOW_MIN_WIDTH": (int, 100),
    "WINDOW_MIN_HEIGHT": (int, 40),
    "WINDOW_SHIFT_PIXELS": (int, 2),
    "SCREENSHOT_SHIFT_PIXELS": (int, -1),
    "ROOT_ALPHA": (float, 0.8),
    "DEFAULT_CURSOR": (str, "arrow"),
    "SELECT_CURSOR": (str, "hand2"),
    "SELECTED_COLOR": (str, "blue"),
    "HIGHLIGHTED_COLOR": (str, "red"),
    "TITLE_LABEL_RELHEIGHT": (float, 0.25),
    "TITLE_LABEL_RELWIDTH": (float, 0.75),
    "TITLE_LABEL_ANCHOR": (str, "w"),
    "TITLE_LABEL_BG": (str, "white"),
    "TITLE_LABEL_FG": (str, "black"),
    "TITLE_LABEL_FONT_INCREASE": (float, 0.1),
    "TITLE_LABEL_HEIGHT": (int, 3),
    "TITLE_LABEL_PADX": (int, 12),
    "TITLE_LABEL_PADY": (int, 6),
    "ICON_WIDTH": (int, 32),
    "ICON_LABEL_ANCHOR": (str, "n"),
    "ICON_LABEL_BG": (str, "white"),
    "ICON_LABEL_PADX": (int, 2),
    "ICON_LABEL_PADY": (int, 2),
    "NAME_LABEL_RELHEIGHT": (float, 0.25),
    "NAME_LABEL_RELWIDTH": (float, 0.25),
    "NAME_LABEL_ANCHOR": (str, "s"),
    "NAME_LABEL_BG": (str, "white"),
    "NAME_LABEL_FG": (str, "black"),
    "NAME_LABEL_HEIGHT": (int, 3),
    "NAME_LABEL_PADX": (int, 2),
    "NAME_LABEL_PADY": (int, 10),
    "WORKSPACES_FRAME_RELHEIGHT": (float, 0.60),
    "WORKSPACES_FRAME_RELWIDTH": (float, 0.25),
    "WORKSPACE_NUMBER_RELHEIGHT": (float, 0.75),
    "WORKSPACE_NUMBER_RELWIDTH": (float, 1.0),
    "WORKSPACE_NUMBER_LABEL_ANCHOR": (str, "center"),
    "WORKSPACE_NUMBER_LABEL_BG": (str, "white"),
    "WORKSPACE_NUMBER_LABEL_FG": (str, "black"),
    "WORKSPACE_NUMBER_FONT_INCREASE": (float, 0.8),
    "WORKSPACE_NUMBER_LABEL_PADX": (int, 2),
    "WORKSPACE_NUMBER_LABEL_PADY": (int, 2),
    "WORKSPACE_NAME_RELHEIGHT": (float, 0.25),
    "WORKSPACE_NAME_RELWIDTH": (float, 1.0),
    "WORKSPACE_NAME_LABEL_ANCHOR": (str, "center"),
    "WORKSPACE_NAME_LABEL_HEIGHT": (int, 2),
    "WORKSPACE_NAME_LABEL_BG": (str, "white"),
    "WORKSPACE_NAME_LABEL_FG": (str, "black"),
    "WORKSPACE_NAME_FONT_INCREASE": (float, -0.4),
    "WORKSPACE_NAME_LABEL_PADX": (int, 0),
    "WORKSPACE_NAME_LABEL_PADY": (int, 0),
    "WINDOWS_LIST_RELHEIGHT": (float, 0.75),
    "WINDOWS_LIST_RELWIDTH": (float, 0.75),
    "WINDOWS_LIST_BG": (str, "white"),
    "LISTED_WINDOW_RELHEIGHT": (float, 0.125),
    "LISTED_WINDOW_RELWIDTH": (float, 0.95),
    "LISTED_WINDOW_LABEL_ANCHOR": (str, "w"),
    "LISTED_WINDOW_LABEL_BG": (str, "white"),
    "LISTED_WINDOW_LABEL_FG": (str, "black"),
    "LISTED_WINDOW_NAME_FONT_INCREASE": (float, -0.1),
    "LISTED_WINDOW_LABEL_PADX": (int, 2),
    "LISTED_WINDOW_LABEL_PADY": (int, 2),
    "LISTED_ICON_LABEL_ANCHOR": (str, "w"),
    "LISTED_ICON_LABEL_BG": (str, "white"),
    "LISTED_ICON_LABEL_PADX": (int, 4),
    "LISTED_ICON_LABEL_PADY": (int, 0),
    "TOOLBAR_RELHEIGHT": (float, 0.15),
    "TOOLBAR_RELWIDTH": (float, 0.25),
    "TOOLBAR_BG": (str, "white"),
    "TOOLBAR_BUTTON_FONT_INCREASE": (float, -0.1),
    "TOOLBAR_BUTTON_SHRINK_HEIGHT": (float, 0.2),
    "TOOLBAR_BUTTON_SHRINK_WIDTH": (float, 0.04),
    "OPTIONS_BUTTON_RELHEIGHT": (float, 1.0),
    "OPTIONS_BUTTON_RELWIDTH": (float, 0.5),
    "OPTIONS_BUTTON_ANCHOR": (str, "nw"),
    "QUIT_BUTTON_RELHEIGHT": (float, 1.0),
    "QUIT_BUTTON_RELWIDTH": (float, 0.5),
    "QUIT_BUTTON_ANCHOR": (str, "nw"),
}


def read_user_settings():
    """Reads and returns user settings data from user home directory.

    :returns: dict
    """
    settings_file = os.path.join(platform_user_data_path(), "user_settings.json")
    if os.path.exists(settings_file):
        with open(settings_file, "r") as json_settings:
            try:
                data = json.load(json_settings)
            except json.JSONDecodeError:
                data = {}
        return data
    return {}


def validate_user_settings():
    """Reads, validates and returns dictionary of user settings.

    :returns: dict {name: value}
    """
    return {
        key: value
        for key, value in read_user_settings().items()
        if key in CONSTANTS.keys() and isinstance(value, CONSTANTS[key][0])
    }


class SettingsMetaclass(type):
    """Meta class needed to access Settings class attributes by names."""

    def __getattr__(self, name):
        """Returns value for provided attribute name.

        It first tries to get the value from user settings.
        If user hasn't configured attribute then program constant is returned.
        """
        value = self.user_settings.get(name)
        return value if value is not None else CONSTANTS[name][1]


class Settings(metaclass=SettingsMetaclass):
    """Class holding all the program's constants and settings."""

    user_settings = validate_user_settings()

