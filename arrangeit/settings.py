# arrangeit - cross-platform desktop utility for easy windows management
# Copyright (C) 1999-2019 Ivica Paleka

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import json
import os
from gettext import gettext as _

from PIL import Image

from arrangeit.utils import open_image, platform_user_data_path

"""
DO NOT EDIT SETTINGS IN THIS FILE FOR USER SIDE CONFIGURATION - for such purpose use
user_settings.json file created and located in arrangeit user data directory.
"""

MESSAGES = {
    "default_saved": _("Collected windows data saved to default file."),
    "msg_release_mouse": _("Mouse middle click or Space for cursor release"),
    "msg_capture_mouse": _("Click title or icon to restart positioning"),
}


SETTINGS = {
    "MIN_WIDTH": (int, 100),
    "MIN_HEIGHT": (int, 40),
    "MOUSE_CHECK_INTERVAL": (int, 5),
    "SAVE_ON_EXIT": (bool, False),
    "SHIFT_CURSOR": (int, 6),
    "SNAP_PIXELS": (int, 2),
    "SNAPPING_IS_ON": (bool, True),
    "SNAP_INCLUDE_SELF": (bool, False),
    "SCREENSHOT_SHIFT_PIXELS": (int, -1),
    "SCREENSHOT_BLUR_PIXELS": (int, 2),
    "SCREENSHOT_TO_GRAYSCALE": (bool, True),
    "TRANSPARENCY_IS_ON": (bool, True),
    "ROOT_ALPHA": (float, 0.9),
    "ROOT_SIZE_DENOMINATOR": (int, 4),  # 3-6
    "DEFAULT_CURSOR": (str, "arrow"),
    "SELECT_CURSOR": (str, "hand2"),
    "CORNER_CURSOR": (tuple, ("ul_angle", "ur_angle", "lr_angle", "ll_angle")),
    "CORNER_COLOR": (str, "SkyBlue1"),
    "SELECTED_COLOR": (str, "SkyBlue1"),
    "HIGHLIGHTED_COLOR": (str, "red"),
    "MAIN_BG": (str, "white"),
    "MAIN_FG": (str, "black"),
    "TITLE_LABEL_RELHEIGHT": (float, 0.25),
    "TITLE_LABEL_RELWIDTH": (float, 0.75),
    "TITLE_LABEL_ANCHOR": (str, "w"),
    "TITLE_LABEL_BG": (str, "LightGoldenrodYellow"),
    "TITLE_LABEL_FG": (str, "black"),
    "TITLE_LABEL_FONT_INCREASE": (float, 0.1),
    "TITLE_LABEL_HEIGHT": (int, 3),
    "TITLE_LABEL_PADX": (int, 12),
    "TITLE_LABEL_PADY": (int, 6),
    "PROPERTY_ICON_SIZE": (int, 16),
    "PROPERTY_ICON_PADX": (int, 4),
    "PROPERTY_ICON_PADY": (int, 4),
    "ICON_LABEL_ANCHOR": (str, "n"),
    "ICON_LABEL_BG": (str, "white"),
    "ICON_LABEL_PADX": (int, 2),
    "ICON_LABEL_PADY": (int, 1),
    "NAME_LABEL_RELHEIGHT": (float, 0.25),
    "NAME_LABEL_RELWIDTH": (float, 0.25),
    "NAME_LABEL_ANCHOR": (str, "s"),
    "NAME_LABEL_BG": (str, "white"),
    "NAME_LABEL_FG": (str, "black"),
    "NAME_LABEL_HEIGHT": (int, 2),
    "NAME_LABEL_PADX": (int, 2),
    "NAME_LABEL_PADY": (int, 0),
    "WORKSPACES_FRAME_RELHEIGHT": (float, 0.62),
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
    "WINDOWS_LIST_RELHEIGHT": (float, 0.68),
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
    "STATUSBAR_RELHEIGHT": (float, 0.07),
    "STATUSBAR_RELWIDTH": (float, 0.75),
    "STATUSBAR_BG": (str, "white"),
    "STATUSBAR_FG": (str, "black"),
    "STATUSBAR_LABEL_FONT_INCREASE": (float, -0.25),
    "STATUSBAR_LABEL_ANCHOR": (str, "center"),
    "STATUSBAR_LABEL_HEIGHT": (int, 1),
    "STATUSBAR_LABEL_PADX": (int, 4),
    "STATUSBAR_LABEL_PADY": (int, 0),
    "TOOLBAR_RELHEIGHT": (float, 0.15),
    "TOOLBAR_RELWIDTH": (float, 0.25),
    "TOOLBAR_BG": (str, "white"),
    "TOOLBAR_BUTTON_FONT_INCREASE": (float, -0.1),
    "TOOLBAR_BUTTON_SHRINK_HEIGHT": (float, 0.05),
    "TOOLBAR_BUTTON_SHRINK_WIDTH": (float, 0.04),
    "OPTIONS_BUTTON_RELHEIGHT": (float, 0.7),
    "OPTIONS_BUTTON_RELWIDTH": (float, 0.5),
    "OPTIONS_BUTTON_ANCHOR": (str, "nw"),
    "QUIT_BUTTON_RELHEIGHT": (float, 0.7),
    "QUIT_BUTTON_RELWIDTH": (float, 0.45),
    "QUIT_BUTTON_ANCHOR": (str, "nw"),
    "OPTIONS_WIDGETS_PADX": (int, 4),
    "OPTIONS_WIDGETS_PADY": (int, 2),
    "OPTIONS_MESSAGE_HEIGHT": (int, 2),
    "OPTIONS_TIMER_DELAY": (int, 5000),
    "ABOUT_LOGO_SIZE": (tuple, (400, 128)),
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
        if key in SETTINGS.keys() and isinstance(value, SETTINGS[key][0])
    }


class SettingsMetaclass(type):
    """Meta class needed to access Settings class attributes by names."""

    def __getattr__(self, name):
        """Returns value for provided attribute name.

        It first tries to get the value from user settings.
        If user hasn't configured attribute then program setting is returned.
        """
        value = self.user_settings.get(name)
        return value if value is not None else SETTINGS.get(name, [None, None])[1]


class Settings(metaclass=SettingsMetaclass):
    """Class holding all the program's constants and settings."""

    user_settings = validate_user_settings()
    LOCATE = 0
    RESIZE = 10
    OTHER = 100
    WINDOW_MODEL_TYPES = {
        "wid": int,
        "rect": (int, int, int, int),
        "resizable": bool,
        "restored": bool,
        "title": str,
        "name": str,
        "icon": Image.Image,
        "workspace": int,
    }
    WINDOW_MODEL_RECT_ELEMENTS = ("x", "y", "w", "h")
    ICON_SIZE = 32
    BLANK_ICON = open_image("blank.png")
    CORNER_RECT_INDEXES = [(0, 3), (0, 1), (2, 1), (2, 3)]
    HELP_PAGE_URL = (
        "https://github.com/ipaleka/arrangeit/blob/master/docs/userguide.rst"
    )
    RELEASES_PAGE_URL = "https://github.com/ipaleka/arrangeit/releases"

    @classmethod
    def is_setting(cls, name, value):
        """Returns True if provided name with value is valid setting.

        :param name: setting name
        :type name: str
        :param value: value to check type for
        :type value: str/int/float
        :returns: Boolean
        """
        return not (name not in SETTINGS or not isinstance(value, SETTINGS[name][0]))

    @classmethod
    def setting_type(cls, name):
        """Returns type of setting with provided name.

        :param name: setting name
        :type name: str
        :returns: type
        """
        return SETTINGS.get(name, (None, None))[0]

    @classmethod
    def color_group(cls, group):
        """Returns all the Settings members which names end with provided name.

        :param group: setting name
        :type group: str
        :returns: list
        """
        return [key for key in SETTINGS.keys() if key.endswith(group)]
