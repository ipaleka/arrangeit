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

import gi
from PIL import ImageTk
from Xlib import X

from arrangeit.base import BaseApp
from arrangeit.settings import Settings
from arrangeit.utils import get_prepared_screenshot

gi.require_version("Gdk", "3.0")
gi.require_version("Wnck", "3.0")
from gi.repository import Gdk, Wnck


class App(BaseApp):
    """Main app class with GNU/Linux specific code."""

    ## TASKS
    def activate_root(self, wid):
        """Activates/focuses root window identified by provided ``wid``.

        FIXME possible nasty hack wid+1

        :param wid: windows id
        :type wid: int
        """
        window = self._window_from_wid(wid + 1)
        if window is not None:
            window.focus(X.CurrentTime)

    def move(self, wid):
        """Just calls :func:`move_and_resize` as the same method moves and resizes

        in Wnck.Window class under GNU/Linux.

        :param wid: windows id
        :type wid: int
        :returns: Boolean
        """
        return self.move_and_resize(wid)

    def move_and_resize(self, wid):
        """Moves and resizes window identified by provided wid.

        Gravity stays the same (Wnck.WindowGravity.CURRENT) and the other arguments
        are calculated/retrieved from model where ``changed`` attribute holds needed data.

        If returned ``mask`` is False then wee don't need to do anything more.

        :param wid: windows id
        :type wid: int
        :var model: window data
        :type model: :class:`WindowModel` instance
        :var mask: combination of bits holding information what is changed
        :type mask: :class:`Wnck.WindowMoveResizeMask` flag
        :var win: window instance
        :type win: :class:`Wnck.Window` object
        :returns: Boolean
        """
        model = self.collector.collection.get_model_by_wid(wid)
        if model.is_ws_changed:
            self._move_window_to_workspace(wid, model.changed_ws)

        win = self.collector.get_window_by_wid(wid)

        if model.restored and win.is_minimized():
            win.unminimize(X.CurrentTime)
        elif not model.restored and not win.is_minimized():
            win.minimize()

        mask = self.collector.get_window_move_resize_mask(model)
        if mask:
            if win.is_maximized():
                win.unmaximize()
            win.set_geometry(Wnck.WindowGravity.STATIC, mask, *model.changed)
            return False
        return True

    def move_to_workspace(self, wid, number):
        """Moves root window to provided custom workspace number.

        Calls :func:`_move_window_to_workspace` with wid increased by 1.

        FIXME possible nasty hack wid+1

        :param wid: root id got from Tkinter
        :type wid: int
        :param number: our custom workspace number
        :type number: int
        """
        return self._move_window_to_workspace(wid + 1, number)

    ## HELPERS
    def _activate_workspace(self, number):
        """Activates workspace identified by provided our custom workspace number.

        :param number: our custom workspace number
        :type number: int
        :var workspace: workspace to move to
        :type workspace: :class:`Wnck.Workspace`
        :returns: :class:`Wnck.Workspace`
        """
        workspace = self.collector.get_wnck_workspace_for_custom_number(number)
        if workspace:
            workspace.activate(X.CurrentTime)
            return workspace
        return True

    def _move_window_to_workspace(self, wid, number):
        """Moves window with provided wid to provided custom workspace number.

        It shutdowns Wnck in beginning as this is the only method that uses Wnck
        after initial windows collecting - without shutdown wid is not recognized.

        :param wid: windows id
        :type wid: int
        :param number: our custom workspace number
        :type number: int
        :var workspace: workspace to move to
        :type workspace: :class:`Wnck.Workspace`
        :var win: window instance
        :type win: :class:`Wnck.Window`
        :returns: Boolean
        """
        Wnck.shutdown()
        workspace = self._activate_workspace(number)
        if workspace:
            win = self.collector.get_window_by_wid(wid)
            win.move_to_workspace(workspace)
            # FIXME X.CurrentTime/0 activates with a warning
            win.activate(X.CurrentTime)
            return False
        return True

    def _window_from_wid(self, wid):
        """Returns window instance from provided window identifier ``wid``.

        :param wid: windows id
        :type wid: int
        :returns: :class:`Wnck.Window` instance
        """
        return next(
            (
                win
                for win in Gdk.Screen.get_default().get_window_stack()
                if win.get_xid() == wid
            ),
            None,
        )

    ## COMMANDS
    def grab_window_screen(self, model):
        """Grabs and returns screenshot of the window from provided model.

        We can't include window decoration in image so offset in pixels
        for both axes is returned.

        :param model: model of the window we want screenshot from
        :type model: :class:`WindowModel`
        :param window: model window instance
        :type window: :class:`Gdk.Window`
        :param pixbuf: X11 pixbuf image
        :type pixbuf: binary data
        :param width: window width in pixels without window manager decoration
        :type width: int
        :param height: window height in pixels without window manager decoration
        :type height: int
        :returns: (:class:`PIL.ImageTk.PhotoImage`, (int, int))
        """
        window = self._window_from_wid(model.wid)
        if window is not None:
            width, height = window.get_width(), window.get_height()
            pixbuf = Gdk.pixbuf_get_from_window(window, 0, 0, width, height)
            return (
                get_prepared_screenshot(
                    self.collector.get_image_from_pixbuf(pixbuf),
                    blur_size=Settings.SCREENSHOT_BLUR_PIXELS,
                    grayscale=Settings.SCREENSHOT_TO_GRAYSCALE,
                ),
                (model.changed_w - width, model.changed_h - height),
            )
        return ImageTk.PhotoImage(Settings.BLANK_ICON), (0, 0)
