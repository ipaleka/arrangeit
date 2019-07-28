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

import locale
import os

from PIL import ImageGrab, ImageTk
from win32con import SW_MINIMIZE, SW_RESTORE
from win32gui import IsIconic, MoveWindow, SetActiveWindow, ShowWindow

# gettext requirement on MS Windows
if os.getenv("LANG") is None:
    os.environ["LANG"] = locale.getdefaultlocale()[0]

from arrangeit.base import BaseApp
from arrangeit.settings import Settings
from arrangeit.utils import Rectangle, get_prepared_screenshot


class App(BaseApp):
    """Main app class with MS Windows specific code."""

    thumbnails = ()

    ## TASKS
    def activate_root(self, hwnd):
        """Activates/focuses root window identified by provided ``hwnd``."""
        SetActiveWindow(hwnd)

    def move(self, hwnd):
        """Just calls :func:`move_and_resize` as the same method moves and resizes

        under MS Windows.

        :param hwnd: windows id
        :type hwnd: int
        """
        return self.move_and_resize(hwnd)

    def move_and_resize(self, hwnd):
        """Moves and resizes window identified by provided hwnd.

        :param hwnd: root id got from Tkinter
        :type hwnd: int
        :var model: collected window data
        :type model: :class:`WindowModel`
        :returns: Boolean
        """
        model = self.collector.collection.get_model_by_wid(hwnd)
        if model.is_ws_changed:
            self.move_other_to_workspace(hwnd, model.changed_ws)
        if model.is_changed:
            if IsIconic(hwnd):
                ShowWindow(hwnd, SW_RESTORE)
            MoveWindow(hwnd, *model.changed, True)
            if not model.restored:
                ShowWindow(hwnd, SW_MINIMIZE)
            return False
        return True

    def move_other_to_workspace(self, hwnd, number):
        """Moves other process' window to provided workspace number.

        :param hwnd: identifier of the window to move
        :type hwnd: int
        :param number: workspace number
        :type number: int
        """
        return self.collector.api.move_other_window_to_desktop(hwnd, number)

    def move_to_workspace(self, hwnd, number):
        """Moves root window to provided workspace number.

        :param hwnd: root id got from Tkinter
        :type hwnd: int
        :param number: workspace number
        :type number: int
        """
        return self.collector.api.move_own_window_to_desktop(hwnd, number)

    def screenshot_cleanup(self, *args):
        """Unregisters DWM thumbnails kept in instance's ``thumbnails`` attribute.

        :var thumbnail: DWM thumbnail identifier
        :type thumbnail: int
        """
        for thumbnail in self.thumbnails:
            self.collector.api.unregister_thumbnail(thumbnail)
        self.thumbnails = ()

    ## COMMANDS
    def _screenshot_with_thumbnails(self, model, root_wid):
        """Takes and returns screenshot of root window after DWM thumbnails are created

        and updated. First thumbnail is created below rect of root with default size
        and the other is created on the root's right. Thumbnails are unregistered
        after screenshot is taken.

        :param model: model of the window we want thumbnail from
        :type model: :class:`WindowModel`
        :param root_wid: root window identifier
        :type root_wid: int
        :var width: initial width of root window
        :type width: int
        :var height: initial height of root window
        :type height: int
        :var lower_thumbnail: DWM thumbnail below root with default size
        :type lower_thumbnail: int
        :var right_thumbnail: DWM thumbnail on the right of root with default size
        :type right_thumbnail: int
        :var screenshot: screenshot of root window with thumbnails in it
        :type screenshot: :class:`PIL.Image.Image`
        :returns: :class:`PIL.Image.Image`
        """
        width, height = self.controller.default_size
        lower_thumbnail = self.collector.api.setup_thumbnail(
            model.wid, root_wid, Rectangle(0, height, width, model.h)
        )
        if lower_thumbnail is None:
            return Settings.BLANK_ICON

        right_thumbnail = self.collector.api.setup_thumbnail(
            model.wid, root_wid, Rectangle(width, 0, model.w, model.h)
        )
        if right_thumbnail is None:
            return Settings.BLANK_ICON

        self.thumbnails = (lower_thumbnail, right_thumbnail)

        return self._window_area_desktop_screenshot(root_wid)

    def _window_area_desktop_screenshot(self, hwnd):
        """Takes desktop screenshot of the area occupied by window with given hwnd.

        :param hwnd: root window identifier
        :type hwnd: int
        :returns: :class:`PIL.Image.Image`
        """
        return ImageGrab.grab(self.collector.api.extended_frame_rect(hwnd))

    def grab_window_screen(self, model, root_wid=None):
        """Setups and returns screenshot of the window from provided model.

        If DWM composition settings allows then surface of model window
        is taken from root window after thumbnails are created in it.

        TODO check why this (-1, -1) fits

        :param model: model of the window we want screenshot from
        :type model: :class:`WindowModel`
        :param root_wid: root window identifier
        :type root_wid: int
        :returns: (:class:`PIL.ImageTk.PhotoImage`, (int, int))
        """
        if self.collector.api.is_dwm_composition_enabled():
            return (
                get_prepared_screenshot(
                    self._screenshot_with_thumbnails(model, root_wid),
                    blur_size=Settings.SCREENSHOT_BLUR_PIXELS,
                    grayscale=Settings.SCREENSHOT_TO_GRAYSCALE,
                ),
                (-1, -1),
            )
        return ImageTk.PhotoImage(Settings.BLANK_ICON), (0, 0)
