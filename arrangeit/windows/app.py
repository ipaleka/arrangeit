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

from PIL import ImageTk

from win32con import SW_MINIMIZE, SW_RESTORE
from win32gui import IsIconic, MoveWindow, SetActiveWindow, ShowWindow

from arrangeit.base import BaseApp
from arrangeit.settings import Settings

import ctypes
import ctypes.wintypes


class App(BaseApp):
    """Main app class with MS Windows specific code."""

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
            self.move_to_workspace(hwnd, model.changed_ws)
        if model.is_changed:
            if IsIconic(hwnd):
                ShowWindow(hwnd, SW_RESTORE)
            MoveWindow(hwnd, *model.changed, True)
            if not model.restored:
                ShowWindow(hwnd, SW_MINIMIZE)
            return False
        return True

    def move_to_workspace(self, hwnd, number):
        """TODO implement"""
        pass

    ## COMMANDS
    def grab_window_screen(self, model, root_hwnd=None):
        """TODO implement

        :param model: model of the window we want screenshot from
        :type model: :class:`WindowModel`
        :returns: :class:`PIL.ImageTk.PhotoImage`
        """
        if self.collector.api.dwm_is_composition_enabled():
            return ImageTk.PhotoImage(self.thumbnail(root_hwnd, model)), (0, 0)
        return ImageTk.PhotoImage(Settings.BLANK_ICON), (0, 0)

    def thumbnail(self, root_hwnd, model):
        self.thumbnail_id = ctypes.wintypes.HANDLE()
        # ret_val = ctypes.windll.dwmapi.DwmRegisterThumbnail(
        #     root_hwnd, model.wid, ctypes.byref(self.thumbnail_id)
        # )
        ret_val = self.collector.api.helpers._dwm_register_thumbnail(
            root_hwnd, model.wid, ctypes.byref(self.thumbnail_id)
        )
        print(hex(ret_val), "start:", self.thumbnail_id, root_hwnd, model.wid)

        from arrangeit.windows.api import DWM_THUMBNAIL_PROPERTIES

        DWM_TNP_RECTDESTINATION = 0x00000001
        DWM_TNP_RECTSOURCE = 0x00000002
        DWM_TNP_OPACITY = 0x00000004
        DWM_TNP_VISIBLE = 0x00000008
        DWM_TNP_SOURCECLIENTAREAONLY = 0x00000010

        destination_rect = ctypes.wintypes.RECT()
        destination_rect.left = 0
        destination_rect.top = 0
        destination_rect.right = model.w
        destination_rect.bottom = model.h
        opacity = ctypes.wintypes.BYTE(255)  # (255 * 70)/100

        properties = DWM_THUMBNAIL_PROPERTIES()
        properties.dwFlags = (
            DWM_TNP_SOURCECLIENTAREAONLY
            | DWM_TNP_VISIBLE
            | DWM_TNP_OPACITY
            | DWM_TNP_RECTDESTINATION
        )
        properties.rcDestination = destination_rect
        properties.opacity = opacity
        properties.fVisible = True
        properties.fSourceClientAreaOnly = False
        # ret_val = ctypes.windll.dwmapi.DwmUpdateThumbnailProperties(
        #     self.thumbnail_id, ctypes.byref(properties)
        # )
        ret_val = self.collector.api.helpers._dwm_update_thumbnail_properties(
            self.thumbnail_id, ctypes.byref(properties)
        )
        print(hex(ret_val), "update:", self.thumbnail_id)

        from win32gui import GetWindowRect
        from PIL import ImageGrab

        bbox = GetWindowRect(root_hwnd)
        img = ImageGrab.grab(bbox)

        # ret_val = ctypes.windll.dwmapi.DwmUnregisterThumbnail(self.thumbnail_id)
        ret_val = self.collector.api.helpers._dwm_unregister_thumbnail(
            self.thumbnail_id
        )
        print(hex(ret_val), "unregister:", self.thumbnail_id)
        return img
